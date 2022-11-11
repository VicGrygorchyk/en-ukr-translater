from transformers import MarianTokenizer, PreTrainedTokenizerBase


def get_tokenizer(path_or_model: str) -> 'PreTrainedTokenizerBase':
    """
    Returns a tokenizer from pretrained model.
    :param path_or_model: path to the model, or the model name from HuggingFace lib
    :return:
    """
    return MarianTokenizer.from_pretrained(path_or_model)
