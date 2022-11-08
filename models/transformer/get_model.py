from transformers import AutoModelForSeq2SeqLM


def get_model(model_checkpoint_or_path):
    return AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint_or_path)
