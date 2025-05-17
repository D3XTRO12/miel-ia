from xgboost import XGBClassifier

def create_model():
    """
    XGBoost con parámetros ajustados para mejor generalización y menos overfit.
    """
    return XGBClassifier(
        objective='multi:softprob',
        num_class=3,
        random_state=42,
        n_estimators=80,
        max_depth=3,
        learning_rate=0.02,
        subsample=0.7,
        colsample_bytree=0.7,
        min_child_weight=5,
        gamma=0.3,
        reg_alpha=1.0,
        reg_lambda=2.0,
        scale_pos_weight=1,
        tree_method='auto',
        eval_metric='mlogloss',
        use_label_encoder=False
    )
