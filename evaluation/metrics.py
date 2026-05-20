from __future__ import annotations

import math
from collections import Counter
from typing import Iterable

from evaluation.normalize import extract_primary_number, normalize_text, tokenize


def safe_div(numerator: float, denominator: float) -> float:
    return numerator / denominator if denominator else 0.0


def precision_recall_f1(tp: int, fp: int, fn: int) -> dict[str, float]:
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    f1 = safe_div(2 * precision * recall, precision + recall) if precision and recall else 0.0
    return {"precision": precision, "recall": recall, "f1": f1}


def jaccard_similarity(left: Iterable[str], right: Iterable[str]) -> float:
    left_set = set(left)
    right_set = set(right)
    if not left_set and not right_set:
        return 1.0
    if not left_set or not right_set:
        return 0.0
    return len(left_set & right_set) / len(left_set | right_set)


def token_overlap_score(left: str, right: str) -> float:
    return jaccard_similarity(tokenize(left), tokenize(right))


def rouge_l_f1(reference: str, prediction: str) -> float:
    ref_tokens = tokenize(reference)
    pred_tokens = tokenize(prediction)
    if not ref_tokens and not pred_tokens:
        return 1.0
    if not ref_tokens or not pred_tokens:
        return 0.0
    lcs = _lcs_length(ref_tokens, pred_tokens)
    precision = lcs / len(pred_tokens)
    recall = lcs / len(ref_tokens)
    return safe_div(2 * precision * recall, precision + recall) if precision and recall else 0.0


def bleu_score(reference: str, prediction: str, max_n: int = 4) -> float:
    ref_tokens = tokenize(reference)
    pred_tokens = tokenize(prediction)
    if not ref_tokens and not pred_tokens:
        return 1.0
    if not ref_tokens or not pred_tokens:
        return 0.0

    precisions = []
    for n in range(1, max_n + 1):
        ref_counts = Counter(_ngrams(ref_tokens, n))
        pred_counts = Counter(_ngrams(pred_tokens, n))
        total = sum(pred_counts.values())
        if total == 0:
            precisions.append(0.0)
            continue
        overlap = sum(min(count, ref_counts[gram]) for gram, count in pred_counts.items())
        precisions.append((overlap + 1.0) / (total + 1.0))

    log_precision_sum = sum(math.log(precision) for precision in precisions if precision > 0.0)
    geometric_mean = math.exp(log_precision_sum / max_n)
    brevity_penalty = 1.0 if len(pred_tokens) > len(ref_tokens) else math.exp(1 - len(ref_tokens) / len(pred_tokens))
    return brevity_penalty * geometric_mean


def numeric_match(truth_value: str, pred_value: str, abs_tol: float, rel_tol: float) -> bool:
    truth_number = extract_primary_number(truth_value)
    pred_number = extract_primary_number(pred_value)
    if not truth_number or not pred_number:
        return False
    if truth_number["operator"] != pred_number["operator"]:
        return False
    truth = truth_number["value"]
    pred = pred_number["value"]
    tolerance = max(abs_tol, abs(truth) * rel_tol)
    return abs(truth - pred) <= tolerance


def scalar_exact_or_numeric_match(truth_value: str, pred_value: str, abs_tol: float, rel_tol: float) -> bool:
    left = normalize_text(truth_value)
    right = normalize_text(pred_value)
    if left == right:
        return True
    return numeric_match(left, right, abs_tol=abs_tol, rel_tol=rel_tol)


def _lcs_length(left: list[str], right: list[str]) -> int:
    previous = [0] * (len(right) + 1)
    for left_token in left:
        current = [0]
        for index, right_token in enumerate(right, start=1):
            if left_token == right_token:
                current.append(previous[index - 1] + 1)
            else:
                current.append(max(previous[index], current[-1]))
        previous = current
    return previous[-1]


def _ngrams(tokens: list[str], n: int) -> list[tuple[str, ...]]:
    if len(tokens) < n:
        return []
    return [tuple(tokens[index : index + n]) for index in range(len(tokens) - n + 1)]
