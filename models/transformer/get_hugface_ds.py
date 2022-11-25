"""
Reformat datasets to train, test, validation with schema {\'id\': \'92924\', \'translation\': {\'en\': "", \'uk\': ""}}
"""
from datasets import load_dataset, DatasetDict, Dataset


def get_flores_dataset() -> DatasetDict:
    """
    # dev 997 devtest - 1012
    # flores = load_dataset('facebook/flores', name='eng_Latn-ukr_Cyrl')
    {'id': 1,
    'URL': '',
    'domain': 'wikinews', 'topic': 'health', 'has_image': 0, 'has_hyperlink': 0,
    'sentence_eng_Latn': '', '
    sentence_ukr_Cyrl': ''}
    :return:
    """
    def format_item(ds_item):
        return {'id': ds_item['id'],
                'translation': {'en': ds_item['sentence_eng_Latn'], 'uk': ds_item['sentence_ukr_Cyrl']}}

    flores = load_dataset('facebook/flores', name='eng_Latn-ukr_Cyrl')
    flores = flores.map(format_item, remove_columns=['URL', 'domain', 'sentence_eng_Latn', 'sentence_ukr_Cyrl'])
    flores['train'] = flores.pop('dev')
    split_devtest = flores.pop('devtest').train_test_split(train_size=0.6, seed=442)

    for item in split_devtest['train']:
        flores['train'] = flores['train'].add_item(item)

    split_devtest_t = split_devtest['test'].train_test_split(train_size=0.5, seed=442)
    flores['validation'] = split_devtest_t['train']
    flores['test'] = split_devtest_t['test']

    return flores


def get_ted_dataset() -> DatasetDict:
    """
    # train - 2464
    # ted = load_dataset('ted_talks_iwslt', language_pair=("en", "uk"), year='2016')
    """
    ted = load_dataset('ted_talks_iwslt', language_pair=("en", "uk"), year='2016')
    split_datasets = ted['train'].train_test_split(train_size=0.8, seed=20)
    ted['train'] = split_datasets.pop('train')
    split_test_ds = split_datasets['test'].train_test_split(train_size=0.5, seed=20)
    ted['test'] = split_test_ds.pop('train')
    ted['validation'] = split_test_ds.pop('test')
    return ted


def get_pat_dataset() -> DatasetDict:
    """
    train 89226
    {'index': 3421,
    'family_id': 52275661,
    'translation':
    {'en': 'A replaceable handle to kitchen appliances comprises a bakelite handle with a connecting mechanism, available therein, a plastic part, which includes the upper section and the lower one, a spring, an aluminium part, which includes the upper section and the lower one.',
    'uk': "Знімна ручка до кухонного приладдя містить бакелітову ручку з наявним у ній з'єднувальним механізмом, пластикову частину, яка включає верхню секцію і нижню секцію, пружину, алюмінієву частину, яка включає верхню секцію і нижню секцію."}}
    """
    pat = load_dataset('para_pat', 'en-uk')
    split_datasets = pat['train'].train_test_split(train_size=0.95, seed=42)
    pat['train'] = split_datasets.pop('train')
    split_test_ds = split_datasets['test'].train_test_split(train_size=0.5, seed=42)
    pat['test'] = split_test_ds.pop('train')
    pat['validation'] = split_test_ds.pop('test')
    return pat


def get_all_datasets() -> DatasetDict:
    pat = get_pat_dataset()
    flore = get_flores_dataset()
    ted = get_ted_dataset()
    for item in flore['train']:
        pat['train'].add_item(item)
    for item in ted['train']:
        pat['train'].add_item(item)

    for item in flore['test']:
        pat['test'].add_item(item)
    for item in ted['test']:
        pat['test'].add_item(item)

    for item in flore['validation']:
        pat['validation'].add_item(item)
    for item in ted['validation']:
        pat['validation'].add_item(item)

    return pat
