# Project Explanation: Blockchain-Based Proxy Re-Encryption with AI Access Control

## 1. Project Overview
**Title:** Blockchain-Based Proxy Re-Encryption Model with AI-Driven Access Monitoring for IoT
**Goal:** To create a secure, scalable, and Zero-Trust access control system for Internet of Things (IoT) devices. 

This system addresses the challenge of securely sharing data from edge devices (like sensors) to authorized users without a central authority having permanent access to plain text data. it combines:
*   **Blockchain**: For an immutable, decentralized audit log of all access requests and permissions.
*   **Proxy Re-Encryption (PRE)**: To allow secure data sharing where a semi-trusted proxy can transform ciphertext for a recipient without seeing the underlying data (simulated).
*   **AI Threat Monitoring**: A 3-layer security system to detect anomalous access patterns and block threats in real-time.

---

## 2. System Architecture

The system follows a layered architecture:

1.  **IoT Layer (Edge)**:
    *   Physical devices (ESP32/NodeMCU) or Simulators.
    *   Collects environmental data (Temperature, Humidity).
    *   Sends data to the Gateway.
2.  **Gateway Layer**:
    *   Acts as the bridge between insecure hardware and the secure backend.
    *   Buffers incoming data packets.
    *   Endpoint: `POST /api/data` on `hardware_gateway.py`.
3.  **Application Core (Backend/Logic)**:
    *   **Blockchain Manager**: Maintains the "Smart Contract" logic for access approval.
    *   **AI Monitor**: Analyzes user behavior to calculate Trust Scores.
    *   **PRE Crypto**: Handles encryption, key generation, and re-encryption logic.
4.  **Presentation Layer (Dashboard)**:
    *   Built with **Streamlit**.
    *   Provides a "Cyberpunk" themed UI for real-time monitoring.
    *   Visualizes the Blockchain ledger, AI metrics, and Live Data stream.

---

## 3. Key Components & Modules

### A. Dashboard (`app.py`)
The main entry point. It runs a Streamlit server to visualize the system.
*   **Visual Style**: Uses custom CSS for a reactive "Purple Cyberpunk" aesthetic (Glassmorphism, Neon glows).
*   **Tabs**:
    *   *Live Intercept*: Shows raw data coming from the IoT device and the encryption process.
    *   *AI Cortex*: Visualizes the Anomaly Detection model's status and history.
    *   *Blockchain Ledger*: Displays the immutable chain of blocks.
*   **Simulation Controls**: Allows toggling "Attack Mode" (simulates DDoS) or switching between "Simulated Data" and "Real Hardware".

### B. Blockchain Manager (`core/blockchain_manager.py`)
Acts as the authority for access control.
*   **Structure**: A local JSON-based ledger (`ledger.json`) that persists across runs.
*   **Smart Contract Logic**: The `evaluate_access()` function decides if a user can read data.
    *   **Rule 1 (Role)**: Must be an authorized role (Alice/Bob).
    *   **Rule 2 (Trust)**: User must have a high static Trust Score.
    *   **Rule 3 (Dynamic Risk)**: MUST NOT have a high AI Risk Score (>70).
*   **Immutability**: Every access decision is hashed and appended to the chain with the previous block's hash, ensuring the log cannot be tampered with.

### C. Proxy Re-Encryption (`core/pre_crypto.py`)
Handles the cryptographic operations.
*   **Scheme**: Uses **ECC (SECP256R1)** for asymmetric keys and **AES-GCM** for symmetric encryption.
*   **Workflow**:
    1.  **Encrypt**: Data is encrypted with a shared secret derived from the *Owner's* Public Key.
    2.  **Re-Encrypt (Simulated)**: The system acts as a trusted proxy. It decrypts the data using the Owner's key (in a TEE context) and re-encrypts it for the *Recipient's* Public Key.
*   **Why implementation is a "Simulation"**: True PRE (like BBS98 algorithm) allows mathematical transformation of ciphertext *without* decryption. This project simulates the *workflow* and access control aspect using standard ECDH/AES for broader compatibility and demonstration speed.

### D. AI Threat Monitor (`core/ai_monitor.py`)
A sophisticated 3-layer defense system:
*   **Layer 1 (Anomaly Detection)**: Uses an **Isolation Forest** (Machine Learning) model. It is pre-trained on a baseline of normal traffic (2-10 requests/min). Any significant deviation is flagged.
*   **Layer 2 (Behavioral Drift)**: Calculates statistical drift based on the specific user's history.
*   **Layer 3 (Risk Scoring Engine)**: Combines the above scores with weights to produce a final `Risk Score` (0-100).
    *   *Critical Override*: If Layer 1 detects a massive anomaly (score > 65), it overrides other factors to block the request immediately.

### E. IoT Gateway (`iot/hardware_gateway.py`)
A lightweight **Flask** server.
*   Listens on `0.0.0.0:5000` for JSON data.
*   Used to decouple the hardware from the main dashboard app.
*   Writes received data to `iot/live_packet.json` which the Streamlit app polls.

---

## 4. Hardware Integration

*   **Firmware**: `iot/esp32_firmware/esp32_firmware.ino`
*   **Function**: Connects to WiFi, reads sensors, and sends HTTP POST requests to the Gateway IP.
*   **Configuration**: Requires setting the `BACKEND_IP` in the sketch to match your PC's IP address.

## 5. How to Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure requirements includes: streamlit, pandas, numpy, cryptography, scikit-learn, flask)*

2.  **Start the Gateway** (optional, for real hardware):
    ```bash
    python iot/hardware_gateway.py
    ```

3.  **Start the Dashboard**:
    ```bash
    streamlit run app.py
    ```

## 6. Future Enhancements
*   **True PRE**: Replace the ECDH simulation with a library like `nucypher` or `pyumbral` for mathematically verifiable Proxy Re-Encryption.
*   **P2P Blockchain**: Move from a local `ledger.json` to a real P2P network or Ethereum testnet interaction.
*   **Database**: Replace the in-memory/JSON storage with SQLite or PostgreSQL for specialized production logging.
