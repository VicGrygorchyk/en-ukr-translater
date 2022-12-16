from typing import TYPE_CHECKING, Literal

from datasets import load_dataset, DatasetDict

from get_hugface_ds import get_pat_dataset, get_flores_dataset, get_ted_dataset

if TYPE_CHECKING:
    from transformers import PreTrainedTokenizerBase

langs_key = Literal['en', 'uk']


def get_dataset(path: str) -> 'DatasetDict':
    """
    Dataset of kind
    {\'id\': \'92924\', \'translation\': {\'en\': "", \'uk\': ""}}
    :return:
    """
    raw_datasets = load_dataset(path)
    split_datasets = raw_datasets['train'].train_test_split(train_size=0.92, seed=42)
    raw_datasets['train'] = split_datasets.pop('train')
    raw_datasets['validation'] = split_datasets.pop('test')
    return raw_datasets


def get_all_datasets(path) -> DatasetDict:
    pat = get_pat_dataset()
    flore = get_flores_dataset()
    ted = get_ted_dataset()
    custom_dataset = get_dataset(path)

    for item in flore['train']:
        pat['train'].add_item(item)
    for item in ted['train']:
        pat['train'].add_item(item)
    for item in custom_dataset['train']:
        pat['train'].add_item(item)

    pat['train'].shuffle(seed=42)

    for item in flore['test']:
        pat['test'].add_item(item)
    for item in ted['test']:
        pat['test'].add_item(item)
    for item in custom_dataset['test']:
        pat['test'].add_item(item)

    for item in flore['validation']:
        pat['validation'].add_item(item)
    for item in ted['validation']:
        pat['validation'].add_item(item)
    for item in custom_dataset['validation']:
        pat['validation'].add_item(item)

    return pat


def get_tokenized_datasets(
        tokenizer: 'PreTrainedTokenizerBase',
        datasets: 'DatasetDict',
        max_length: int,
        input_lang: langs_key = 'en',
        target_lang: langs_key = 'uk') -> 'DatasetDict':

    def preprocess_function(examples):
        inputs = [ex[input_lang] for ex in examples['translation']]
        targets = [ex[target_lang] for ex in examples['translation']]
        model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True)
        return model_inputs

    tokenized_datasets = datasets.map(preprocess_function, batched=True, remove_columns=datasets['train'].column_names)
    return tokenized_datasets
