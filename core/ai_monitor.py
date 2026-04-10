import random
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

class AIThreatMonitor:
    """
    3-Layer AI Architecture for Access Behavior Monitoring.
    Layer 1: Anomaly Detection (Isolation Forest) - Learns 'Normal' patterns.
    Layer 2: Behavioral Analysis (Frequency/Drift).
    Layer 3: Risk Scoring Engine (Weighted Decision).
    """
    def __init__(self):
        self.history = []
        
        # Initialize Model
        # Contamination is the expected proportion of outliers (0.05 = 5%)
        self.model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42)
        self.is_trained = False
        
        # Layer Weights
        self.w_anomaly = 0.5
        self.w_behavior = 0.3
        self.w_static = 0.2
        
        # Pre-train with synthetic 'normal' data to avoid empty model errors on start
        self._train_initial_model()

    def _train_initial_model(self):
        """Trains the Isolation Forest on synthetic 'normal' data."""
        # Generate 200 normal samples: Frequency 2-10 requests/min
        X_train = np.random.randint(2, 11, size=(200, 1))
        self.model.fit(X_train)
        self.is_trained = True
        print("[AI Monitor] Anomaly Detection Model Trained on Normal Baseline.")

    def _layer_1_anomaly_score(self, frequency):
        """
        Uses Isolation Forest to detect anomalies.
        Returns:
            Score 0-100 (where 100 is highly anomalous)
        """
        # DEMO HEURISTIC: 
        # The ML model detects outliers, but mapping the decision function to 0-100 can vary.
        # Since we know our normal range is ~2-10, anything > 20 is DEFINITELY an attack.
        if frequency > 20:
            return 100.0

        if not self.is_trained:
            return 0
            
        # Reshape for sklearn
        X = np.array([[frequency]])
        
        # decision_function returns value (negative = outlier, positive = inlier)
        # We invert this so that lower values are more risky
        score_raw = self.model.decision_function(X)[0]
        
        # Normalize to 0-100 risk score
        risk = 50 - (score_raw * 200) 
        risk = max(0, min(100, risk))
        
        return risk

    def _layer_2_behavior_drift(self, user_id, current_freq):
        """
        Checks for sudden spikes in usage frequency compared to history.
        """
        user_history = [h for h in self.history if h['user'] == user_id]
        if not user_history:
            return 0
        
        # Calculate Rolling Average (Last 5 accesses)
        recent_history = user_history[-5:]
        avg_freq = sum(h['frequency'] for h in recent_history) / len(recent_history)
        if avg_freq == 0: avg_freq = 1
        
        # Calculate drift
        drift = (current_freq - avg_freq) / avg_freq
        
        # Normalize drift to 0-100 score
        score = min(100, max(0, drift * 100))
        return score

    def calculate_risk_score(self, user_id: str, is_attack_simulation: bool = False) -> dict:
        """
        Full 3-Layer Evaluation.
        """
        # 1. Simulate Input Metrics
        if is_attack_simulation:
            # High frequency burst (e.g., 50-80 req/min)
            frequency = random.randint(50, 80)
        else:
            # Normal user behavior (e.g., 2-8 req/min)
            frequency = random.randint(2, 8)

        # 2. Run Layers
        
        # Layer 1: Anomaly (Machine Learning)
        l1_score = self._layer_1_anomaly_score(frequency)
        
        # Layer 2: Behavior (Statistical Drift)
        l2_score = self._layer_2_behavior_drift(user_id, frequency)
        
        # Layer 3: Risk Engine (Weighted Ensemble)
        # Static penalty for Unknown/Untrusted roles is handled in Blockchain manager for simplicity,
        # but here we can add a base risk.
        base_risk = 0
        
        # WEIGHT ADJUSTENT:
        # Prioritize Anomaly Detection logic over empty behavioral history
        final_score = (
            (self.w_anomaly * l1_score) +
            (self.w_behavior * l2_score) +
            base_risk
        )
        
        # CRITICAL SECURITY OVERRIDE: 
        # If Anomaly Detection (Layer 1) is very high (indicating a definite attack pattern),
        # do not let a lack of history (Layer 2) dilute the risk score.
        if l1_score > 65:
            final_score = max(final_score, l1_score)
            
        final_score = round(min(100, final_score), 2)
        
        result = {
            "user": user_id,
            "frequency": frequency,
            "l1_anomaly": round(l1_score, 2),
            "l2_behavior": round(l2_score, 2),
            "final_risk_score": final_score,
            "timestamp": pd.Timestamp.now()
        }
        
        # Update history
        self.history.append(result)
        
        # Online Learning: If normal and approved, we could partially retrain, 
        # but for this demo, we keep the baseline.
        
        return result
