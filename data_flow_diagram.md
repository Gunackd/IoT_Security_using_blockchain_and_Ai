# System Data Flow Diagram

This document illustrates how data moves through the **Blockchain-Based Proxy Re-Encryption** system, starting from the IoT edge layer, passing through the gateway, and being processed by the AI and Blockchain core before reaching the user dashboard.

```mermaid
graph TD
    %% Define Nodes
    IoT[("IoT Layer<br/>(ESP32 / Simulator)")]
    Gateway["Hardware Gateway<br/>(Flask API)"]
    JSON[("live_packet.json<br/>(Shared Storage)")]
    Dash["Dashboard<br/>(Streamlit app.py)"]
    
    subgraph "Secure Core"
        AI["AI Monitor<br/>(Anomaly Detection)"]
        BC["Blockchain Manager<br/>(Access Control)"]
        PRE["PRE Crypto<br/>(Encryption Engine)"]
        Ledger[("ledger.json<br/>(Immutable Log)")]
    end

    User((User/Admin))

    %% Data Flow
    IoT -- "1. POST Sensor Data (Encrypted)" --> Gateway
    Gateway -- "2. Write Data" --> JSON
    
    JSON -- "3. Poll/Read Data" --> Dash
    
    Dash -- "4. Extract User Behavior" --> AI
    AI -- "5. Return Risk Score" --> Dash
    
    Dash -- "6. Request Access (User + Risk)" --> BC
    BC -- "7. Validate & Append Block" --> Ledger
    BC -- "8. Return Permission (Allow/Deny)" --> Dash
    
    Dash -- "9. If Allowed: Request Re-Encryption" --> PRE
    PRE -- "10. Return Re-Encrypted Data" --> Dash
    
    Dash -- "11. Display Real-Time/Decrypted Data" --> User

    %% Styling
    style error stroke:#f00,stroke-width:2px
    style IoT fill:#e1f5fe,stroke:#01579b
    style Dash fill:#f3e5f5,stroke:#4a148c
    style BC fill:#fff3e0,stroke:#e65100
    style AI fill:#fff3e0,stroke:#e65100
    style PRE fill:#fff3e0,stroke:#e65100
```

## Detailed Flow Description

1.  **Ingestion**: The **IoT Layer** sends encrypted sensor packets to the **Hardware Gateway** via HTTP POST.
2.  **Buffering**: The Gateway writes the latest packet to the temporary **`live_packet.json`** file.
3.  **Visualization Loop**: The **Dashboard** (Streamlit) continuously polls `live_packet.json` for new data.
4.  **Security Analysis**: Before showing data, the Dashboard sends the current session context to the **AI Monitor** to calculate a Risk Score based on behavior anomalies.
5.  **Access Control**: The Dashboard requests access from the **Blockchain Manager**, providing the User requesting access and the calculated Risk Score.
6.  **Audit Logging**: The Blockchain Manager records the request (User, Risk, Decision) into the **Immutable Ledger** (`ledger.json`) and returns a strict Allow/Deny decision.
7.  **Data Reveal**: If access is granted, the **PRE Crypto** module re-encrypts the data for the specific user, and the Dashboard displays the decrypted content.
