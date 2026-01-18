import joblib
import json
import numpy as np
import time
from pathlib import Path

class FraudDetector:
    """Real-time fraud detection using trained ML model."""
    
    def __init__(self):
        """Load trained model and scaler."""
        self.model = joblib.load('models/fraud_model.pkl')
        self.scaler = joblib.load('models/scaler.pkl')
        
        with open('models/feature_names.json', 'r') as f:
            self.feature_names = json.load(f)
        
        with open('models/metadata.json', 'r') as f:
            self.metadata = json.load(f)
        
        print(f"✅ Model loaded: {self.metadata['model_type']}")
        print(f"✅ Accuracy: {self.metadata['accuracy']:.2%}")
    
    def predict(self, transaction_data):
        """Predict fraud probability for a transaction."""
        start_time = time.time()
        
        try:
            # Extract features in correct order
            features = [
                transaction_data['keystroke_speed'],
                transaction_data['touch_pressure'],
                transaction_data['device_tilt'],
                transaction_data['payment_amount'],
                transaction_data['merchant_type'],
                transaction_data['time_of_day']
            ]
            
            # Normalize
            features_scaled = self.scaler.transform([features])
            
            # Predict probability
            fraud_probability = self.model.predict_proba(features_scaled)[0][1]
            fraud_score = int(fraud_probability * 100)
            
            # Determine action
            if fraud_score < 30:
                action = 'APPROVE'
                explanation = 'Transaction pattern matches legitimate user behavior.'
            elif fraud_score < 50:
                action = 'STEP_UP'
                explanation = 'Transaction requires additional verification due to unusual patterns.'
            else:
                action = 'BLOCK'
                explanation = 'Transaction blocked due to high fraud risk indicators.'
            
            # Identify risk factors
            risk_factors = self._identify_risk_factors(transaction_data)
            
            processing_time_ms = (time.time() - start_time) * 1000
            
            return {
                'fraud_score': fraud_score,
                'is_fraud': fraud_score >= 50,
                'action': action,
                'explanation': explanation,
                'risk_factors': risk_factors,
                'processing_time_ms': round(processing_time_ms, 2)
            }
        
        except Exception as e:
            print(f"❌ Prediction error: {str(e)}")
            return {
                'fraud_score': 0,
                'is_fraud': False,
                'action': 'ERROR',
                'explanation': f'Processing error: {str(e)}',
                'risk_factors': [],
                'processing_time_ms': 0
            }
    
    def _identify_risk_factors(self, data):
        """Identify specific risk factors in the transaction."""
        risk_factors = []
        
        if data['keystroke_speed'] < 30:
            risk_factors.append('Unusually slow keystroke speed')
        elif data['keystroke_speed'] > 85:
            risk_factors.append('Unusually fast keystroke speed')
        
        if data['touch_pressure'] < 1.5:
            risk_factors.append('Low touch pressure - possible impersonation')
        
        if data['device_tilt'] > 35:
            risk_factors.append('Unusual device orientation')
        
        if data['payment_amount'] > 10000:
            risk_factors.append('High transaction amount')
        
        merchant_names = ['GROCERY', 'FUEL', 'SHOPPING', 'RESTAURANT', 'ELECTRONICS', 'JEWELRY', 'TRAVEL']
        if data['merchant_type'] in [5, 6]:
            risk_factors.append(f'High-risk merchant: {merchant_names[data["merchant_type"]]}')
        
        if data['time_of_day'] == 3 and data['payment_amount'] > 5000:
            risk_factors.append('Late night high-value transaction')
        
        return risk_factors if risk_factors else ['Transaction appears normal']

if __name__ == '__main__':
    detector = FraudDetector()
    
    # Test case 1: Normal transaction
    normal_transaction = {
        'keystroke_speed': 65,
        'touch_pressure': 4.2,
        'device_tilt': 12,
        'payment_amount': 500,
        'merchant_type': 0,
        'time_of_day': 0
    }
    
    result = detector.predict(normal_transaction)
    print("\n📊 Normal Transaction:")
    print(f"  Score: {result['fraud_score']}%")
    print(f"  Action: {result['action']}")
    print(f"  Time: {result['processing_time_ms']}ms")
    
    # Test case 2: Suspicious transaction
    suspicious_transaction = {
        'keystroke_speed': 25,
        'touch_pressure': 1.2,
        'device_tilt': 40,
        'payment_amount': 15000,
        'merchant_type': 5,
        'time_of_day': 3
    }
    
    result = detector.predict(suspicious_transaction)
    print("\n📊 Suspicious Transaction:")
    print(f"  Score: {result['fraud_score']}%")
    print(f"  Action: {result['action']}")
    print(f"  Time: {result['processing_time_ms']}ms")
    print(f"  Risk Factors: {', '.join(result['risk_factors'])}")
