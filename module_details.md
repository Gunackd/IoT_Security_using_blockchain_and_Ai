# Used Module Details Description

## Project: A Blockchain-Based Proxy Re-Encryption for AI-Driven Zero Trust Access Control in IoT

---

## 1. External Python Libraries

### 1.1 Streamlit (`streamlit`)
| Property | Detail |
|---|---|
| **Type** | Web Application Framework |
| **Used In** | `app.py` |
| **Purpose** | Provides the entire interactive web-based dashboard UI for the project. It renders the real-time security operations centre (SOC) interface with tabs, metrics, charts, buttons, sidebars, and session state management. |
| **Key Functions Used** | `st.set_page_config()`, `st.sidebar`, `st.tabs()`, `st.columns()`, `st.button()`, `st.toggle()`, `st.selectbox()`, `st.line_chart()`, `st.json()`, `st.code()`, `st.metric()`, `st.expander()`, `st.session_state`, `st.markdown()`, `st.spinner()`, `st.toast()`, `st.balloons()`, `st.rerun()` |

---

### 1.2 Cryptography (`cryptography`)
| Property | Detail |
|---|---|
| **Type** | Cryptographic Operations Library |
| **Used In** | `core/pre_crypto.py` |
| **Purpose** | Implements the core Proxy Re-Encryption (PRE) cryptographic scheme using Elliptic Curve Cryptography (ECC) and AES-GCM symmetric encryption. This module is the cryptographic backbone of the entire project. |
| **Sub-modules Used** | |
| `ec` (Elliptic Curve) | `cryptography.hazmat.primitives.asymmetric.ec` — Used for ECC key pair generation (`ec.generate_private_key`, `ec.SECP256R1`) and Elliptic Curve Diffie-Hellman key exchange (`ec.ECDH()`). |
| `serialization` | `cryptography.hazmat.primitives.serialization` — Used to serialize/deserialize public keys to PEM format for transmission (`Encoding.PEM`, `PublicFormat.SubjectPublicKeyInfo`, `load_pem_public_key`). |
| `hashes` | `cryptography.hazmat.primitives.hashes` — Provides `SHA256` hashing algorithm used within the HKDF key derivation function. |
| `HKDF` | `cryptography.hazmat.primitives.kdf.hkdf` — HMAC-based Key Derivation Function that derives a 32-byte symmetric AES key from the ECDH shared secret. |
| `AESGCM` | `cryptography.hazmat.primitives.ciphers.aead` — AES-256-GCM authenticated encryption/decryption used to encrypt and decrypt the actual IoT data payloads. |

---

### 1.3 Pandas (`pandas`)
| Property | Detail |
|---|---|
| **Type** | Data Analysis & Manipulation Library |
| **Used In** | `app.py`, `core/ai_monitor.py` |
| **Purpose** | Used for structuring AI threat monitoring history into DataFrames for tabular display and real-time line chart visualization on the dashboard. Also provides `pd.Timestamp.now()` for precise timestamping of risk assessment events. |
| **Key Functions Used** | `pd.DataFrame()`, `pd.Timestamp.now()` |

---

### 1.4 NumPy (`numpy`)
| Property | Detail |
|---|---|
| **Type** | Numerical Computing Library |
| **Used In** | `app.py`, `core/ai_monitor.py` |
| **Purpose** | Generates synthetic training data for the Isolation Forest ML model (200 normal-distribution samples). Also used for reshaping input data arrays for scikit-learn model predictions and generating random simulated sensor readings (temperature values). |
| **Key Functions Used** | `np.random.randint()`, `np.array()` |

---

### 1.5 Scikit-Learn (`scikit-learn`)
| Property | Detail |
|---|---|
| **Type** | Machine Learning Library |
| **Used In** | `core/ai_monitor.py` |
| **Purpose** | Provides the **Isolation Forest** algorithm, an unsupervised machine learning model used for real-time anomaly detection. The model is pre-trained on a baseline of "normal" network traffic (2–10 requests/minute) and detects anomalous access patterns (e.g., DDoS-like bursts) by scoring new observations. |
| **Key Classes & Methods** | `IsolationForest(n_estimators=100, contamination=0.05, random_state=42)`, `.fit()`, `.decision_function()` |
| **Configuration** | 100 decision trees, 5% expected contamination rate, deterministic seed (42) |

---

### 1.6 Flask (`flask`)
| Property | Detail |
|---|---|
| **Type** | Lightweight Web Framework (Micro-framework) |
| **Used In** | `iot/hardware_gateway.py` |
| **Purpose** | Runs a REST API server on the IoT Hardware Gateway that receives real-time sensor data from ESP32/NodeMCU devices via HTTP POST requests. The gateway encrypts incoming data and buffers it in `live_packet.json` for consumption by the Streamlit dashboard. |
| **Key Components Used** | `Flask()`, `request.json`, `jsonify()`, `@app.route()` decorator, `app.run(host='0.0.0.0', port=5000)` |
| **Endpoints** | `/api/data` (POST — receive sensor data), `/api/status` (GET — health check) |

