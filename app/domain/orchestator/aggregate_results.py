def build_output(binary_preds, classify_preds):
    result = {
        "binary_decision": binary_preds,
        "classify_decision": classify_preds if classify_preds else "Not enough agreement to classify"
    }
    return result
