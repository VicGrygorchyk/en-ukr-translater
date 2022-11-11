"""
BLUE metric
"""
from evaluate import load, EvaluationModule


def get_bleu_metrics() -> EvaluationModule:
    return load('sacrebleu')
