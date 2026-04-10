# Testing, Verification, and Validation Plan

## 1. Overview
This document outlines the strategy for ensuring the quality, reliability, and security of the **Blockchain-Based Proxy Re-Encryption & AI Access Control** system. It covers Unit Testing (individual components), Integration Testing (system interaction), Verification (compliance with requirements), and Validation (fitness for use).

---

## 2. Unit Testing Strategy
**Goal:** Verify that individual functions and classes working in isolation perform as expected.

### A. Core Modules (`core/`)

#### 1. Blockchain Manager (`core/blockchain_manager.py`)
*   **Test `create_block`**:
    *   *Input*: Standard transaction data.
    *   *Check*: Verify the block contains the correct `previous_hash` and the new `hash` satisfies difficulty requirements (if any).
*   **Test `evaluate_access`**:
    *   *Scenario 1 (Authorized)*: User="Alice", Trust=100, Risk=10. -> **Expect**: `True` (Access Granted).
    *   *Scenario 2 (High Risk)*: User="Alice", Trust=100, Risk=80. -> **Expect**: `False` (Access Denied).
    *   *Scenario 3 (Unknown User)*: User="Eve". -> **Expect**: `False`.
*   **Test `load_chain` / `save_chain`**:
    *   *Check*: Ensure the sequence of blocks in `ledger.json` matches the in-memory chain after a restart.

#### 2. Proxy Re-Encryption (`core/pre_crypto.py`)
*   **Test `encrypt` and `decrypt`**:
    *   *Procedure*: Encrypt "Hello World", then Decrypt it.
    *   *Check*: The result matches the original string.
*   **Test `re_encrypt`**:
    *   *Procedure*: Encrypt with Alice's key -> Re-encrypt for Bob -> Decrypt with Bob's private key.
    *   *Check*: Decryption is successful and matches the original data.

#### 3. AI Monitor (`core/ai_monitor.py`)
*   **Test `calculate_risk_score`**:
    *   *Input*: Known anomaly score and drift values.
    *   *Check*: Verify the mathematical weighting logic (e.g., does a high anomaly score dominate the result?).
*   **Test `detect_anomaly`**:
    *   *Mock*: Mock the `IsolationForest` to return fixed predictions (-1 for anomaly, 1 for normal).
    *   *Check*: Verify that the system correctly flags the request.

### B. IoT Gateway (`iot/hardware_gateway.py`)
*   **Test Endpoint `/api/data`**:
    *   *Input*: Valid JSON payload `{"temp": 25, "humidity": 60}`.
    *   *Check*: Response status 200 and data is written to `live_packet.json`.
    *   *Input*: Malformed JSON.
    *   *Check*: Response status 400.

---

## 3. Integration Testing Strategy
**Goal:** Verify that different modules work together correctly as a system.

### A. Data Flow Integration
*   **Flow**: `Device Simulator` -> `Hardware Gateway` -> `Dashboard (App.py)`
*   **Test**:
    1.  Start the `hardware_gateway.py`.
    2.  Run `device_simulator.py` (or send a CURL request).
    3.  Check `iot/live_packet.json` to confirm updates.
    4.  Verify `app.py` (via Streamlit runner) picks up the new values and displays them.

### B. AI & Blockchain Integration
*   **Flow**: `AI Monitor` -> `Blockchain Manager`
*   **Test**:
    1.  Trigger an "Attack" simulation in the Dashboard.
    2.  Verify `ai_monitor` produces a high Risk Score (>70).
    3.  Verify `blockchain_manager` records a "REJECTED" transaction in `ledger.json`.

---

## 4. Verification Processes
**Goal:** "Are we building the product right?" (Compliance with specs).

1.  **Code Review**:
    *   All changes to `core/` must be reviewed to ensure crypto logic is not inadvertently weakened.
    *   Check for hardcoded secrets (API keys, Private Keys) before committing.
2.  **Static Analysis**:
    *   Run `pylint` or `flake8` on the codebase to catch syntax errors and undefined variables.
    *   **Automated Check**: `pylint core/*.py iot/*.py`.
3.  **Traceability Matrix**:
    *   *Requirement*: "System must block users with Risk Score > 70."
    *   *Verification Logic*: Check `blockchain_manager.py` line ~54 to confirm the logic `if risk_score > 70: return False`.

---

## 5. Validation Processes
**Goal:** "Are we building the right product?" (User satisfaction & Real-world performance).

1.  **User Acceptance Testing (UAT)**:
    *   **UI Check**: Validate the "Cyberpunk" theme. Do the neon glows appear correctly? Is the dashboard responsive?
    *   **Usability**: Can a non-technical user interpret the "Trust Score" graph?
2.  **Attack Simulation (Security Validation)**:
    *   **Scenario**: Simulate a DDoS (High frequency requests).
    *   **Validation**:
        *   Does the system remain stable?
        *   Does existing "Normal" traffic still get processed (if rate limiting is per-user)?
        *   **Pass Criteria**: Anomaly detected within 2 seconds.
3.  **Hardware Validation**:
    *   **Scenario**: Connect a real ESP32 microcontroller with a DHT11 sensor.
    *   **Validation**:
        *   Disconnect WiFi on ESP32 -> Verify Dashboard shows "Connection Lost" or stale data.
        *   Reconnect -> Verify data resumes immediately.

---

## 6. Execution Plan (How to run tests)

### Prerequisites
Install testing tools:
```bash
pip install pytest mock
```

### Running Unit Tests
Navigate to the project root and run:
```bash
pytest tests/
```
*(Note: Create a `tests/` directory and populate it with `test_*.py` files corresponding to the strategies above.)*

### Manual Verification Checklist
- [ ] `ledger.json` updates after Access Grant/Deny.
- [ ] `live_packet.json` reflects real-time data.
- [ ] Dashboard graph updates every 2 seconds.
