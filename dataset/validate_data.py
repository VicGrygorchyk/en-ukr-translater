"""
Read json files, use models to get predictions and compare to saved result
"""
from typing import List, TypedDict, Optional, Literal
import glob
import json

from transformers import pipeline
import evaluate

curated_path = '/home/mudro/Documents/Projects/en-ukr-translater/dataset/curated/*'
json_files = glob.glob(curated_path)

splitted = Literal["splitted"]
model_checkpoint = "Helsinki-NLP/opus-mt-en-uk"
translator = pipeline("translation", model=model_checkpoint)
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
        print(score)
        if score < 50:
            print(f'+++ {json_file_path} +++\n')
            print(f'======================\nLow score {score}\nfor {pred}.\nref {ref}.\norigin{eng}\n')
            # raise Exception(f'Low score {score}\nfor {pred}.\nref {ref}')


def get_pred(eng_text: List[str]) -> List[str]:
    result: List[TranslatedText] = translator(eng_text)
    return [list(val.values())[0] for val in result]


def validate_each_item():
    for json_file_path in sorted(json_files):
        with open(json_file_path, 'r+', encoding='utf-8') as json_f:
            res_dict: List[DictItem] = json.load(json_f)
            eng_orig = []
            ukr_refs = []
            for item in res_dict:
                translation = item["translation"]
                eng_orig.append(translation['en'])
                ukr_refs.append(translation['uk'])
            if eng_orig:
                ukr_preds = get_pred(eng_orig)
                check_transl_score(ukr_preds, ukr_refs, eng_orig, json_file_path)


validate_each_item()
