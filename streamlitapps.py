import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="LLM Risk Framework",
    page_icon="🛡️",
    layout="wide"
)

# --- Mock Data (You would load this from a file) ---
risk_catalog = {
    "Prompt Injection": {
        "description": "An attack where a user inputs a malicious prompt designed to trick the LLM into ignoring its safety instructions or roles.",
        "impact": "Bypassing security filters, revealing sensitive system instructions, or unauthorized data access.",
        "stage": "Post-Deployment (Inference)"
    },
    "Data Leakage (Memorization)": {
        "description": "The LLM 'remembers' and reveals sensitive PII or proprietary data from its training set.",
        "impact": "Breach of confidentiality, regulatory fines (GDPR), loss of intellectual property.",
        "stage": "Pre-Deployment (Training) & Post-Deployment (Inference)"
    },
    "Membership Inference Attack (MIA)": {
        "description": "An attacker determines whether a specific data record (e.g., a user's personal info) was part of the model's training data.",
        "impact": "Violation of user privacy and data protection laws.",
        "stage": "Post-Deployment (Inference)"
    }
}

mitigation_catalog = {
    "Prompt Injection": [
        {"control": "Input Sanitization & Filtering", "type": "Technical", "desc": "Scan and sanitize user inputs to remove or neutralize malicious keywords, scripts, or instructions."},
        {"control": "Instruction Defense", "type": "Technical", "desc": "Clearly separate the system's 'master prompt' from the user's input using special formatting (e.g., XML tags)."},
        {"control": "Red Teaming", "type": "Procedural", "desc": "Proactively test the LLM with adversarial prompts to find vulnerabilities before deployment."}
    ],
    "Data Leakage (Memorization)": [
        {"control": "Differential Privacy (DP)", "type": "Technical (Data)", "desc": "Add statistical noise during training to prevent the model from memorizing specific data points."},
        {"control": "Output Filtering (PII Scrubbing)", "type": "Technical", "desc": "Use a secondary model or regex to scan and block sensitive data (like phone numbers) from appearing in the output."}
    ],
     "Membership Inference Attack (MIA)": [
        {"control": "Differential Privacy (DP)", "type": "Technical (Data)", "desc": "The most effective defense. Adds noise during training to make it mathematically difficult to infer individual data points."},
        {"control": "Data Anonymization", "type": "Procedural (Data)", "desc": "Ensure all PII is removed or heavily anonymized before being used in any fine-tuning dataset."}
    ]
}

# --- Sidebar Navigation ---
st.sidebar.title("LLM Risk Framework")
page = st.sidebar.radio(
    "Pilih Fasa:",
    ["🏠 Pengenalan (Home)", 
     "🔎 Fasa 1: Risk Identification", 
     "📊 Fasa 2: Risk Measurement", 
     "🛡️ Fasa 3: Risk Mitigation", 
     "⏱️ Fasa 4: Monitoring & Audit"]
)

# --- Page Content ---

if page == "🏠 Pengenalan (Home)":
    st.title("Data Security and Privacy Risk Assessment Framework for LLM Deployment")
    
    # st.image("path/to/your/4-phase-diagram.png") # Uncomment this to add your diagram
    st.markdown("""
    This application is an interactive demonstrator for the 4-phase risk assessment framework developed for the final year project: 
    **"Data Security and Privacy Risk Assessment in Large Language Model (LLM) Deployment"**.

    This tool guides a user (such as a security analyst or project manager) through the process of identifying, measuring, and mitigating the unique risks associated with deploying a Large Language Model.

    ### How to Use:
    Use the navigation on the left to move through each phase of the framework.
    """)

elif page == "🔎 Fasa 1: Risk Identification":
    st.header("Fasa 1: Risk Identification")
    st.markdown("This phase involves identifying and categorizing the unique threat vectors for LLMs.")
    
    st.subheader("Risk Taxonomy (Catalog)")
    st.markdown("Select a threat category to see a detailed description of common risks.")
    
    risk_choice = st.selectbox("Pilih Kategori Risiko:", options=risk_catalog.keys())
    
    if risk_choice:
        st.divider()
        data = risk_catalog[risk_choice]
        st.subheader(f"Threat: {risk_choice}")
        st.markdown(f"**Description:** {data['description']}")
        st.markdown(f"**Potential Impact:** {data['impact']}")
        st.info(f"**Stage Affected:** {data['stage']}", icon="ℹ️")

elif page == "📊 Fasa 2: Risk Measurement":
    st.header("Fasa 2: Risk Measurement (Metric)")
    st.markdown("This phase uses a qualitative risk matrix to score the identified threats.")
    
    st.subheader("Risk Calculator")
    st.markdown("Select your risk and use the sliders to determine the risk score.")
    
    risk_choice = st.selectbox("Pilih Risiko (dari Fasa 1):", options=risk_catalog.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        likelihood = st.slider("Likelihood (Kebarangkalian)", min_value=1, max_value=5, value=3)
    with col2:
        impact = st.slider("Impact (Kesan)", min_value=1, max_value=5, value=3)
        
    risk_score = likelihood * impact
    
    st.divider()
    st.subheader(f"Risk Score: {risk_score}")

    if risk_score >= 15:
        st.error(f"**Priority: HIGH / CRITICAL** (Score: {risk_score}) - Mitigation is mandatory.")
    elif risk_score >= 8:
        st.warning(f"**Priority: MEDIUM** (Score: {risk_score}) - Mitigation is recommended.")
    else:
        st.success(f"**Priority: LOW** (Score: {risk_score}) - Review periodically.")

elif page == "🛡️ Fasa 3: Risk Mitigation":
    st.header("Fasa 3: Risk Mitigation")
    st.markdown("This phase provides a catalog of recommended controls (defenses) mapped to each risk.")
    
    st.subheader("Control Catalog")
    st.markdown("Select the risk you want to mitigate.")
    
    risk_choice = st.selectbox("Pilih Risiko (dari Fasa 1):", options=mitigation_catalog.keys())
    
    if risk_choice:
        st.divider()
        st.subheader(f"Recommended Controls for: {risk_choice}")
        
        for control in mitigation_catalog[risk_choice]:
            with st.expander(f"**{control['control']}** ({control['type']})"):
                st.write(control['desc'])

elif page == "⏱️ Fasa 4: Monitoring & Audit":
    st.header("Fasa 4: Monitoring & Audit")
    st.markdown("This phase provides a checklist for continuous governance to ensure the framework remains effective.")
    
    st.subheader("Audit Checklist")
    st.markdown("Use this checklist for periodic reviews of the deployed LLM.")
    
    st.checkbox("Logging: Are all user prompts and (anonymized) LLM responses being logged?", value=True)
    st.checkbox("Anomaly Detection: Is there a system to detect unusual prompt patterns (e.g., high-frequency attacks)?")
    st.checkbox("Feedback Loop: Is there a process for new threats discovered during monitoring to be added back to the Fasa 1 Risk Catalog?", value=True)
    st.checkbox("Model Review: Has the model been reviewed for 'model drift' or new memorization vulnerabilities?")
    st.checkbox("Red Teaming: Has a periodic 'Red Team' exercise been scheduled to test for new prompt injection techniques?")