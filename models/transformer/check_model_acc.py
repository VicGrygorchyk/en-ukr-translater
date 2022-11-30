"""
Read json files, use models to get predictions and compare to saved result
"""
from typing import List, TypedDict, Optional, Literal
import glob
import json
from itertools import islice

from transformers import pipeline
import evaluate

ds_path = '/home/mudro/Documents/Projects/en-ukr-translater/dataset/curated/1243/*'
json_files = glob.glob(ds_path)

splitted = Literal["splitted"]
model_checkpoint = "/home/mudro/Documents/Projects/en-ukr-translater/models/saved/modelv_2"
translator = pipeline("translation", model=model_checkpoint, device='cuda:0')
metric = evaluate.load("sacrebleu")


class TranslationItem(TypedDict):
    en: str
    uk: str
    tag: Optional[splitted]


class DictItem(TypedDict):
    id: str
    translation: TranslationItem


class TranslatedText(TypedDict):
    translation_text: str


def check_transl_score(predictions: List[str], references: List[str], eng_orig, json_file_path):
    for pred, ref, eng in zip(predictions, references, eng_orig):
        result = metric.compute(predictions=[pred], references=[ref])
        score = result['score']
        if score < 20:
            print(f'+++ {json_file_path} +++\n')
            print(f'======================\nLow score {score}\nfor {pred}\nref {ref}\norigin {eng}\n')
            # raise Exception(f'Low score {score}\nfor {pred}.\nref {ref}')


def get_pred(eng_text: List[str]):
    all_results = []
    length = len(eng_text)
    step = 450
    for batch in list(islice(eng_text, idx, idx + step) for idx in range(0, length, step)):
        result: List[TranslatedText] = translator(list(batch))
        preds = [list(val.values())[0] for val in result]
        all_results.extend(preds)
    return all_results


def validate_each_item():
    for json_file_path in sorted(json_files):
        with open(json_file_path, 'r+', encoding='utf-8') as json_f:
            res_dict: List[DictItem] = json.load(json_f)
            eng_orig = []
            ukr_refs = []
            for item in res_dict:
                translation = item["translation"]
                eng_line = translation['en']
                ukr_line = translation['uk']
                if len(eng_line) > 512:
                    raise Exception(f'file {json_file_path}\n{len(eng_line)} for {eng_line}')
                if len(ukr_line) > 512:
                    raise Exception(f'file {json_file_path}\n{len(ukr_line)} for {ukr_line}')
                eng_orig.append(eng_line)
                ukr_refs.append(ukr_line)
            if eng_orig:
                preds = get_pred(eng_orig)
                check_transl_score(preds, ukr_refs, eng_orig, json_file_path)


validate_each_item()
