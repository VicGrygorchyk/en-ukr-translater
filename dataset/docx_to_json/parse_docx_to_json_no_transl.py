import re
import json
from typing import List
from pathlib import Path
from dataclasses import dataclass, field
from glob import glob

import docx
from transformers import pipeline


dots_pattern = re.compile(r'^(«|"|“)?\.\.(\.)?(\.)?(»|"|”)?$')
match_parag = re.compile(r'^[0-9]+\.')
end_of_sent1 = re.compile(r'(?<=[\w0-9][^(v.)(no.)])\)?\. (?=[A-ZА-Я0-9])', re.UNICODE)
end_of_sent2 = re.compile(r'(?<=[\w0-9])[)"»”]?\. (?=[A-ZА-Я0-9])', re.UNICODE)

translator = pipeline("translation",
                      device='cudo:0',
                      model='/home/mudro/Documents/Projects/en-ukr-translater/models/saved/en_uk_legal_translater')


@dataclass
class ParsedResult:
    file_name: str
    result_list: List = field(default_factory=list)


def get_lines_from_docx(file_path):
    doc = docx.Document(file_path)
    full_text = []
    for parag in doc.paragraphs:
        txt: str = parag.text
        if (txt.strip() == '') or \
                (dots_pattern.match(parag.text)):
            continue
        full_text.append(txt.strip())
    return full_text


def docx_no_transl_to_json(eng_files: List[str], path_to_save: str, max_len: int):
    for eng_file in eng_files:
        res = parse(eng_file, max_len)
        save(res.result_list, path_to_save, res.file_name)


def parse(en_file_name: str, max_len: int) -> ParsedResult:
    print(f'English file {en_file_name}')
    ukr_file_part = en_file_name.split('/')[-1].replace('.docx', '')
    en_lines = get_lines_from_docx(en_file_name)
    en_to_ukr_list = []
    max_length = 0
    print(f'LENGTH BEFORE PROCESS ENG {len(en_lines)}')

    for en_line in en_lines:
        en_res = match_parag.match(en_line)
        eng_len = len(en_line)
        max_iter_len = eng_len
        # split very long line
        if max_iter_len > max_len:
            en_line_split = end_of_sent1.split(en_line)

            for en_l in en_line_split:
                uk_l = translator(en_l).pop()['translation_text']
                en_to_ukr_list.append(
                    {"en": en_l, "uk": uk_l}
                )
                print(f"-SPLITTED--------------------------\nEng line is = {en_l} \n Ukr line is = {uk_l}\n")
            continue

        ukr_line = translator(en_line).pop()['translation_text']
        en_to_ukr_list.append(
            {"en": en_line, "uk": ukr_line}
        )
        print(f"---------------------------\nEng line is = {en_line} \n Ukr line is = {ukr_line}\n")

        max_length = max_iter_len if max_iter_len > max_length else max_length
    print(f"MAX LENGTH IS {max_length}")
    print(f"LENGTH {len(en_to_ukr_list)}")
    return ParsedResult(ukr_file_part, en_to_ukr_list)


def save(en_to_ukr_list: List, path_to_save, file_name):
    result_list_without_split = []
    split_results = []

    for idx, item_ in enumerate(en_to_ukr_list):
        is_split = item_.get('tag')
        if is_split:
            split_results.append({"id": idx, "translation": item_})
        else:
            result_list_without_split.append({"id": idx, "translation": item_})
    path_to_curated_dir = Path(path_to_save)
    json_name = path_to_curated_dir / f'{file_name}.json'
    json_name_split_lines = path_to_curated_dir / f'SPLIT_{file_name}.json'

    with open(json_name, 'w+', encoding='utf-8') as json_f:
        json.dump(result_list_without_split, json_f, indent=4, ensure_ascii=False)
    if split_results:
        with open(json_name_split_lines, 'w+', encoding='utf-8') as json_f:
            json.dump(split_results, json_f, indent=4, ensure_ascii=False)
