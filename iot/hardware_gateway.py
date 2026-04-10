import sys
import os
import json
import time
from flask import Flask, request, jsonify

# Add project root to path to import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.pre_crypto import PRECrypto

app = Flask(__name__)

# Initialize Crypto for the Gateway (Edge Node)
crypto = PRECrypto()
# Generate a keypair for this gateway (simulating the edge device's identity)
priv_key, pub_key = crypto.generate_key_pair()
print("[Gateway] Secure Edge Node Initialized.")
print("[Gateway] Public Key established.")

# Shared file to pass data to the Streamlit App
DATA_FILE = os.path.join(os.path.dirname(__file__), "live_packet.json")

@app.route('/api/data', methods=['POST'])
def receive_data():
    """
    Endpoint for ESP32/NodeMCU to send data.
    Expected JSON: {"temp": 25, "hum": 60, ...}
    """
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        print(f"[Gateway] Received Raw Data: {data}")
        
        # 1. ENCRYPT AT THE EDGE
        # We encrypt the payload immediately upon receipt.
        # In a real scenario, this might encrypt to the Data Owner's public key.
        # Here, we encrypt to *our own* public key just to demonstrate the ciphertext creation
        # that the Streamlit app will then display/decrypt.
        payload_str = json.dumps(data)
        
        # Returns: (ephemeral_pub_bytes, nonce, ciphertext)
        encrypted_pkg = crypto.encrypt_data(pub_key, payload_str)
        
        # 2. SAVE FOR DASHBOARD
        # We save the HEX representation so it can be serialized to JSON
        # (Bytes are not JSON serializable)
        packet = {
            "timestamp": time.time(),
            "raw_payload": data,
            "ciphertext_hex": encrypted_pkg[2].hex(), # Only showing ciphertext for demo
            # In a real app we'd need to store the full tuple (eph_pub, nonce, cipher)
            # But for the dashboard "Last Packet" visualization, we just pass the raw + hex.
            # actually, let's pass the raw mostly, and the Streamlit app can re-simulate 
            # or we pass the tuple components if we want true decryption flow across processes.
            # SIMPLIFICATION: We will save the RAW data to the file, and let the Streamlit App
            # handle the encryption/decryption cycle in its loop for the visual demo, 
            # OR we act as a "Buffer".
            #
            # Let's go with "Buffer Mode": The Gateway receives valid data and updates the 'latest sensor reading'.
            # The Streamlit app reads this 'latest reading' efficiently.
            "status": "Buffered"
        }
        
        with open(DATA_FILE, 'w') as f:
            json.dump(packet, f)
            
        return jsonify({"status": "Encrypted & Queued", "timestamp": time.time()}), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/status', methods=['GET'])
def health_check():
    return jsonify({"status": "Gateway Online", "device": "Edge-01"}), 200

if __name__ == '__main__':
    # Run on 0.0.0.0 to accept connections from external devices (ESP32)
    print("Starting IoT Gateway on 0.0.0.0:5000...")
    app.run(host='0.0.0.0', port=5000)
