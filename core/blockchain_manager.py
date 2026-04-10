import hashlib
import time
import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

@dataclass
class AccessRequest:
    request_id: str
    user_id: str
    resource_id: str
    risk_score: float
    timestamp: float
    approved: bool
    status_reason: str

class BlockchainManager:
    """
    Simulates a Blockchain Smart Contract for Zero-Trust Access Control.
    Includes local persistence to 'ledger.json'.
    """
    def __init__(self, ledger_file="ledger.json"):
        self.ledger_file = ledger_file
        self.chain = []
        self.state = {
            "users": {
                "Alice": {"role": "Owner", "trust_score": 100},
                "Bob": {"role": "Authorized", "trust_score": 90},
                "Eve": {"role": "Unknown", "trust_score": 10}
            },
            "access_requests": []
        }
        self.load_ledger()
        
        if not self.chain:
            # Genesis Block
            self.add_transaction({"event": "GENESIS", "timestamp": time.time()})

    def load_ledger(self):
        """Loads chain and state from JSON file if exists."""
        if os.path.exists(self.ledger_file):
            try:
                with open(self.ledger_file, 'r') as f:
                    data = json.load(f)
                    self.chain = data.get("chain", [])
                    # In a real chain, state is recomputed from chain. 
                    # Here we load it if saved, or just keep default for users.
                    # We only load historical requests to persist the log.
                    saved_requests = data.get("access_requests", [])
                    # Convert dicts back to Dataclass objects
                    self.state["access_requests"] = [AccessRequest(**req) for req in saved_requests]
                print(f"[Blockchain] Ledger loaded. {len(self.chain)} blocks.")
            except Exception as e:
                print(f"[Blockchain] Error loading ledger: {e}")

    def save_ledger(self):
        """Persists chain and relevant state to JSON."""
        data = {
            "chain": self.chain,
            "access_requests": [asdict(req) for req in self.state["access_requests"]]
        }
        try:
            with open(self.ledger_file, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Blockchain] Error saving ledger: {e}")

    def add_transaction(self, data: Dict):
        """Adds a transaction to the immutable ledger and persists it."""
        prev_hash = self.chain[-1]["hash"] if self.chain else "0"
        tx_hash = hashlib.sha256(f"{data}{prev_hash}".encode()).hexdigest()
        block = {
            "index": len(self.chain),
            "timestamp": time.time(),
            "data": data,
            "hash": tx_hash,
            "prev_hash": prev_hash
        }
        self.chain.append(block)
        self.save_ledger()
        return block

    def evaluate_access(self, user_id: str, resource_id: str, risk_score: float) -> AccessRequest:
        """
        Smart Contract Logic:
        Decides access based on User Role AND Dynamic Risk Score.
        Zero-Trust Policy: Risk Score > 70 => BLOCK, regardless of role.
        """
        user_info = self.state["users"].get(user_id)
        
        status_reason = "Processing"
        approved = False
        
        if not user_info:
            approved = False
            status_reason = "User Not Found"
        elif risk_score > 70:
            approved = False
            status_reason = f"High Risk Detected (Score: {risk_score})"
        elif user_info["trust_score"] < 50:
            approved = False
            status_reason = "Low Static Trust Score"
        else:
            approved = True
            status_reason = "Access Granted"

        request = AccessRequest(
            request_id=hashlib.md5(f"{user_id}{time.time()}".encode()).hexdigest(),
            user_id=user_id,
            resource_id=resource_id,
            risk_score=risk_score,
            timestamp=time.time(),
            approved=approved,
            status_reason=status_reason
        )
        
        # Update State
        self.state["access_requests"].append(request)
        
        # Log to Blockchain
        self.add_transaction({
            "event": "ACCESS_EVALUATION",
            "user": user_id,
            "risk": risk_score,
            "approved": approved
        })
        
        return request

    def get_ledger(self):
        return self.chain

    def get_latest_requests(self, limit=5):
        return self.state["access_requests"][-limit:]
