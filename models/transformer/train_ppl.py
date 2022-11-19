from dataset_utils import get_dataset, get_tokenized_dataset
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager

from dataset import datasets_globals
from models import models_globals


DATASET_PATH = datasets_globals.CURATED_DATASET_PATH
MAX_LEN = datasets_globals.MAX_LEN
model_checkpoint = models_globals.MODEL_ABS_PATH  # "Helsinki-NLP/opus-mt-en-uk"
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved'


if __name__ == "__main__":
    raw_datasets = get_dataset(DATASET_PATH)
    tokenizer = get_tokenizer(model_checkpoint)
    tokenized_dataset = get_tokenized_dataset(tokenizer, raw_datasets, MAX_LEN)
    model = get_model(model_checkpoint)

    trainer = TrainerManager(
        save_path,
        model,
        tokenizer,
        tokenized_dataset
    )
    trainer.train(MAX_LEN)
