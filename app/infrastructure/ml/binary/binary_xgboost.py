from xgboost import XGBClassifier

def create_model():
    return XGBClassifier(
        objective='binary:logistic',
        random_state=42,
        n_estimators=100,       
        max_depth=3,            
        learning_rate=0.05,     
        subsample=0.8,          
        colsample_bytree=0.8,   
        reg_alpha=1,            
        reg_lambda=1            
    )
