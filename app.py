import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(
    page_title="DevOps Spotlight Effect Simulator",
    page_icon="📊",
    layout="wide"
)

# Title and Description
st.title("📊 Engineering Resilience: Quantifying the Spotlight Effect")
st.markdown("""
This interactive simulator allows you to experiment with the empirical weights derived from our multiple linear regression model. 
Adjust the variables below to see how acute psychological stress, blame culture, and automation directly impact engineering system recovery times.
""")

st.divider()

# Sidebar for Model Coefficients (Updated to match your new Python model)
st.sidebar.header("🔧 Model Parameters (Regression Weights)")
st.sidebar.markdown("Adjust these to match your final `regression_results.txt` coefficients.")

# Updated defaults based on: MTTR = 20.0 + 2.0*Spotlight - 1.5*Blameless - 2.5*CICD
beta_0 = st.sidebar.number_input("Intercept (Baseline Hours)", value=20.0, step=0.1)
beta_1 = st.sidebar.number_input("Spotlight Effect Weight (Beta 1)", value=2.0, step=0.1)
beta_2 = st.sidebar.number_input("CI/CD Automation Weight (Beta 2)", value=2.5, step=0.1)
beta_3 = st.sidebar.number_input("Blameless Culture Weight (Beta 3)", value=1.5, step=0.1)

# Main Page Layout: Two Columns for Inputs and Outputs
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.header("🕹️ Live Operational Predictors")
    st.markdown("Simulate a specific team's cultural and technical profile:")
    
    # Inputs for the variables (1 to 5 Likert Scale)
    S = st.slider("Spotlight Index (S) - Acute Outage Stress", min_value=1.0, max_value=5.0, value=3.5, step=0.1,
                  help="1 = Calm & focused under pressure; 5 = Extreme panic and feeling hyper-scrutinized.")
    
    B = st.slider("Blameless Culture Score (B) - Psychological Safety", min_value=1.0, max_value=5.0, value=3.0, step=0.1,
                  help="1 = Heavy finger-pointing and fear; 5 = Complete psychological safety and focus on system flaws.")
    
    C = st.slider("CI/CD Automation Index (C) - Pipeline Maturity", min_value=1.0, max_value=5.0, value=4.0, step=0.1,
                  help="1 = Fully manual deployments; 5 = Elite automated continuous delivery pipelines.")

with col2:
    st.header("⏱️ Predicted Operational Outcome")
    
    # Calculate MTTR using the Multiple Linear Regression Equation
    # T_r = beta_0 + beta_1*S - beta_2*C - beta_3*B
    predicted_mttr = beta_0 + (beta_1 * S) - (beta_2 * C) - (beta_3 * B)
    
    # Prevent negative time in extreme mathematical scenarios (clamped to your 0.5 hour elite minimum)
    predicted_mttr = max(0.5, predicted_mttr)
    
    # Display the result prominently
    st.metric(
        label="Predicted Mean Time to Recovery (MTTR)", 
        value=f"{predicted_mttr:.2f} Hours",
        delta=f"Impact shift based on culture metrics"
    )
    
    # Dynamic classification badge based on standard DORA metrics
    if predicted_mttr <= 1.0:
        st.success("🏆 **DORA Performance Status: Elite Performance** (Under 1 hour)")
    elif predicted_mttr <= 4.0:
        st.info("📈 **DORA Performance Status: High Performance** (1-4 hours)")
    elif predicted_mttr <= 24.0:
        st.warning("⚠️ **DORA Performance Status: Medium Performance** (4-24 hours)")
    else:
        st.error("🚨 **DORA Performance Status: Low Performance** (More than 24 hours)")

st.divider()

# Section: Theoretical Scenario Mapping Visualizer
st.header("📈 Interactive Sensitivity Analysis")
st.markdown("See how MTTR changes across the entire spectrum of the Spotlight Effect for this specific team.")

# Generate data for the line chart based on the user's current settings
spotlight_range = np.linspace(1.0, 5.0, 50)
mttr_trend = beta_0 + (beta_1 * spotlight_range) - (beta_2 * C) - (beta_3 * B)
mttr_trend = np.clip(mttr_trend, 0.5, 36.0) # Matched your Python script's 0.5 to 36 clamp

chart_data = pd.DataFrame({
    'Spotlight Index (Stress)': spotlight_range,
    'Predicted MTTR (Hours)': mttr_trend
})

# Plotting with matplotlib/seaborn
fig, ax = plt.subplots(figsize=(10, 4))
sns.lineplot(data=chart_data, x='Spotlight Index (Stress)', y='Predicted MTTR (Hours)', ax=ax, color='#d32f2f', linewidth=2.5)
ax.axvline(x=S, color='#1976d2', linestyle='--', label=f'Current Team Stress Level ({S})')
ax.set_title("How Acute Panic Scales Downtime Hours", fontsize=12, fontweight='bold')
ax.set_xlabel("Spotlight Index (Acute Stress Scale 1-5)")
ax.set_ylabel("MTTR (Hours)")
ax.legend()
st.pyplot(fig)