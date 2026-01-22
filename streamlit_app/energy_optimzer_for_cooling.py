# importing the necessary libraries
import streamlit as st
import pandas as pd
import joblib
import plotly.graph_objects as go


# configuring the page
st.set_page_config(
    page_title="Decentralised Cooling Systems Optimizer",
    page_icon="❄️",
    layout="wide"
)

# adding custom CSS
st.markdown("""
    <style>
    .reportview-container .main .block-container{ max-width: 1200px; }
    .stTable { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True)


# loading the model and the scaler
MODEL_FILE = "./model_and_scaler/optimizer_model.pkl"
SCALER_FILE = "./model_and_scaler/feature_scaler.pkl"

@st.cache_resource
def load_assets():
        model = joblib.load(MODEL_FILE)
        scaler = joblib.load(SCALER_FILE)
        return model, scaler


model, scaler = load_assets()


# setting up the sidebar
st.sidebar.header("🕹️ Simulation Parameters")
st.sidebar.write("Adjust the system inputs below:")
# Outdoor Temp: Range reflects your 7 stacked datasets (up to 46.1°C)
outdoor_temp = st.sidebar.slider(
    "Outdoor Ambient Temperature (°C)", 
    min_value=20.0, 
    max_value=46.0, 
    value=35.0, 
    step=0.5
)


# setting the number input for the cooling units
n_units = st.sidebar.number_input(
    "Number of Heat Pump Units (Cooling Mode)", 
    min_value=1, 
    max_value=1000000, 
    value=1000, 
    step=100
)

# displaying the baseline and load-shed setpoints
st.sidebar.markdown("---")
st.sidebar.info("""
**Setpoints:**
- **Baseline:** 22.22°C (Standard Comfort)
- **Load-Shed:** 24.44°C (Grid Relief Event)
""")


# adding the baseline and load-shed setpoints for prediction
SP_BASELINE = 22.22
SP_LOAD_SHED = 24.44

# specifying function for model input
def get_prediction(indoor_temp):
    # constructing the input for model
    raw_input = pd.DataFrame({
        'T_Outdoor (C)': [outdoor_temp],
        'T_Indoor (C)': [indoor_temp],
        'Delta_T': [outdoor_temp - indoor_temp]
    })
    # performing the scaling and prediction
    scaled_input = scaler.transform(raw_input)
    return model.predict(scaled_input)[0]

# predicting for a single cooling unit (Watts)
p_base = get_prediction(SP_BASELINE)
p_shed = get_prediction(SP_LOAD_SHED)

# calculating the difference between baseline and load-shed power (MW)
delta_shed_raw = p_shed - p_base
impact_shed_mw = (delta_shed_raw * n_units) / 1000000
flex_down_pct = (delta_shed_raw / p_base) * 100

# function to label the power difference
def get_status(val_mw):
    if val_mw > 0.005: return "INCREASED"
    elif val_mw < -0.005: return "REDUCED"
    else: return "STABLE"


# getting the label for the power difference
status_shed = get_status(impact_shed_mw)


# setting up the dashboard
st.title("❄️ Decentralised Cooling Systems Optimizer")
st.markdown(f"**Objective:** To determine the decentralised grid demand response for baseline and load-shed scenarios, at varying cooling units and outdoor temperatures.")


# setting up the result columns
col1, col2 = st.columns([3, 2])

# column 1: for grid impact results
with col1:
    st.subheader("Grid Impact Results")
    # converting results to a DataFrame for table display
    results_df = pd.DataFrame({
        "SCENARIO": ["1. BASELINE", "2. LOAD-SHED"],
        "SETPOINT": [f"{SP_BASELINE:.2f}°C", f"{SP_LOAD_SHED:.2f}°C"],
        "POWER (W)": [f"{p_base:.0f} W", f"{p_shed:.0f} W"],
        f"IMPACT (MW) - {n_units:,} units": ["0.000 MW", f"{impact_shed_mw:+.3f} MW"],
        "STATUS": ["BASELINE", status_shed]
    }).astype(object)
    st.table(results_df)

    st.markdown("#### **Grid Demand Summary**")
    st.write(f"📉 **Load-Shed Capacity:** `{flex_down_pct:+.2f}%` shift in demand potential.")

    # setting the notes section
    st.markdown("---")
    if flex_down_pct > 0:
        st.warning(f"**Note:** The positive shift (+{flex_down_pct:.2f}%) at {outdoor_temp}°C indicates **'Saturation'**. Raising the setpoint fails to reduce power because the compressor is already operating at its maximum physical limit to combat the high ambient temperature.")
    else:
        st.success(f"**Note:** The negative shift ({flex_down_pct:.2f}%) indicates successful **demand relief** on the grid. The individual heat pump units have sufficient capacity to modulate power in response to setpoint changes.")

# column 1: for the aggregated load profile
with col2:
    st.subheader("Aggregated Load Profile")

    # setting the analysis section
    if flex_down_pct > 0:
            st.info(f"""
    **Analysis:** At {outdoor_temp}°C, **{n_units} cooling units** draw more power from the grid when the setpoint is raised.
    """)
    else:
            st.info(f"""
    **Analysis:** At {outdoor_temp}°C, **{n_units} cooling units** function as a **{abs(impact_shed_mw):.3f} MW** Virtual Power Plant when the setpoint is raised.
    """)            
    # visualizing the aggregated load
    fig = go.Figure()
    
    # setting the bar chart to display the baseline and load-shed power
    fig.add_trace(go.Bar(
        x=['Baseline', 'Load-Shed'],
        y=[(p_base * n_units)/1000, (p_shed * n_units)/1000],
        marker_color=['#95A5A6', '#2ECC71' if flex_down_pct < 0 else '#E74C3C'],
        text=[f"{(p_base * n_units)/1000:.1f} kW", f"{(p_shed * n_units)/1000:.1f} kW"],
        textposition='auto',
    ))

    fig.update_layout(
        title=f"Total Power Demand (kW)",
        yaxis_title="Aggregated Power (kW)",
        template="plotly_white",
        height=410,
        width=400,
        showlegend=False
    )
    

    st.plotly_chart(fig, width="content")







