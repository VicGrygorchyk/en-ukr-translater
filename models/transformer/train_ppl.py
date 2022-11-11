from dataset_utils import get_dataset, get_tokenized_dataset
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager
import sys

sys.path.append('/home/mudro/Documents/Projects/en-ukr-translater')
print(sys.path)
from globals import MAX_LEN, MODEL_ABS_PATH, CURATED_DATASET_PATH


DATASET_PATH = CURATED_DATASET_PATH
model_checkpoint = MODEL_ABS_PATH
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved'  # "Helsinki-NLP/opus-mt-en-uk"


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
