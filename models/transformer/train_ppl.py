import os
import sys
from typing import TypedDict, List

from dataset_utils import get_dataset, get_tokenized_datasets
from tokenizer import get_tokenizer
from get_model import get_model
from trainer import TrainerManager
from tester import TesterManager
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


if __name__ == "__main__":
    # train the model in 3 phases: 1) on small legal vocab, 2) on small legal acts, 3) on courts decisions
    dataset_phases: List[ModelToPhaseMap] = [
        # {
        #     'model': f'{save_path}/modelv1',  # 'Helsinki-NLP/opus-mt-en-uk',
        #     'phase_path':  f'{DATASET_PATH}/phase1',
        #     'save_path': f'{save_path}/modelv1',
        #     'descr': 'Run on the small legal vocab'
        # },
        # {
        #     'model': f'{save_path}/modelv2',
        #     'phase_path': f'{DATASET_PATH}/phase2',
        #     'save_path': f'{save_path}/modelv2',
        #     'descr': 'Run on the dataset of small legal acts'
        # },
        # {
        #     'model': f'{save_path}/modelv2',
        #     'phase_path': f'{DATASET_PATH}/phase2_2',
        #     'save_path': f'{save_path}/modelv2_2',
        #     'descr': 'Run on the dataset of small legal acts 2'
        # },
        # {
        #     'model': f'{save_path}/modelv2_2',
        #     'phase_path': f'{DATASET_PATH}/phase2_3',
        #     'save_path': f'{save_path}/modelv2_3',
        #     'descr': 'Run on the dataset of small legal acts 3'
        # },
        {
            'model': f'{save_path}/modelv2_3',
            'phase_path': f'{DATASET_PATH}/phase2_4',
            'save_path': f'{save_path}/modelv2_4',
            'descr': 'Run on the dataset of small legal acts 4'
        },
        # {
        #     'model': f'{save_path}/modelv2_4',
        #     'phase_path': f'{DATASET_PATH}/phase2',
        #     'save_path': f'{save_path}/modelv2',
        #     'descr': 'Run on the dataset of small legal acts 5'
        # },
        # {
        #     'model': f'{save_path}/modelv2',
        #     'phase_path': f'{DATASET_PATH}/phase2_2',
        #     'save_path': f'{save_path}/modelv2_2',
        #     'descr': 'Run on the dataset of small legal acts 6'
        # },
        # {
        #     'model': f'{save_path}/modelv2_2',
        #     'phase_path': f'{DATASET_PATH}/phase2_3',
        #     'save_path': f'{save_path}/modelv2_3',
        #     'descr': 'Run on the dataset of small legal acts 7'
        # },
        # {
        #     'model': f'{save_path}/modelv2_3',
        #     'phase_path': f'{DATASET_PATH}/phase2_4',
        #     'save_path': f'{save_path}/modelv2_4',
        #     'descr': 'Run on the dataset of small legal acts 8'
        # },
        # {
        #     'model': f'{save_path}/modelv2_4',
        #     'phase_path': f'{DATASET_PATH}/phase3',
        #     'save_path': f'{save_path}/modelv3',
        #     'descr': 'Run on the dataset of courts decisions (HUDOC)'
        # }
    ]

    for phase_ in dataset_phases:
        model_path = phase_['model']
        run_name = phase_['save_path'].split('/')[-1]

        with mlflow.start_run(run_name=run_name, description=phase_['descr']):
            model = get_model(model_path)
            mlflow.pytorch.log_model(model, artifact_path='')
            # get dataset
            phase_path = phase_['phase_path']
            full_ds = get_dataset(phase_path)
            tokenizer = get_tokenizer(model_path)
            tokenized_datasets = get_tokenized_datasets(tokenizer, full_ds, MAX_LEN)
            # train
            trainer = TrainerManager(
                phase_['save_path'],
                model,
                tokenizer,
                tokenized_datasets
            )
            trainer.train(MAX_LEN)
            # test
            tester = TesterManager(model, tokenizer, tokenized_datasets['test'])
            tester.test(MAX_LEN)
