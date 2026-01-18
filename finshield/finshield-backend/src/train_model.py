import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import joblib
import json
from pathlib import Path
from datetime import datetime

def train_model():
    """Train fraud detection model."""
    
    print("📊 Loading training data...")
    train_df = pd.read_csv('data/training_data.csv')
    test_df = pd.read_csv('data/test_data.csv')
    
    # Separate features and labels
    X_train = train_df.drop('fraud', axis=1)
    y_train = train_df['fraud']
    X_test = test_df.drop('fraud', axis=1)
    y_test = test_df['fraud']
    
    print(f"Training samples: {len(X_train)}")
    print(f"Test samples: {len(X_test)}")
    
    # Normalize features
    print("\n🔄 Normalizing features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Gradient Boosting model
    print("\n🤖 Training Gradient Boosting model...")
    model = GradientBoostingClassifier(
        n_estimators=100,
        learning_rate=0.1,
        max_depth=7,
        random_state=42
    )
    
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test_scaled)
    y_pred_proba = model.predict_proba(X_test_scaled)[:, 1]
    
    print("\n📈 Model Performance:")
    print(f"  Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"  Precision: {precision_score(y_test, y_pred):.4f}")
    print(f"  Recall:    {recall_score(y_test, y_pred):.4f}")
    print(f"  F1 Score:  {f1_score(y_test, y_pred):.4f}")
    print(f"  ROC-AUC:   {roc_auc_score(y_test, y_pred_proba):.4f}")
    
    # Save model
    print("\n💾 Saving model...")
    Path('models').mkdir(exist_ok=True)
    joblib.dump(model, 'models/fraud_model.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    # Save feature names
    feature_names = list(X_train.columns)
    with open('models/feature_names.json', 'w') as f:
        json.dump(feature_names, f)
    
    # Save metadata
    metadata = {
        'model_type': 'GradientBoostingClassifier',
        'training_date': datetime.now().isoformat(),
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'features': feature_names
    }
    with open('models/metadata.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("✅ Model saved to: models/fraud_model.pkl")
    print("✅ Scaler saved to: models/scaler.pkl")
    print("✅ Metadata saved to: models/metadata.json")

if __name__ == '__main__':
    train_model()
