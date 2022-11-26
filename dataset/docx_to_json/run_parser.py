import glob

from parse_docx_to_json import docx_to_json
from parse_txt_to_json import txt_to_json
from parse_tmx_to_json import tmx_to_json
from parse_single_txt_to_json import single_txt_to_json

from dataset import datasets_globals

curated_path = datasets_globals.CURATED_DATASET_PATH
MAX_LEN = datasets_globals.MAX_LEN
eng_files_docx = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/eng/*.docx')
ukr_files_docx = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/ukr/*.docx')

eng_files_txt = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/eng/*.en')
ukr_files_txt = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/ukr/*.uk')

tmx_files = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/*.tmx')

single_txt_to_json(
    '/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/english_ukranian_legal_dictionary.txt',
    path_to_save=f'{curated_path}/phase1'
)
txt_to_json(eng_files_txt, ukr_files_txt, path_to_save=f'{curated_path}/phase2', max_len=MAX_LEN)
tmx_to_json(tmx_files, path_to_save=f'{curated_path}/phase2', max_len=MAX_LEN)
docx_to_json(eng_files_docx, ukr_files_docx, path_to_save=f'{curated_path}/phase3', max_len=MAX_LEN)
