import os
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class PRECrypto:
    def __init__(self):
        self.curve = ec.SECP256R1()

    def generate_key_pair(self):
        """Generates a private and public key pair using ECC SECP256R1."""
        private_key = ec.generate_private_key(self.curve)
        public_key = private_key.public_key()
        return private_key, public_key

    def derive_shared_secret(self, private_key, peer_public_key):
        """Derives a shared secret using ECDH."""
        shared_key = private_key.exchange(ec.ECDH(), peer_public_key)
        # Derive a symmetric key from the shared secret
        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'handshake data',
        ).derive(shared_key)
        return derived_key

    def encrypt_data(self, public_key, data):
        """
        Encrypts data using ECIES-like scheme:
        1. Generate ephemeral key pair.
        2. Derive shared secret with recipient's public key.
        3. Encrypt data with AES-GCM using derived secret.
        Returns: (ephemeral_public_key_bytes, nonce, ciphertext)
        """
        ephemeral_private, ephemeral_public = self.generate_key_pair()
        shared_secret = self.derive_shared_secret(ephemeral_private, public_key)
        
        aesgcm = AESGCM(shared_secret)
        nonce = os.urandom(12)
        if isinstance(data, str):
            data = data.encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, data, None)
        
        # Serialize ephemeral public key to send with ciphertext
        ephemeral_public_bytes = ephemeral_public.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return ephemeral_public_bytes, nonce, ciphertext

    def decrypt_data(self, private_key, ephemeral_public_key_bytes, nonce, ciphertext):
        """
        Decrypts data:
        1. Deserialize ephemeral public key.
        2. Derive shared secret with own private key.
        3. Decrypt with AES-GCM.
        """
        ephemeral_public_key = serialization.load_pem_public_key(ephemeral_public_key_bytes)
        shared_secret = self.derive_shared_secret(private_key, ephemeral_public_key)
        
        aesgcm = AESGCM(shared_secret)
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')

    # Simulation of Re-Encryption
    # In a real PRE scheme (like BBS98), there's a specific mathematical transformation.
    # For this system, we will simulate the Proxy's role:
    # The proxy "re-encrypts" by verifying access rights (Blockchain/AI) and then
    # wrapping the data for the new user.
    # Note: True PRE allows transformation WITHOUT decryption. 
    # Here we demonstrate the *Control Flow* of a semi-trusted proxy.
    
    def re_encrypt_for_user(self, owner_private_key, new_user_public_key, encrypted_package):
        """
        Simulates proxy re-encryption.
        In this demo flow:
        1. Proxy (simulated) holds the data.
        2. To grant access to 'new_user', we effectively re-key the data.
        NOTE: For a strict PRE demo without exposing plaintext to proxy, we would implement 
        NuCypher-like split-key logic. 
        For this functional prototype: We assume the Proxy is a Trusted Execution Environment (TEE).
        """
        # Unpack
        eph_pub_bytes, nonce, ciphertext = encrypted_package
        
        # 1. Recover Plaintext (TEE operation)
        # In this simplified demo, we assume the 'owner_private_key' is available to the TEE 
        # specifically for this re-encryption transaction authorized by the blockchain.
        plaintext = self.decrypt_data(owner_private_key, eph_pub_bytes, nonce, ciphertext)
        
        # 2. Encrypt for New User
        return self.encrypt_data(new_user_public_key, plaintext)

if __name__ == "__main__":
    # Quick Verification
    pre = PRECrypto()
    
    # Alice (Owner)
    alice_priv, alice_pub = pre.generate_key_pair()
    
    # Bob (Recipient)
    bob_priv, bob_pub = pre.generate_key_pair()
    
    # Alice encrypts data
    msg = "Secret IoT Sensor Data"
    print(f"Original: {msg}")
    encrypted_pkg = pre.encrypt_data(alice_pub, msg)
    print("Encrypted package generated.")
    
    # Proxy Re-Encryption (Alice -> Bob)
    # Simulator: Alice authorizes re-encryption for Bob
    print("Re-encrypting for Bob...")
    bob_pkg = pre.re_encrypt_for_user(alice_priv, bob_pub, encrypted_pkg)
    
    # Bob Decrypts
    decrypted = pre.decrypt_data(bob_priv, *bob_pkg)
    print(f"Bob Decrypted: {decrypted}")
    assert msg == decrypted
    print("Verification Successful!")
