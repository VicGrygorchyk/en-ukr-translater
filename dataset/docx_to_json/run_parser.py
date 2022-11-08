import glob

from parse_docx_to_json import docx_to_json
from globals import MAX_LEN, CURATED_DATASET_PATH

curated_path = CURATED_DATASET_PATH
eng_files = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/eng/*')
ukr_files = glob.glob('/home/mudro/Documents/Projects/en-ukr-translater/dataset/raw/ukr/*')


docx_to_json(eng_files, ukr_files, curated_path, MAX_LEN)
