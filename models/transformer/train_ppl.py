import os
import sys
from typing import TypedDict, List

from dataset_utils import get_dataset, get_tokenized_datasets
from get_hugface_ds import get_flores_dataset, get_ted_dataset, get_pat_dataset
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager
import mlflow

sys.path.append(os.getcwd())
from dataset import datasets_globals


DATASET_PATH = datasets_globals.CURATED_DATASET_PATH
MAX_LEN = datasets_globals.MAX_LEN
save_path = '/home/mudro/Documents/Projects/en-ukr-translater/models/saved'


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
            'model': 'Helsinki-NLP/opus-mt-en-uk',
            'phase_path': 'get_flores_dataset',
            'save_path': f'{save_path}/modelv1',
            'descr': 'Run on the flores dataset',
            'batch_size': 6
        },
        {
            'model': f'{save_path}/modelv1',
            'phase_path': 'get_ted_dataset',
            'save_path': f'{save_path}/modelv1_1',
            'descr': 'Run on the TED talk 2016 dataset',
            'batch_size': 6
        },
        {
            'model': f'{save_path}/modelv1_1',
            'phase_path': 'get_pat_dataset',
            'save_path': f'{save_path}/modelv1_2',
            'descr': 'Run on wikinews pat dataset',
            'batch_size': 3
        },
        # {
        #     'model': f'{save_path}/modelv1_2',
        #     'phase_path': f'{DATASET_PATH}/phase2',
        #     'save_path': f'{save_path}/modelv2',
        #     'descr': 'Run on the dataset of small legal acts',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2',
        #     'phase_path': f'{DATASET_PATH}/phase2_2',
        #     'save_path': f'{save_path}/modelv2_2',
        #     'descr': 'Run on the dataset of small legal acts 2',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_2',
        #     'phase_path': f'{DATASET_PATH}/phase2_3',
        #     'save_path': f'{save_path}/modelv2_3',
        #     'descr': 'Run on the dataset of small legal acts 3',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_3',
        #     'phase_path': f'{DATASET_PATH}/phase2_4',
        #     'save_path': f'{save_path}/modelv2_4',
        #     'descr': 'Run on the dataset of small legal acts 4',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_4',
        #     'phase_path': f'{DATASET_PATH}/phase3',
        #     'save_path': f'{save_path}/modelv3',
        #     'descr': 'Run on the dataset of courts decisions (HUDOC)',
        #     'batch_size': 4
        # },
        # {
        #     'model': f'{save_path}/modelv3',
        #     'phase_path': f'{DATASET_PATH}/phase2',
        #     'save_path': f'{save_path}/modelv2',
        #     'descr': 'Run on the dataset of small legal acts 5',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2',
        #     'phase_path': f'{DATASET_PATH}/phase2_2',
        #     'save_path': f'{save_path}/modelv2_2',
        #     'descr': 'Run on the dataset of small legal acts 6',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_2',
        #     'phase_path': f'{DATASET_PATH}/phase2_3',
        #     'save_path': f'{save_path}/modelv2_3',
        #     'descr': 'Run on the dataset of small legal acts 7',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_3',
        #     'phase_path': f'{DATASET_PATH}/phase2_4',
        #     'save_path': f'{save_path}/modelv2_4',
        #     'descr': 'Run on the dataset of small legal acts 8',
        #     'batch_size': 3
        # },
        # {
        #     'model': f'{save_path}/modelv2_4',
        #     'phase_path': f'{DATASET_PATH}/phase2_5',
        #     'save_path': f'{save_path}/modelv2_5',
        #     'descr': 'Run on the dataset of courts decisions (HUDOC)',
        #     'batch_size': 4
        # },
        # {
        #     'model': f'{save_path}/modelv2_4',
        #     'phase_path': f'{DATASET_PATH}/phase3',
        #     'save_path': f'{save_path}/modelv3',
        #     'descr': 'Run on the dataset of courts decisions (HUDOC)',
        #     'batch_size': 4
        # }
    ]

    datasets_map = {
        'get_flores_dataset': get_flores_dataset(),
        'get_ted_dataset': get_ted_dataset(),
        'get_pat_dataset': get_pat_dataset()
    }

    for phase_ in dataset_phases:
        model_path = phase_['model']
        run_name = phase_['save_path'].split('/')[-1]

        with mlflow.start_run(run_name=run_name, description=phase_['descr']):
            model = get_model(model_path)
            # get dataset
            phase_path = phase_['phase_path']
            full_ds = datasets_map.get(phase_path, get_dataset(phase_path))
            tokenizer = get_tokenizer(model_path)
            tokenized_datasets = get_tokenized_datasets(tokenizer, full_ds, MAX_LEN)
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
