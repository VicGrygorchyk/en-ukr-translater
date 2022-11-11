from typing import TYPE_CHECKING

from datasets import load_dataset, DatasetDict

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase


def get_dataset(path: str) -> 'DatasetDict':
    """
    Dataset of kind
    {\'id\': \'92924\', \'translation\': {\'en\': "", \'uk\': ""}}
    :return:
    """
    raw_datasets = load_dataset(path, 'law')
    split_datasets = raw_datasets['train'].train_test_split(train_size=0.9, seed=20)
    split_datasets['validation'] = split_datasets.pop('test')
    return split_datasets


def get_tokenized_dataset(
        tokenizer: 'PreTrainedTokenizerBase',
        datasets: 'DatasetDict',
        max_length: int) -> 'DatasetDict':

    def preprocess_function(examples=None):
        inputs = [ex['en'] for ex in examples['translation']]
        targets = [ex['uk'] for ex in examples['translation']]
        model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True)
        return model_inputs

    tokenized_datasets = datasets.map(preprocess_function, batched=True, remove_columns=datasets['train'].column_names)
    return tokenized_datasets
