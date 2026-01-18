import pandas as pd
import numpy as np
from pathlib import Path

def generate_synthetic_data(n_samples=2000):
    """Generate synthetic transaction data for fraud detection model training."""
    
    np.random.seed(42)
    
    data = {
        'keystroke_speed': np.random.uniform(20, 100, n_samples),
        'touch_pressure': np.random.uniform(0.5, 5.0, n_samples),
        'device_tilt': np.random.uniform(0, 45, n_samples),
        'payment_amount': np.random.uniform(100, 50000, n_samples),
        'merchant_type': np.random.randint(0, 7, n_samples),
        'time_of_day': np.random.randint(0, 4, n_samples),
    }
    
    # Create fraud labels based on patterns
    fraud_labels = []
    for i in range(n_samples):
        risk_score = 0
        
        if data['keystroke_speed'][i] < 30:
            risk_score += 30
        if data['touch_pressure'][i] < 1.5:
            risk_score += 35
        if data['device_tilt'][i] > 35:
            risk_score += 25
        if data['merchant_type'][i] in [5, 6] and data['payment_amount'][i] > 10000:
            risk_score += 40
        if data['time_of_day'][i] == 3 and data['payment_amount'][i] > 20000:
            risk_score += 30
        
        # Add noise (10% baseline fraud)
        if np.random.random() < 0.1:
            risk_score += np.random.uniform(20, 50)
        
        fraud_labels.append(1 if risk_score > 60 else 0)
    
    data['fraud'] = fraud_labels
    df = pd.DataFrame(data)
    
    return df

if __name__ == '__main__':
    # Create data directory
    Path('data').mkdir(exist_ok=True)
    
    print("📊 Generating synthetic transaction data...")
    train_df = generate_synthetic_data(n_samples=2000)
    test_df = generate_synthetic_data(n_samples=500)
    
    # Save data
    train_df.to_csv('data/training_data.csv', index=False)
    test_df.to_csv('data/test_data.csv', index=False)
    
    print(f"✅ Training data: {len(train_df)} samples")
    print(f"✅ Test data: {len(test_df)} samples")
    print(f"✅ Fraud rate: {train_df['fraud'].mean()*100:.1f}%")
    print("\n📈 Feature statistics:")
    print(train_df.describe())
    print("\n✅ Data saved to data/training_data.csv and data/test_data.csv")