---

## 2. Python Standard Library Modules

| Module | Used In | Purpose |
|---|---|---|
| `hashlib` | `core/blockchain_manager.py` | Generates SHA-256 hashes for blockchain blocks and MD5 hashes for unique access request IDs. |
| `time` | `app.py`, `core/blockchain_manager.py`, `iot/device_simulator.py`, `iot/hardware_gateway.py` | Timestamps for blockchain blocks, access requests, encrypted packets, and encryption performance measurement. |
| `json` | `app.py`, `core/blockchain_manager.py`, `iot/hardware_gateway.py` | JSON serialization/deserialization for blockchain ledger persistence (`ledger.json`), live IoT packets (`live_packet.json`), and sensor data payloads. |
| `os` | `app.py`, `core/blockchain_manager.py`, `core/pre_crypto.py`, `iot/hardware_gateway.py`, `iot/device_simulator.py`, `verify_upgrade.py` | File path operations, checking file existence, generating cryptographically secure random bytes (`os.urandom(12)` for AES-GCM nonces), and file cleanup. |
| `random` | `core/ai_monitor.py`, `iot/device_simulator.py` | Simulating normal (2–8 req/min) and attack (50–80 req/min) access frequencies for AI model evaluation. |
| `sys` | `iot/device_simulator.py`, `iot/hardware_gateway.py`, `verify_upgrade.py` | Modifying `sys.path` to ensure cross-directory imports of core modules. |
| `base64` | `app.py` | Imported for potential Base64 encoding of encrypted data for display purposes. |
| `dataclasses` | `core/blockchain_manager.py` | `@dataclass` decorator and `asdict()` for the `AccessRequest` structured data class, enabling clean serialization to JSON. |
| `typing` | `core/blockchain_manager.py` | Type hints (`Dict`, `List`, `Optional`) for function signatures to improve code readability and maintainability. |

---

## 3. Custom Project Modules

### 3.1 `core/blockchain_manager.py` — Blockchain Manager
| Property | Detail |
|---|---|
| **Classes** | `BlockchainManager`, `AccessRequest` (dataclass) |
| **Purpose** | Simulates a blockchain-based smart contract for Zero-Trust access control. Maintains an immutable chain of blocks (ledger), each containing hashed transaction data. Evaluates access requests using a policy engine that combines user role and AI-computed risk scores. |
| **Key Features** | Genesis block creation, SHA-256 block hashing, ledger persistence to `ledger.json`, smart contract logic (risk > 70 → BLOCK, trust < 50 → BLOCK), access request logging. |
| **Used By** | `app.py`, `verify_upgrade.py` |

---

### 3.2 `core/ai_monitor.py` — AI Threat Monitor
| Property | Detail |
|---|---|
| **Class** | `AIThreatMonitor` |
| **Purpose** | Implements a 3-Layer AI architecture for real-time threat detection and risk scoring. |
| **Layer 1** | **Anomaly Detection** — Uses Isolation Forest (ML) to detect abnormal access frequencies. Pre-trained on 200 synthetic normal samples (2–10 req/min). Scores > 65 trigger a security override. |
| **Layer 2** | **Behavioral Analysis** — Statistical drift detection using a rolling average of the last 5 access events per user. Detects sudden frequency spikes. |
| **Layer 3** | **Risk Scoring Engine** — Weighted ensemble combining Layer 1 (50%), Layer 2 (30%), and static trust (20%) into a final 0–100 risk score. |
| **Used By** | `app.py`, `verify_upgrade.py` |

---

### 3.3 `core/pre_crypto.py` — Proxy Re-Encryption Cryptography
| Property | Detail |
|---|---|
| **Class** | `PRECrypto` |
| **Purpose** | Implements an ECIES-like Proxy Re-Encryption scheme that enables secure data sharing between IoT devices and authorized users without exposing plaintext to intermediaries. |
| **Encryption Flow** | Generate ephemeral ECC key pair → ECDH shared secret → HKDF key derivation → AES-256-GCM encryption |
| **Re-Encryption** | Simulates proxy re-encryption by decrypting with the owner's key (in a Trusted Execution Environment) and re-encrypting for the new user's public key. |
| **Curve** | NIST P-256 (`SECP256R1`) |
| **Used By** | `app.py`, `iot/device_simulator.py`, `iot/hardware_gateway.py` |

---

