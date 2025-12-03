import streamlit as st
import time
import pandas as pd

# --- PLIANT BRANDING CONFIG ---
st.set_page_config(
    page_title="Pliant OpsEngine | Sovereign Architecture",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Pliant Look & Feel (Dark Blue/Clean)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #0a1e3c;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #1c3a63;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        border-left: 5px solid #0a1e3c;
    }
    .status-approved {
        color: #28a745;
        font-weight: bold;
    }
    .status-risk {
        color: #dc3545;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR: THE CONTROL TOWER ---
with st.sidebar:
    st.image("https://www.getpliant.com/hubfs/Pliant_Logo_Black.svg", width=150)
    st.markdown("### ⚙️ OpsEngine Control")
    st.markdown("---")
    
    mode = st.radio("Simulation Mode", ["Live Triage", "Backtest Analysis"])
    
    st.markdown("### 🔒 Risk Parameters")
    auto_approve_limit = st.slider("Auto-Approve Limit (€)", 0, 50000, 10000)
    min_cash_balance = st.number_input("Min Cash Balance Required", value=50000)
    
    st.markdown("---")
    st.caption("v2.1 | Architect: Fardan Qureshi")

# --- MAIN INTERFACE ---
st.title("💳 Pliant OpsEngine")
st.markdown("**Autonomous Triage & Risk Automation Protocol**")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📨 Incoming Ticket Stream")
    
    # Scenario Selector for Demo
    scenario = st.selectbox(
        "Select Demo Scenario:",
        [
            "Scenario A: Low Risk Limit Increase (Auto-Approve)",
            "Scenario B: High Risk / Low Balance (Block)",
            "Scenario C: AML Flag / Suspicious Merchant (Escalate)"
        ]
    )
    
    if scenario == "Scenario A: Low Risk Limit Increase (Auto-Approve)":
        default_text = "URGENT: Our Google Ads campaigns just paused because we hit the card limit. We need to increase the limit by €5,000 immediately or we lose revenue. Please help!"
        customer_data = {"Company": "TechFlow GmbH", "Cash Balance": "€145,000", "Repayment Score": "99/100", "Risk Tier": "Low"}
    
    elif scenario == "Scenario B: High Risk / Low Balance (Block)":
        default_text = "Hi, I need to raise my limit to €50k for a large equipment purchase today."
        customer_data = {"Company": "NewCo Logistics", "Cash Balance": "€12,000", "Repayment Score": "70/100", "Risk Tier": "Medium"}
        
    else:
        default_text = "Why was my transaction at 'CryptoKing Exchange' declined? Unblock my card now."
        customer_data = {"Company": "Shadow Corp", "Cash Balance": "€200,000", "Repayment Score": "90/100", "Risk Tier": "High (AML Watchlist)"}

    ticket_text = st.text_area("Ticket Content", value=default_text, height=150)
    
    st.markdown("### 🏢 Customer Profile (Live CRM Data)")
    st.json(customer_data)
    
    run_btn = st.button("🚀 Execute OpsEngine")

with col2:
    st.subheader("🧠 The Brain (Live Processing)")
    
    if run_btn:
        with st.spinner("Analyzing Intent & Risk..."):
            time.sleep(1.5) # Simulate processing time
            
            # 1. Intent Analysis
            st.markdown("#### 1. Intent Recognition")
            if "limit" in ticket_text.lower() and "increase" in ticket_text.lower():
                intent = "Credit Limit Increase"
                st.success(f"✅ Intent Detected: **{intent}**")
            elif "declined" in ticket_text.lower() or "unblock" in ticket_text.lower():
                intent = "Transaction Dispute / Unblock"
                st.warning(f"⚠️ Intent Detected: **{intent}**")
            else:
                intent = "General Support"
                st.info(f"ℹ️ Intent Detected: **{intent}**")
            
            time.sleep(1)
            
            # 2. Risk Engine Check
            st.markdown("#### 2. Risk Engine Audit")
            
            risk_decision = "PENDING"
            
            if intent == "Credit Limit Increase":
                requested_amount = 5000 if "5,000" in ticket_text else 50000 # Simple extraction for demo
                
                balance_clean = int(customer_data["Cash Balance"].replace("€", "").replace(",", ""))
                
                col_a, col_b = st.columns(2)
                col_a.metric("Requested", f"€{requested_amount:,}")
                col_b.metric("Cash Coverage", f"{balance_clean/requested_amount:.1f}x")
                
                if requested_amount <= auto_approve_limit and balance_clean > min_cash_balance:
                    risk_decision = "APPROVED"
                    st.markdown(f"<div class='metric-card'><span class='status-approved'>✅ RISK CHECK PASSED</span><br>Balance covers request > 3x. Repayment history perfect.</div>", unsafe_allow_html=True)
                else:
                    risk_decision = "REJECTED"
                    st.markdown(f"<div class='metric-card'><span class='status-risk'>🛑 RISK CHECK FAILED</span><br>Insufficient Cash Balance or Request exceeds Auto-Limit.</div>", unsafe_allow_html=True)
            
            elif intent == "Transaction Dispute / Unblock":
                if customer_data["Risk Tier"] == "High (AML Watchlist)":
                    risk_decision = "ESCALATE_AML"
                    st.markdown(f"<div class='metric-card'><span class='status-risk'>🚨 AML ALERT TRIGGERED</span><br>Merchant Category Code (MCC) matches Crypto/Gambling.</div>", unsafe_allow_html=True)
            
            time.sleep(1)
            
            # 3. Final Action
            st.markdown("#### 3. Automated Action")
            
            if risk_decision == "APPROVED":
                st.success("🚀 **ACTION: LIMIT INCREASED (API v2)**")
                st.markdown("**Drafted Reply (Sent):**")
                st.info(f"Hi there,\n\nGood news! I've instantly approved your limit increase to €{requested_amount:,} based on your healthy cash balance.\n\nYour ads should be running again. Let us know if you need anything else!\n\n*OpsEngine AI*")
                
            elif risk_decision == "REJECTED":
                st.error("✋ **ACTION: ROUTED TO CREDIT ANALYST**")
                st.markdown("**Internal Note:**")
                st.code(f"BOT_NOTE: User requested €{requested_amount:,} but cash balance is only {customer_data['Cash Balance']}. Manual review required.")
                
            elif risk_decision == "ESCALATE_AML":
                st.error("👮 **ACTION: ACCOUNT FROZEN & ROUTED TO COMPLIANCE**")
                st.markdown("**Drafted Reply:**")
                st.info("Hi,\n\nYour transaction is currently under security review. Our Compliance Team will reach out within 2 hours.\n\n*Pliant Security*")

    else:
        st.info("Waiting for ticket stream...")