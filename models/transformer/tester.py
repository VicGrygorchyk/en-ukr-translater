import numpy as np
from datasets import Dataset
from torch import no_grad as torch_no_grad
from torch.utils.data import DataLoader
from accelerate import Accelerator
from transformers import DataCollatorForSeq2Seq
from mlflow import log_metric

from metric_eval import get_bleu_metrics


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


class TesterManager:

    def __init__(self, model, tokenizer, tokenized_datasets: 'Dataset'):
        self.model = model
        self.tokenizer = tokenizer
        self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, self.model)
        tokenized_datasets.set_format("torch")
        self.test_dataloader = DataLoader(
            tokenized_datasets,
            collate_fn=self.data_collator,
            batch_size=8,
        )
        self.accelerator = Accelerator()

    def test(self, max_length):
        self.model.eval()
        for batch in self.test_dataloader:
            with torch_no_grad():
                generated_tokens = self.model.generate(
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
        log_metric('Test: bleu score for epoch', results['score'])
        precisions = np.average(results.get('precisions', [0]))
        log_metric('Test: precision score for epoch', precisions)
        print(f"Test: BLEU score: {results['score']:.2f}. Precision {precisions}")
