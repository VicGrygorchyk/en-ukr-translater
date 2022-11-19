import re
import json
from typing import List, Iterator
from pathlib import Path
from dataclasses import dataclass, field

from translate.storage.tmx import tmxfile


dots_pattern = re.compile(r'^(«|"|“)?\.\.(\.)?(\.)?(»|"|”)?$')
match_parag = re.compile(r'^[0-9]+\.')
end_of_sent1 = re.compile(r'(?<=[\w0-9][^(v.)(no.)])\)?\. (?=[A-ZА-Я0-9])', re.UNICODE)
end_of_sent2 = re.compile(r'(?<=[\w0-9])[)"»”]?\. (?=[A-ZА-Я0-9])', re.UNICODE)


@dataclass
class ParsedResult:
    file_name: str
    result_list: List = field(default_factory=list)


def get_tmx(file_path) -> 'tmxfile':
    with open(file_path, 'rb') as file:
        tmx_file = tmxfile(file, 'en', 'uk')
    return tmx_file


def tmx_to_json(files: List[str], path_to_save: str, max_len: int):
    for file_ in files:
        for res in parse(file_, max_len):
            save(res.result_list, path_to_save, res.file_name)


def parse(file_name: str, max_len: int) -> Iterator[ParsedResult]:
    print(f'file {file_name}')
    file_part = file_name.split('/')[-1].replace('.tmx', '')
    tmx_file = get_tmx(file_name)
    # pair en and ukr lines
    en_to_ukr_list = []
    max_length = 0
    file_parts = 1

    for unit in tmx_file.unit_iter():
        en_line = unit.source
        ukr_line = unit.target
        en_res = match_parag.match(en_line)
        ukr_res = match_parag.match(ukr_line)
        eng_len = len(en_line)
        uk_len = len(ukr_line)
        max_iter_len = max(eng_len, uk_len)
        # if paragraph starts with num, expect ukr_line to start as well
        if en_res:
            print('===================')
            if not ukr_res:
                print(f"File {file_name}. HELP!!! ------Eng line is = {en_line} \n Ukr line is {ukr_line}\n")
            elif en_res.group(0) != ukr_res.group(0):
                print(f" HELP!!! ------Eng line is = {en_line} \n Ukr line is {ukr_line}\n")

        en_to_ukr_list.append(
            {"en": en_line, "uk": ukr_line}
        )
        print(f"---------------------------\nEng line is = {en_line} \n Ukr line is = {ukr_line}\n")

        max_length = max_iter_len if max_iter_len > max_length else max_length
        # break if more than 1000 lines
        if len(en_to_ukr_list) >= 1000:
            yield ParsedResult(f'{file_part}_{file_parts}', en_to_ukr_list)
            en_to_ukr_list = []
            file_parts += 1
            print(f"MAX LENGTH IS {max_length}")
            print(f"LENGTH {len(en_to_ukr_list)}")
    return ParsedResult(file_part, en_to_ukr_list)


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
