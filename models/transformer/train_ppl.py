import os
import sys
from typing import TypedDict, List

from dataset_utils import get_dataset, get_tokenized_datasets
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager
from tester import TesterManager

sys.path.append(os.getcwd())
from dataset import datasets_globals


DATASET_PATH = datasets_globals.CURATED_DATASET_PATH
MAX_LEN = datasets_globals.MAX_LEN
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved/modelv1'


class ModelToPhaseMap(TypedDict):
    model: str
    phase_path: str


if __name__ == "__main__":
    # train the model in 3 phases: 1) on small legal vocab, 2) on small legal acts, 3) on courts decisions
    dataset_phases: List[ModelToPhaseMap] = [
        {
            'model': save_path,  # 'Helsinki-NLP/opus-mt-en-uk',
            'phase_path':  f'{DATASET_PATH}/phase1'
        },
        # {
        #     'model': save_path,
        #     'phase_path': f'{DATASET_PATH}/phase2'
        # },
        # {
        #     'model': save_path,
        #     'phase_path': f'{DATASET_PATH}/phase3'
        # }
    ]
    for phase_ in dataset_phases:
        model_path = phase_['model']
        phase_path = phase_['phase_path']
        full_ds = get_dataset(phase_path)
        tokenizer = get_tokenizer(model_path)
        tokenized_datasets = get_tokenized_datasets(tokenizer, full_ds, MAX_LEN)
        # train
        model = get_model(model_path)
        trainer = TrainerManager(
            save_path,
            model,
            tokenizer,
            tokenized_datasets
        )
        # trainer.train(MAX_LEN)
        # test
        tester = TesterManager(model, tokenizer, tokenized_datasets['test'])
        tester.test(MAX_LEN)
