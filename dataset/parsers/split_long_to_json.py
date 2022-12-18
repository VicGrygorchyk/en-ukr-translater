import re
import json
from typing import List, Dict
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


def split_long_to_json(eng_files: List[str], path_to_save: str, max_len: int):
    for eng_file in eng_files:
        res = parse(eng_file, max_len)
        save(res.result_list, path_to_save, res.file_name)


def get_lines_from_txt(file_path) -> List[Dict]:
    with open(file_path, 'r+') as file:
        full_text = json.load(file)
    return full_text


def parse(file_name: str, max_len: int) -> ParsedResult:
    print(f'file {file_name}')
    file_part = file_name.split('/')[-1].replace('.json', '')
    items_list = get_lines_from_txt(file_name)

    # pair en and ukr lines
    en_to_ukr_list = []
    max_length = 0
    print(f'LENGTH BEFORE PROCESS ENG {len(items_list)}')

    for item in items_list:  # type: Dict
        en_line = item['translation']['en']
        ukr_line = item['translation']['uk']
        en_res = match_parag.match(en_line)
        ukr_res = match_parag.match(ukr_line)

        eng_len = len(en_line)
        uk_len = len(ukr_line)
        max_iter_len = max(eng_len, uk_len)
        # split very long line
        if max_iter_len > max_len:
            en_line_split1 = end_of_sent1.split(en_line)
            uk_line_split1 = end_of_sent1.split(ukr_line)
            en_line_split2 = end_of_sent2.split(en_line)
            uk_line_split2 = end_of_sent2.split(ukr_line)
            if len(en_line_split1) == len(uk_line_split1):
                en_line_split = en_line_split1
                uk_line_split = uk_line_split1
            elif len(en_line_split1) == len(uk_line_split2):
                en_line_split = en_line_split1
                uk_line_split = uk_line_split2
            elif len(en_line_split2) == len(uk_line_split1):
                en_line_split = en_line_split2
                uk_line_split = uk_line_split1
            elif len(en_line_split2) == len(uk_line_split2):
                en_line_split = en_line_split2
                uk_line_split = uk_line_split2
            else:
                print(f"{[(num, line) for num, line in enumerate(en_line_split1)]}"
                      f"\n{[(num, line) for num, line in enumerate(uk_line_split1)]}")
                raise Exception(f"File {file_part}.\n"
                                f"{item['id']}\n"
                                f"{len(en_line_split1)} and {len(uk_line_split1)} can't be split automatically")

            for en_l, uk_l in zip(en_line_split, uk_line_split):
                en_to_ukr_list.append(
                    {"en": en_l, "uk": uk_l, 'tag': 'splitted'}
                )
                print(f"-SPLITTED--------------------------\nEng line is = {en_l} \n Ukr line is = {uk_l}\n")
            continue
        # if paragraph starts with num, expect ukr_line to start as well
        if en_res:
            print('===================')
            if not ukr_res:
                print(f"File {file_part}. HELP!!! ------Eng line is = {en_line} \n Ukr line is {ukr_line}\n")
                # fail
                raise Exception(f"File {file_part}. Eng line is = {en_line} \n Ukr line is {ukr_line}")
            elif en_res.group(0) != ukr_res.group(0):
                print(f" HELP!!! ------Eng line is = {en_line} \n Ukr line is {ukr_line}\n")
                # fail
                raise Exception(f"File {file_part}. Eng {en_res.group(0)} != Ukr {ukr_res.group(0)}")
            else:
                en_to_ukr_list.append(
                    {"en": en_line, "uk": ukr_line}
                )
            print(f"---------------------------\nEng line is = {en_line} \n Ukr line is = {ukr_line}\n")
            print('===================')
        else:
            # expected {'id': '92924', 'translation': {'en': "", 'fr': ""}}
            en_to_ukr_list.append(
                {"en": en_line, "uk": ukr_line}
            )
            print(f"---------------------------\nEng line is = {en_line} \n Ukr line is = {ukr_line}\n")

        max_length = max_iter_len if max_iter_len > max_length else max_length
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