### 3.4 `iot/device_simulator.py` — IoT Device Simulator
| Property | Detail |
|---|---|
| **Class** | `IoTDevice` |
| **Purpose** | Simulates an IoT edge device (sensor) that generates data and encrypts it at the edge using the PRE cryptographic module before transmission. Demonstrates the concept of "encrypt at the source" for zero-trust IoT security. |
| **Key Function** | `produce_encrypted_packet()` — Encrypts sensor readings using ECC public key cryptography. |
| **Used By** | `app.py` |

---

### 3.5 `iot/hardware_gateway.py` — Hardware Gateway (Flask API Server)
| Property | Detail |
|---|---|
| **Purpose** | Acts as an edge gateway server that bridges real ESP32/NodeMCU hardware with the Streamlit dashboard. Receives raw sensor data via REST API, encrypts it immediately at the edge, and buffers it in `live_packet.json` for the dashboard to consume. |
| **Endpoints** | `POST /api/data` (receive & encrypt sensor data), `GET /api/status` (health check) |
| **Used By** | `app.py` (reads `live_packet.json`), ESP32 firmware (sends HTTP POST) |

---

## 4. Arduino/ESP32 Libraries (C++ Firmware)

> **File:** `iot/esp32_firmware/esp32_firmware.ino`

| Library | Purpose |
|---|---|
| `WiFi.h` | ESP32 built-in WiFi library for establishing network connectivity. |
| `HTTPClient.h` | Enables the ESP32 to make HTTP POST requests to send sensor data (JSON) to the Flask hardware gateway server. |
| `WiFiManager.h` | Third-party library ([tzapu/WiFiManager](https://github.com/tzapu/WiFiManager)) that provides a captive portal for WiFi configuration. Eliminates the need for hardcoded WiFi credentials — the ESP32 creates an access point (`ESP32_Config_AP`) for initial setup. |

---

## 5. Module Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     STREAMLIT DASHBOARD (app.py)                │
│  ┌──────────┐   ┌──────────────┐   ┌────────────────────────┐  │
│  │ Streamlit│   │   Pandas     │   │       NumPy            │  │
│  │   (UI)   │   │  (DataFrames)│   │  (Sensor Simulation)   │  │
│  └────┬─────┘   └──────┬───────┘   └────────┬───────────────┘  │
│       │                │                     │                  │
│       ▼                ▼                     ▼                  │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │              SESSION STATE (Runtime Engine)             │    │
│  └──┬──────────────┬──────────────────┬───────────────┬────┘    │
│     │              │                  │               │         │
│     ▼              ▼                  ▼               ▼         │
│  Blockchain    AI Monitor         PRECrypto       IoTDevice     │
│  Manager       (sklearn)          (cryptography)  (Simulator)   │
│  (hashlib)                                                      │
└─────────┬───────────┬──────────────────┬────────────────────────┘
          │           │                  │
          ▼           │                  ▼
   ledger.json        │          live_packet.json ◄── Hardware
     (Persistence)    │           (IoT Buffer)        Gateway
                      │                               (Flask)
                      │                                  ▲
                      │                                  │
                      │                         ESP32 Firmware
                      │                      (WiFi.h, HTTPClient.h,
                      ▼                       WiFiManager.h)
               AI Risk Score
              (0-100 Decision)
```

---

## 6. Summary Table

| # | Module / Library | Version | Category | Primary Role |
|---|---|---|---|---|
| 1 | `streamlit` | Latest | External | Dashboard UI & session management |
| 2 | `cryptography` | Latest | External | ECC, ECDH, AES-GCM encryption (PRE scheme) |
| 3 | `pandas` | Latest | External | Data structuring & visualization support |
| 4 | `numpy` | Latest | External | Numerical operations & ML data generation |
| 5 | `scikit-learn` | Latest | External | Isolation Forest anomaly detection (ML) |
| 6 | `flask` | Latest | External | REST API gateway for hardware IoT devices |
| 7 | `hashlib` | Built-in | Standard Lib | SHA-256 blockchain hashing |
| 8 | `json` | Built-in | Standard Lib | Data serialization & ledger persistence |
| 9 | `os` | Built-in | Standard Lib | File I/O & cryptographic random bytes |
| 10 | `time` | Built-in | Standard Lib | Timestamps & performance measurement |
| 11 | `dataclasses` | Built-in | Standard Lib | Structured data classes |
| 12 | `WiFi.h` | ESP32 SDK | Arduino | ESP32 WiFi connectivity |
| 13 | `HTTPClient.h` | ESP32 SDK | Arduino | HTTP POST requests from ESP32 |
| 14 | `WiFiManager.h` | Third-party | Arduino | Captive portal WiFi configuration |
