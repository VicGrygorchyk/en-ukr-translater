import numpy as np
from tqdm.auto import tqdm
from torch import no_grad as torch_no_grad
from torch.optim import AdamW
from torch.utils.data import DataLoader
from accelerate import Accelerator
from transformers import DataCollatorForSeq2Seq, get_scheduler
from mlflow import log_metric, log_param

from metric_eval import get_bleu_metrics

LEARNING_RATE = 2e-5
WEIGHT_DECAY = 0.01
num_train_epochs = 20
metric = get_bleu_metrics()


def preprocess_preds_and_labels(tokenizer, predictions, labels):
    preds = predictions.cpu().numpy()
    lbls = labels.cpu().numpy()

    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Delete -100s pre-space in the labels
    labels = np.where(lbls != -100, lbls, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    decoded_preds = [pred.strip() for pred in decoded_preds]
    decoded_labels = [[label.strip()] for label in decoded_labels]

    return decoded_preds, decoded_labels


class TrainerManager:

    def __init__(self, output_dir, model, tokenizer, tokenized_datasets):
        self.model = model
        self.output_dir = output_dir
        self.tokenizer = tokenizer
        self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, self.model)
        log_param('Optimizer', 'AdamW')
        log_param('learning rate', LEARNING_RATE)
        log_param('weight decay', WEIGHT_DECAY)
        self.optimizer = AdamW(self.model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

        tokenized_datasets.set_format("torch")
        self.train_dataloader = DataLoader(
            tokenized_datasets["train"],
            shuffle=True,
            collate_fn=self.data_collator,
            batch_size=8,
        )
        self.eval_dataloader = DataLoader(
            tokenized_datasets["validation"], collate_fn=self.data_collator, batch_size=8
        )
        self.accelerator = Accelerator()
        # override model, optim and dataloaders to allow Accelerator to autohandle `device`
        self.model, self.optimizer, self.train_dataloader, self.eval_dataloader = self.accelerator.prepare(
            self.model, self.optimizer, self.train_dataloader, self.eval_dataloader
        )
        len_train_dataloader = len(self.train_dataloader)
        log_metric('Length of training dataloader', len_train_dataloader)
        num_update_steps_per_epoch = len_train_dataloader
        self.num_training_steps = num_train_epochs * num_update_steps_per_epoch
        # create scheduler with changing learning rate
        self.lr_scheduler = get_scheduler(
            "linear",
            optimizer=self.optimizer,
            num_warmup_steps=0,
            num_training_steps=self.num_training_steps,
        )

    def train(self, max_length):
        progress_bar = tqdm(range(self.num_training_steps))

        for epoch in range(num_train_epochs):
            # Training
            self.model.train()
            last_loss = None
            for batch in self.train_dataloader:
                outputs = self.model(**batch)
                loss = outputs.loss
                self.accelerator.backward(loss)

                self.optimizer.step()
                self.lr_scheduler.step()
                cur_lr = self.lr_scheduler.get_last_lr()[-1]
                log_metric('current train lr', cur_lr, epoch)
                self.optimizer.zero_grad()
                progress_bar.update(1)
                last_loss = loss

            log_metric('train loss', last_loss, epoch)
            print(f"epoch {epoch}, loss: {last_loss:.2f}")

            # Evaluation
            self.model.eval()
            unwrapped_model = self.accelerator.unwrap_model(self.model)
            for batch in tqdm(self.eval_dataloader):
                with torch_no_grad():
                    generated_tokens = unwrapped_model.generate(
                        batch["input_ids"],
                        attention_mask=batch["attention_mask"],
                        max_length=max_length,
                    )
                labels = batch["labels"]

                # Necessary to pad predictions and labels for being gathered
                generated_tokens = self.accelerator.pad_across_processes(
                    generated_tokens, dim=1, pad_index=self.tokenizer.pad_token_id
                )
                labels = self.accelerator.pad_across_processes(labels, dim=1, pad_index=-100)

                predictions_gathered = self.accelerator.gather(generated_tokens)
                labels_gathered = self.accelerator.gather(labels)

                decoded_preds, decoded_labels = preprocess_preds_and_labels(
                    self.tokenizer,
                    predictions_gathered,
                    labels_gathered
                )
                metric.add_batch(predictions=decoded_preds, references=decoded_labels)

            results = metric.compute()
            log_metric('Bleu score for epoch', results['score'])
            print(f"epoch {epoch}, BLEU score: {results['score']:.2f}")

            # Save the model and tokenizer
            self.accelerator.wait_for_everyone()
            unwrapped_model.save_pretrained(self.output_dir, save_function=self.accelerator.save)
            if self.accelerator.is_main_process:
                self.tokenizer.save_pretrained(self.output_dir)
