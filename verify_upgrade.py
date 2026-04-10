import sys
import os

# Add project root to path
sys.path.append(os.getcwd())

from core.ai_monitor import AIThreatMonitor
from core.blockchain_manager import BlockchainManager

def verify_system():
    print("--- Verifying AI Monitor ---")
    ai = AIThreatMonitor()
    # Test Normal Prediction
    score_normal = ai._layer_1_anomaly_score(5) # Normal freq
    print(f"Normal Frequency Score (Should be low risk): {score_normal}")
    
    # Test Anomaly Prediction
    score_anomaly = ai._layer_1_anomaly_score(100) # Outlier freq
    print(f"Abnormal Frequency Score (Should be high risk): {score_anomaly}")
    
    print("\n--- Verifying Blockchain Persistence ---")
    bc = BlockchainManager("test_ledger.json")
    bc.add_transaction({"test": "data"})
    print(f"Chain length: {len(bc.chain)}")
    
    # Reload
    bc2 = BlockchainManager("test_ledger.json")
    print(f"Reloaded Chain length: {len(bc2.chain)}")
    assert len(bc.chain) == len(bc2.chain)
    print("Persistence Check Passed.")
    
    # Cleanup
    if os.path.exists("test_ledger.json"):
        os.remove("test_ledger.json")

if __name__ == "__main__":
    verify_system()
