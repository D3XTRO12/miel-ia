def should_classify(binary_preds: dict) -> bool:
    positives = sum(1 for v in binary_preds.values() if v == 1)
    return positives >= 2
