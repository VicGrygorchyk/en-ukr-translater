from datasets import load_dataset


def get_dataset(path):
    """
    Dataset of kind
    {\'id\': \'92924\', \'translation\': {\'en\': "", \'uk\': ""}}
    :return:
    """
    raw_datasets = load_dataset(path, 'law')
    split_datasets = raw_datasets['train'].train_test_split(train_size=0.9, seed=20)
    split_datasets['validation'] = split_datasets.pop('test')
    return split_datasets


def get_tokenized_dataset(tokenizer, datasets, max_length):
    def preprocess_function(examples=None):
        inputs = [ex['en'] for ex in examples['translation']]
        targets = [ex['uk'] for ex in examples['translation']]
        model_inputs = tokenizer(inputs, text_target=targets, max_length=max_length, truncation=True)
        return model_inputs

    tokenized_datasets = datasets.map(preprocess_function, batched=True, remove_columns=datasets['train'].column_names)
    return tokenized_datasets
