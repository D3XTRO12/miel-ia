from sklearn.ensemble import RandomForestClassifier

def create_model():
    return RandomForestClassifier(
        n_estimators=100,         
        max_depth=10,             
        min_samples_split=10,     
        min_samples_leaf=4,       
        max_features='sqrt',      
        bootstrap=True,               
        random_state=42
    )
