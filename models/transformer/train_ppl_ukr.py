"""
Train ukr - eng model
"""
import os
import sys
from typing import TypedDict, List

from dataset_utils import get_dataset, get_tokenized_datasets
from get_hugface_ds import get_all_datasets
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
    # train the model in phases: 1) on articles from internet, 2) on small legal acts, 3) on courts decisions
    dataset_phases: List[ModelToPhaseMap] = [
        {
            'model': 'Helsinki-NLP/opus-mt-uk-en',
            'phase_path': 'get_all_datasets',
            'save_path': f'{save_path}/modelv1',
            'descr': 'Train ukr on the web dataset',
            'batch_size': 3
        },
        {
            'model': f'{save_path}/modelv1',
            'phase_path': f'{DATASET_PATH}/phase2',
            'save_path': f'{save_path}/modelv_2',
            'descr': 'Train ukr on the dataset of legal acts and courts decisions',
            'batch_size': 3
        }
    ]

    datasets_map = {
        'get_all_datasets': get_all_datasets
    }

    for phase_ in dataset_phases:
        model_path = phase_['model']
        run_name = phase_['save_path'].split('/')[-1]

        with mlflow.start_run(run_name=run_name, description=phase_['descr']):
            model = get_model(model_path)
            # get dataset
            phase_path = phase_['phase_path']
            dataset_func = datasets_map.get(phase_path, lambda: get_dataset(phase_path))
            full_ds = dataset_func()
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
