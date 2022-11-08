from transformers import MarianTokenizer


def get_tokenizer(path):
    return MarianTokenizer.from_pretrained(path)
