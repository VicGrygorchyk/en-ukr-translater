"""
Train ukr - eng model
"""
import os
import sys
from typing import TypedDict, List

from dataset_utils import get_tokenized_datasets, get_all_datasets
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager
import mlflow

sys.path.append(os.getcwd())
from dataset import datasets_globals


DATASET_PATH = datasets_globals.CURATED_DATASET_PATH
MAX_LEN = datasets_globals.MAX_LEN
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved_ukr'


class ModelToPhaseMap(TypedDict):
    model: str
    phase_path: str
    save_path: str
    descr: str
    batch_size: int


if __name__ == "__main__":
    dataset_phases: List[ModelToPhaseMap] = [
        {
            'model': f'{save_path}/modelv1',
            'phase_path': f'{DATASET_PATH}/cleared',
            'save_path': f'{save_path}/modelv2',
            'descr': 'Train ukr on the dataset of legal acts and courts decisions',
            'batch_size': 3
        }
    ]

    for phase_ in dataset_phases:
        model_path = phase_['model']
        run_name = phase_['save_path'].split('/')[-1]

        with mlflow.start_run(run_name=run_name, description=phase_['descr']):
            model = get_model(model_path)
            # get dataset
            full_ds = get_all_datasets(phase_['phase_path'])
            tokenizer = get_tokenizer(model_path)
            tokenized_datasets = get_tokenized_datasets(tokenizer, full_ds, MAX_LEN, input_lang='uk', target_lang='en')
            # train
            trainer = TrainerManager(
                phase_['save_path'],
                model,
                tokenizer,
                tokenized_datasets,
                batch_size=phase_['batch_size']
            )
            trainer.train(MAX_LEN)
            # test
            trainer.test(MAX_LEN)
