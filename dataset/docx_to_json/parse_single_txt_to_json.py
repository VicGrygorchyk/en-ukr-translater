import re
import json
from typing import List, Iterator
from pathlib import Path
from dataclasses import dataclass, field


dots_pattern = re.compile(r'^(«|"|“)?\.\.(\.)?(\.)?(»|"|”)?$')
match_parag = re.compile(r'^[0-9]+\.')
end_of_sent1 = re.compile(r'(?<=[\w0-9][^(v.)(no.)])\)?\. (?=[A-ZА-Я0-9])', re.UNICODE)
end_of_sent2 = re.compile(r'(?<=[\w0-9])[)"»”]?\. (?=[A-ZА-Я0-9])', re.UNICODE)


@dataclass
class ParsedResult:
    file_name: str
    result_list: List = field(default_factory=list)


def get_lines_from_txt(file_path):
    with open(file_path, 'r+', encoding='utf-8') as file:
        full_text = file.readlines()
    return full_text


def single_txt_to_json(file_path: str, path_to_save: str):
    for res in parse(file_path):
        save(res.result_list, path_to_save, res.file_name)


def parse(file_path: str) -> Iterator[ParsedResult]:
    print(f'file {file_path}')
    file_part = file_path.split('/')[-1].replace('.txt', '')
    _lines = get_lines_from_txt(file_path)
    # pair en and ukr lines
    en_to_ukr_list = []
    max_length = 0
    file_parts = 1

    for _line in _lines:
        en_line, ukr_line = _line.split('	')
        en_line = en_line.replace('\n', '')
        ukr_line = ukr_line.replace('\n', '')

        eng_len = len(en_line)
        uk_len = len(ukr_line)
        max_iter_len = max(eng_len, uk_len)

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
    yield ParsedResult(file_part, en_to_ukr_list)


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
