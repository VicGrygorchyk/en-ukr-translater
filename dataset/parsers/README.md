# How to parse files

For training we need a dataset with ukrainian to english sentences mapped. 
To achieve this, we execute the file `run_parser.py` to convert a raw docx files into json.
As a result, we should obtain the json files with objects of the format: 
`{"id": int, {"en": str, "uk": str}}`, where id is the line number and en is an
english source paragraph, uk is a ukrainian target paragraph.


