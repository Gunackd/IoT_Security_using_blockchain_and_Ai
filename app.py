import streamlit as st
import time
import json
import os # Added import
import pandas as pd
import numpy as np
import base64
from core.blockchain_manager import BlockchainManager
from core.ai_monitor import AIThreatMonitor
from core.pre_crypto import PRECrypto
from iot.device_simulator import IoTDevice

# ... (CSS and helper functions omitted for brevity, logic follows) ...

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Secure IoT | Zero Trust",
    layout="wide",
    page_icon="🛡️",
    initial_sidebar_state="expanded"
)

# --- CUSTOM CSS FOR "PURPLE CYBERPUNK" THEME ---
st.markdown("""
<style>
    /* MAIN CONTAINER & BACKGROUND */
    .stApp {
        background-color: #050510; /* Deepest Purple/Black */
        background-image: radial-gradient(circle at 50% 10%, #1a0b2e 0%, #050510 60%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }

    /* NEON PURPLE ACCENTS */
    :root {
        --primary-glow: #bf00ff;   /* The bright purple from the image */
        --secondary-glow: #00d2ff; /* Cyan accent */
        --danger-glow: #ff0055;    /* Red/Pink for threats */
        --bg-card: rgba(20, 10, 35, 0.7);
    }

    /* HEADERS */
    h1, h2, h3, h4 {
        color: #ffffff;
        font-family: 'Orbitron', 'Roboto', sans-serif; /* Tech font */
        text-transform: uppercase;
        letter-spacing: 1.5px;
        text-shadow: 0 0 10px rgba(191, 0, 255, 0.3);
    }

    /* GLASSMORPHISM CARDS */
    .stCard {
        background: var(--bg-card);
        border: 1px solid rgba(191, 0, 255, 0.3);
        border-left: 4px solid var(--primary-glow); /* Accent border left */
        border-radius: 8px;
        padding: 20px;
        backdrop-filter: blur(12px);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(191, 0, 255, 0.05);
        margin-bottom: 20px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .stCard:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(191, 0, 255, 0.15);
        border-color: var(--primary-glow);
    }

    /* METRICS & DATA TEXT */
    div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: var(--primary-glow);
        text-shadow: 0 0 15px var(--primary-glow);
        font-size: 2.2rem !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #a0a0ff;
        font-size: 0.9rem;
        text-transform: uppercase;
    }

    /* STATUS BADGES */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .status-ok {
        background: rgba(0, 255, 157, 0.1);
        color: #00ff9d;
        border: 1px solid #00ff9d;
        box-shadow: 0 0 10px rgba(0, 255, 157, 0.2);
    }
    .status-alert {
        background: rgba(255, 0, 85, 0.1);
        color: #ff0055;
        border: 1px solid #ff0055;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
    } 

    /* BUTTONS */
    .stButton button {
        background: linear-gradient(90deg, #2a0e45 0%, #4a148c 100%);
        color: white;
        border: 1px solid var(--primary-glow);
        border-radius: 4px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background: linear-gradient(90deg, #bf00ff 0%, #aa00ff 100%);
        box-shadow: 0 0 20px rgba(191, 0, 255, 0.6);
        border-color: white;
    }

    /* JSON/CODE BLOCKS */
    code {
        background-color: #0a0515 !important;
        color: #00d2ff !important; /* Cyan text for code */
        border: 1px solid #333;
    }
    
</style>
""", unsafe_allow_html=True)

# --- INITIALIZATION ---
if 'blockchain' not in st.session_state:
    st.session_state.blockchain = BlockchainManager() # Auto-loads ledger
if 'ai_monitor' not in st.session_state:
    with st.spinner("Initializing AI Models..."):
        st.session_state.ai_monitor = AIThreatMonitor()
if 'crypto' not in st.session_state:
    st.session_state.crypto = PRECrypto()
    st.session_state.owner_priv, st.session_state.owner_pub = st.session_state.crypto.generate_key_pair()
    st.session_state.iot_device = IoTDevice("Sensor-01")

# --- SIDEBAR ---
with st.sidebar:
    st.title("🔐 Control Center")
    st.markdown("---")
    user_selection = st.selectbox("Identity Spoofing", 
                                ["Alice (Owner)", "Bob (Authorized)", "Eve (Attacker)"])
    
    st.markdown("### ⚔️ Attack Simulation")
    attack_mode = st.toggle("Activate High-Freq Attack", 
                          help="Simulates a DDOS-like burst of requests to trigger AI Anomaly Detection.")
    
    st.markdown("### 🔌 Hardware")
    use_hardware = st.toggle("Use External Hardware (ESP32)", 
                           help="Reads data from iot/live_packet.json populated by the Gateway.")

    st.markdown("---")
    st.info(f"Blockchain Blocks: {len(st.session_state.blockchain.chain)}")
    if st.button("Values Reset (Ram Only)"):
        st.session_state.ai_monitor = AIThreatMonitor()
        st.rerun()

# --- MAIN LAYOUT ---
col_title, col_status = st.columns([3, 1])
with col_title:
    st.title("Blockchain Proxy Re-Encryption")
    st.caption("AI-Driven Zero Trust Access Control for IoT")
with col_status:
    if attack_mode:
        st.error("⚠️ SYSTEM UNDER ATTACK")
    elif use_hardware:
        st.info("🔌 HARDWARE LINKED")
    else:
        st.success("🟢 SYSTEM NOMINAL")

# Tabs
tab_live, tab_brain, tab_chain = st.tabs(["📡 Live Intercept", "🧠 AI Cortex", "🔗 Blockchain Ledger"])

