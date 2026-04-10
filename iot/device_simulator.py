import time
import sys
import os
import random

# Ensure we can import core modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.pre_crypto import PRECrypto

class IoTDevice:
    def __init__(self, device_id):
        self.device_id = device_id
        self.crypto = PRECrypto()
        # Edge Key Generation
        print(f"[{self.device_id}] Initializing Edge Security (ECC)...")
        self.private_key, self.public_key = self.crypto.generate_key_pair()
        print(f"[{self.device_id}] Secure Identity Established.")

    def produce_encrypted_packet(self, data_payload):
        """
        Simulates reading sensor data and ENCRYPTING AT THE EDGE.
        """
        print(f"[{self.device_id}] Reading Sensor: {data_payload}...")
        
        # Self-encrypting for storage/cloud (encrypt to own public key or gateway key)
        # For this demo, we encrypt to our own public key to simulate 
        # that only authorized re-encryption can unlock it.
        encrypted_pkg = self.crypto.encrypt_data(self.public_key, data_payload)
        
        print(f"[{self.device_id}] Sending Encrypted Packet... Success!")
        return encrypted_pkg

def run_simulation():
    device = IoTDevice("Device-X1")
    
    # Simulate a stream of data
    sensor_readings = ["Temp: 24.5C", "Humidity: 60%", "Vibration: Normal"]
    
    for reading in sensor_readings:
        device.produce_encrypted_packet(reading)
        time.sleep(1)

if __name__ == "__main__":
    run_simulation()
