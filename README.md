# 📦 Supply Prescript – Closed-Loop Prescriptive Analytics

![Python](https://img.shields.io/badge/Python-3.12-blue) ![XGBoost](https://img.shields.io/badge/XGBoost-Machine%20Learning-orange) ![SciPy](https://img.shields.io/badge/SciPy-Optimization-green) ![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red) ![SQLite](https://img.shields.io/badge/SQLite-Database-blue)

## 🚀 Overview
Supply Prescript is an end-to-end prescriptive analytics application designed to support supply-chain decision making. It combines machine learning, optimization, decision execution, and business impact evaluation in a closed-loop workflow.

**Predict → Optimize → Recommend → Execute → Evaluate → Learn**

## 🎯 Objectives
- Predict shipment delay probability using XGBoost.
- Estimate expected shipment delay.
- Generate optimized supply-chain actions using SciPy.
- Compare cost, delivery speed, and feasibility.
- Execute the selected business decision.
- Store decisions using SQLite.
- Evaluate cost savings and Decision ROI.

## ⭐ Key Features
🔮 **XGBoost Prediction** – Predicts shipment delay risk.  
⚙️ **SciPy Optimization** – Generates feasible supply-chain actions.  
💡 **Recommendation Engine** – Provides three alternative actions.  
🚀 **Decision Execution** – Executes the selected recommendation.  
🗄️ **SQLite Write-Back** – Records operational decisions.  
📊 **Decision History** – Tracks executed decisions.  
💰 **Cost Savings** – Measures business impact against baseline.  
📈 **Decision ROI** – Evaluates decision effectiveness.  
🔄 **Closed-Loop Evaluation** – Compares predicted and simulated actual outcomes.

## 🧠 Predictive Analytics
The XGBoost model uses supplier reliability, distance, order quantity, inventory level, transportation cost, weather risk, supplier capacity, demand level, and historical delay to predict shipment delay probability.

## ⚙️ Prescriptive Analytics
The optimization layer evaluates three operational alternatives:

**🏭 Secondary Supplier | 🚚 Standard Shipping | ✈️ Air Freight**

Each recommendation is evaluated using cost, delivery delay, feasibility, and recommendation score.

## 🔄 Closed-Loop Architecture
**Historical Data → XGBoost Prediction → Delay Probability → SciPy Optimization → Recommendations → Execute Decision → SQLite Write-Back → Actual Outcome → Cost Savings & ROI → Learn**

## 🛠️ Technology Stack
**Python | Pandas | NumPy | Scikit-learn | XGBoost | SciPy | Streamlit | SQLite | Matplotlib | Seaborn**

## 📁 Project Structure
Supply-Prescript/  
├── app/  
│   └── app.py  
├── data/  
│   └── supply_chain_data.csv  
├── src/  
│   ├── data_generator.py  
│   ├── prediction_model.py  
│   └── optimization.py  
├── outputs/  
│   ├── model_results.csv  
│   ├── recommendations.csv  
│   └── xgboost_model.pkl  
├── notebooks/  
├── report/  
├── presentation/  
├── .gitignore  
├── requirements.txt  
└── README.md

## ▶️ Run the Project
Create and activate the virtual environment, install the dependencies, generate the dataset, train the model, generate recommendations, and launch the dashboard:

**python -m venv venv**

**.\venv\Scripts\Activate.ps1**

**pip install -r requirements.txt**

**python src\data_generator.py**

**python src\prediction_model.py**

**python src\optimization.py**

**streamlit run app\app.py**

## 📊 Dashboard
The Streamlit dashboard provides shipment selection, risk analysis, XGBoost prediction, delay probability, predicted delay, recommended actions, decision execution, SQLite write-back, decision history, cost savings, and Decision ROI.

## 📈 Demonstrated Business Result
The completed application demonstrated a high-risk shipment scenario with **100% delay probability**, **14.0 days predicted delay**, three feasible recommendations, successful **Secondary Supplier** decision execution, approximately **$1,063.66 cost savings**, and **14.09% Decision ROI**.

> The supply-chain dataset and actual-outcome calculations are synthetic/simulated and are used for project demonstration.

## 🎓 Project Highlights
This project demonstrates practical implementation of **Machine Learning + Prescriptive Analytics + Mathematical Optimization + Decision Intelligence + Operational Write-Back + ROI Evaluation**.

## 👨‍💻 Supply Prescript
**Closed-Loop Prescriptive Analytics**

**Predict → Optimize → Recommend → Execute → Evaluate → Learn**