# --- TAB 1: LIVE DATA ---
with tab_live:
    col_iot, col_gateway = st.columns(2)
    
    with col_iot:
        st.subheader("Edge Device (IoT)")
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        
        # LOGIC FOR DATA SOURCE
        data_source_ready = False
        data_payload = "{}"
        
        if use_hardware:
            st.caption("Listening to `iot/live_packet.json`...")
            gw_file = os.path.join("iot", "live_packet.json")
            
            if st.button("🔄 Sync Hardware Buffer"):
                if os.path.exists(gw_file):
                    try:
                        with open(gw_file, "r") as f:
                            packet = json.load(f)
                            # The gateway saves 'raw_payload' as a dict, we need string for encryption simulation
                            if isinstance(packet.get("raw_payload"), dict):
                                data_payload = json.dumps(packet["raw_payload"])
                            else:
                                data_payload = json.dumps({"error": "Invalid format from Gateway"})
                            data_source_ready = True
                            st.toast("Synced with ESP32!")
                    except Exception as e:
                        st.error(f"Read Error: {e}")
                else:
                    st.warning("No data found. Is `hardware_gateway.py` running?")
        else:
            if st.button("⚡ Generate & Encrypt Data"):
                # Simulation Mode
                temp = np.random.randint(20, 80)
                data_payload = json.dumps({
                    "temp": f"{temp}°C",
                    "status": "OK"
                })
                data_source_ready = True

        # ENCRYPTION STEP
        if data_source_ready:
            start_time = time.time()
            encrypted_pkg = st.session_state.crypto.encrypt_data(
                st.session_state.owner_pub, data_payload
            )
            enc_time = (time.time() - start_time) * 1000
            
            st.session_state.last_packet = {
                "payload": data_payload,
                "ciphertext": encrypted_pkg,
                "enc_time": enc_time
            }
            if use_hardware:
                st.info(f"External Data Encrypted ({enc_time:.2f}ms)")
            else:
                st.toast(f"Packet Encrypted in {enc_time:.2f}ms")
        
        if 'last_packet' in st.session_state:
            st.code(st.session_state.last_packet['payload'], language="json")
            if use_hardware:
                st.caption("Live Data from NodeMCU/ESP32")
            else:
                st.caption("Simulated Plaintext (On Device)")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_gateway:
        st.subheader("Security Gateway")
        st.markdown('<div class="stCard">', unsafe_allow_html=True)
        if 'last_packet' in st.session_state:
            # Hex dump visualization
            st.text(f"Encrypted Stream: {st.session_state.last_packet['ciphertext'][2][:40].hex()}...")
            
            if st.button(f"🔓 Decrypt Request ({user_selection})"):
                with st.spinner("AI Evaluating Trust Score..."):
                    time.sleep(0.4)
                    
                    # AI Check
                    risk_assessment = st.session_state.ai_monitor.calculate_risk_score(
                        user_selection, is_attack_simulation=attack_mode
                    )
                    risk_score = risk_assessment['final_risk_score']
                    
                    # Blockchain Check
                    access_req = st.session_state.blockchain.evaluate_access(
                        user_id=user_selection.split()[0], 
                        resource_id="Sensor-01", 
                        risk_score=risk_score
                    )
                
                # Result Visualization
                score_color = "red" if risk_score > 70 else "green"
                st.markdown(f"**Risk Score:** <span style='color:{score_color};font-size:1.2em'>{risk_score}/100</span>", unsafe_allow_html=True)
                
                if access_req.approved:
                    st.success(f"✅ ACCESS GRANTED")
                    st.json(st.session_state.last_packet['payload'])
                    st.balloons()
                else:
                    st.error(f"⛔ ACCESS DENIED: {access_req.status_reason}")
                    if risk_score > 70:
                        st.caption("Reason: Anomaly detected by Isolation Forest model.")
        else:
            st.info("Waiting for data stream...")
        st.markdown('</div>', unsafe_allow_html=True)

# --- TAB 2: AI BRAIN ---
with tab_brain:
    row1_col1, row1_col2 = st.columns([2, 1])
    
    with row1_col1:
        st.subheader("Real-Time Anomaly Detection (Isolation Forest)")
        if st.session_state.ai_monitor.history:
            df = pd.DataFrame(st.session_state.ai_monitor.history)
            
            # Chart
            st.line_chart(df[['l1_anomaly', 'final_risk_score']])
            st.caption("L1: Mathematical Outlier Score | Final: Weighted Risk Score")
        else:
            st.write("No data points yet.")

    with row1_col2:
        st.subheader("Model Weights")
        weights = {
            "Anomaly (ML)": st.session_state.ai_monitor.w_anomaly,
            "Behavior (Stat)": st.session_state.ai_monitor.w_behavior,
            "Static Trust": st.session_state.ai_monitor.w_static
        }
        st.dataframe(pd.DataFrame(list(weights.items()), columns=["Layer", "Weight"]), hide_index=True)
        
        st.info("The Isolation Forest model is pre-trained on a baseline of 2-10 req/min. Higher frequencies are tagged as anomalies.")

# --- TAB 3: BLOCKCHAIN ---
with tab_chain:
    st.subheader("Immutable Ledger (Persisted)")
    
    chain_data = st.session_state.blockchain.get_ledger()
    for block in reversed(chain_data):
        with st.expander(f"Block #{block['index']} [{block['hash'][:8]}...]", expanded=(block['index']==len(chain_data)-1)):
            st.json(block)
    
    if st.button("Force Save Ledger"):
        st.session_state.blockchain.save_ledger()
        st.success("Ledger saved to disk.")
