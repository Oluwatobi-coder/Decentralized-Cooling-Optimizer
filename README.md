# Data-Driven Optimization of Residential Cooling Systems for a Decentralised Grid

[Open the Decentralised Cooling Systems Optimizer Tool❄️](https://decentralized-cooling-optimizer.streamlit.app/)


This project presents a predictive modeling and aggregation framework designed to determine the flexibility of residential cooling systems within a decentralised grid architecture. By using machine learning, the study models the power consumption of 3-ton residential heat pumps operated in cooling mode across a wide range of outside temperature (23.9°C to 46.1°C), and two indoor temperature setpoints: 22.22°C (baseline) and 24.44°C (load-shed).


## 📌 Project Overview

In decentralized grids, residential cooling demand closely tracks rising outdoor temperatures. Increase in demand can cause serious grid strains. Demand response methods rely on setpoint shifting to provide relief to the grid during these scenarios. This project demonstrates how set-point change on the cooling units can affect energy demand in a decentralised grid by training a digital twin on 8 distinct experimental datasets covering a wide range of outdoor temperatures ($23.9°C - 46.1°C$). The model quantifies exactly how much grid relief a particular number of cooling systems can provide and at a specified outdoor temperature, and also identifying the exact windows where the change is not desirable.

## 🛠️ Technology Used

* **Machine Learning:** XGBoost (Extreme Gradient Boosting), Scikit-Learn
* **Language:** Python 3.8+
* **Data Processing:** Pandas, NumPy, Joblib
* **Web Framework:** Streamlit
* **Visualization:** Plotly Interactive Charts, Matplotlib

## 🔳 Key Features

* **Thermodynamic Saturation Detection:** Automatically detects the ambient temperature (approx. 34°C) where the grid relief potential of the cooling units turn negative or inelastic.
* **Non-Linear Power Modeling:** Uses XGBoost ($R^2=0.89$) to capture the non-linearities in Coefficient of Performance (COP) that linear models miss.
* **Scenario Analysis Engine:** Simulates grid impact for "Baseline" (22.2°C) vs. "Load Shed" (24.4°C) scenarios across a sliding temperature scale.
* **Scalability:** Instantly scales predictions from a single cooling unit to a several units.

## 📂 Dataset

The model is trained on the **[NREL BENEFIT Dataset](https://data.nrel.gov/submissions/246)** (Hardware-in-the-Loop Experimental Data).
* **Equipment:** SEER 16 Heat Pump.
* **Range:** 8 experimental datasets covering $23.9°C$ to $46.1°C$ outdoor temperatures.
* **Resolution:** 1-second interval power and temperature data.

## 📁 Repository Structure

```text
├── data
│   ├── HP_Cool_OAT75F_SP72F68F.csv
│   ├── HP_Cool_OAT85F_SP76F72F68F.csv
│   ├── HP_Cool_OAT95F_SP76F72F68F.csv
│   ├── HP_Cool_OAT105F_SP68F.csv
│   ├── HP_Cool_OAT105F_SP76F72F.csv
│   ├── HP_Cool_OAT115F_SP68F.csv
│   ├── HP_Cool_OAT115F_SP72F.csv
│   ├── HP_Cool_OAT115F_SP76F.csv
├── eda_results
│   ├── eda_1_power_distribution.png
│   ├── eda_2_power_vs_deltaT.png
│   ├── eda_3_load_profile.png
│   ├── eda_4_control_error.png
│   ├── eda_5_hourly_profile.png
│   ├── eda_6_coil_temp_diff.png
├── model_and_scaler
│   ├── feature_scaler.pkl
│   ├── optimizer_model.pkl               
├── notebook
│   ├── energy_optimization_for_cooling.ipynb
├── README.md
├── LICENSE
└── requirements.txt

```

## 🚀 Getting Started

Follow these steps to set up the project environment locally:

### Prerequisites

**Python 3.8+**

### 1. Clone the Repository

```bash
git clone https://github.com/Oluwatobi-coder/Decentralized-Cooling-Optimizer.git
cd Decentralized-Cooling-Optimizer

```

### 2. Install Dependencies

```bash
pip install -r requirements.txt

```

## 🧠 Model Training & Validation

To reproduce the Saturation Threshold discovery:

1. Open `notebook/energy_optimization_for_cooling.ipynb`.
2. Run the cells to train the models and obtain the simulation results.

## 🌐 Running the Streamlit App

To launch the Digital Twin dashboard locally:

1. Navigate to the root directory.
2. Run the Streamlit command:
```bash
streamlit run ./streamlit_app/energy_optimzer_for cooling.py

```

3. Adjust the **Outdoor Temperature** slider and the number of **Heat Pump Units** to see the change in **Grid Impact Results**.

## 📊 Results

* **Model Performance:** XGBoost significantly outperformed Linear Regression in capturing non-linear relationships.

| Metric | Linear Regression | XGBoost |
| --- | --- | --- |
| **MAE** | ±210.54 W | **±56.21 W** |
| ** Score** | 0.55 | **0.89** |

* **The Saturation Point:** The table below (visualized in the app) shows why 34°C is the critical limit for grid operators.

| Outdoor Temp | Grid Relief (1k Cooling Units) | Grid Flexibility Status |
| --- | --- | --- |
| **31°C** | **-0.095 MW** | Effective (-3.29%) |
| **34°C** | **+0.033 MW** | Saturated (+1.13%) |

## 🤝 Contributing

Contributions to improve the predictive model or the set-point based grid relief approach are welcome:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/new-feature`).
3. Commit your changes.
4. Push to the branch and open a Pull Request.

## 📚 References

This project validates findings from the following core engineering resources:

American Society of Heating, Refrigerating and Air-Conditioning Engineers. (2021). Thermodynamics and refrigeration cycles. In 2021 ASHRAE handbook—Fundamentals (pp. 2.1–2.21). ASHRAE.

Chen, T., & Guestrin, C. (2016). XGBoost: A Scalable Tree Boosting System. In Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD ’16), 785–794. https://doi.org/10.1145/2939672.2939785

Palensky, P., & Dietrich, D. (2011). Demand side management: demand response, intelligent energy systems, and smart loads. IEEE Transactions on Industrial Informatics, 7(3), 381–388. https://doi.org/10.1109/tii.2011.2158841

Ramaraj, S., & Sparn, B. (2024). BENEFIT with Northeastern University: HVAC Hardware-in-the-Loop Experimental Testing of a Heat Pump and Air Conditioner. OSTI OAI (U.S. Department of Energy Office of Scientific and Technical Information). https://doi.org/10.7799/2440214

Wang, Z., & Srinivasan, R. S. (2016). A review of artificial intelligence based building energy use prediction: Contrasting the capabilities of single and ensemble prediction models. Renewable and Sustainable Energy Reviews, 75, 796–808. https://doi.org/10.1016/j.rser.2016.10.079

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.

If you find this work for your research, please ⭐ the repository!

