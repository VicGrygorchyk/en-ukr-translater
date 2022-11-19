import sys
import glob

from parse_docx_to_json import docx_to_json
from parse_txt_to_json import txt_to_json
from parse_tmx_to_json import tmx_to_json

sys.path.append('/home/mudro/Documents/Projects/en-ukr-translater')
from globals import MAX_LEN, CURATED_DATASET_PATH

curated_path = CURATED_DATASET_PATH
eng_files_docx = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/eng/*.docx')
ukr_files_docx = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/ukr/*.docx')

eng_files_txt = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/eng/*.en')
ukr_files_txt = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/ukr/*.uk')

tmx_files = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/*.tmx')

# docx_to_json(eng_files_docx, ukr_files_docx, curated_path, MAX_LEN)
txt_to_json(eng_files_txt, ukr_files_txt, curated_path, MAX_LEN)
tmx_to_json(tmx_files, curated_path, MAX_LEN)
