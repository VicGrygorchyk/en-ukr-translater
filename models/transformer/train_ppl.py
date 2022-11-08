from dataset_utils import get_dataset, get_tokenized_dataset
from tokenizer import get_tokenizer
from get_model import get_model
from metric_eval import compute_bleu_metrics
from trainer import TrainerManager
from globals import MAX_LEN, MODEL_ABS_PATH, CURATED_DATASET_PATH


DATASET_PATH = CURATED_DATASET_PATH
model_checkpoint = MODEL_ABS_PATH
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved'  # "Helsinki-NLP/opus-mt-en-uk"

raw_datasets = get_dataset(DATASET_PATH)
tokenizer = get_tokenizer(model_checkpoint)
tokenized_dataset = get_tokenized_dataset(tokenizer, raw_datasets, MAX_LEN)
model = get_model(model_checkpoint)

trainer = TrainerManager(
    save_path,
    model,
    tokenizer
)
trainer.set_trainer(tokenized_dataset, lambda preds: compute_bleu_metrics(tokenizer, preds))
trainer.train(MAX_LEN)
