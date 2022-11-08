from transformers import Seq2SeqTrainer, Seq2SeqTrainingArguments, DataCollatorForSeq2Seq


class TrainerManager:

    def __init__(self, output_dir, model, tokenizer):
        self.model = model
        self.output_dir = output_dir
        self.tokenizer = tokenizer
        self.data_collator = DataCollatorForSeq2Seq(self.tokenizer, self.model)
        self.args = Seq2SeqTrainingArguments(
            self.output_dir,
            evaluation_strategy="no",
            save_strategy="steps",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            per_device_eval_batch_size=8,
            weight_decay=0.01,
            save_total_limit=3,
            num_train_epochs=10,
            predict_with_generate=True,
            fp16=True,
            push_to_hub=False,
        )
        self._trainer = None

    @property
    def trainer(self) -> Seq2SeqTrainer:
        if not self._trainer:
            raise Exception('Trainer should be set.')
        return self._trainer

    def set_trainer(self, tokenized_datasets, compute_metrics):
        self._trainer = Seq2SeqTrainer(self.model, self.args,
                                       train_dataset=tokenized_datasets["train"],
                                       eval_dataset=tokenized_datasets["validation"],
                                       data_collator=self.data_collator,
                                       tokenizer=self.tokenizer,
                                       compute_metrics=compute_metrics)

    def train(self, max_length):
        print(f'''BLEU score before training {self.trainer.evaluate(max_length=max_length)}''')
        self.trainer.train()
        print(f'''BLUE score after training {self.trainer.evaluate(max_length=max_length)}''')
