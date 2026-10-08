import streamlit as st
import pandas as pd
import sqlite3
import joblib
from datetime import datetime


# =================================================
# PAGE CONFIGURATION
# =================================================

st.set_page_config(
    page_title="Supply Prescript",
    page_icon="📦",
    layout="wide"
)


# =================================================
# DATABASE
# =================================================

DB_FILE = "outputs/supply_prescript.db"


def create_database():
    conn = sqlite3.connect(DB_FILE)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            decision_id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id TEXT,
            action TEXT,
            predicted_cost REAL,
            actual_cost REAL,
            predicted_delay REAL,
            actual_delay REAL,
            decision_status TEXT,
            roi REAL,
            decision_date TEXT
        )
    """)

    conn.commit()
    conn.close()


create_database()


# =================================================
# LOAD DATA AND MODEL
# =================================================

data = pd.read_csv(
    "data/supply_chain_data.csv"
)

recommendations = pd.read_csv(
    "outputs/recommendations.csv"
)

model = joblib.load(
    "outputs/xgboost_model.pkl"
)


# =================================================
# TITLE
# =================================================

st.title("📦 Supply Prescript")

st.subheader(
    "Closed-Loop Prescriptive Analytics"
)

st.markdown(
    "Predict → Optimize → Recommend → Execute → Evaluate → Learn"
)


# =================================================
# SHIPMENT SELECTION
# =================================================

st.sidebar.header("Shipment Selection")

shipment_ids = data["shipment_id"].tolist()

selected_shipment = st.sidebar.selectbox(
    "Select Shipment",
    shipment_ids
)

shipment = data[
    data["shipment_id"] == selected_shipment
].iloc[0]


# =================================================
# SHIPMENT INFORMATION
# =================================================

st.header("Shipment Risk Analysis")

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Shipment ID",
        shipment["shipment_id"]
    )


with col2:
    st.metric(
        "Supplier Reliability",
        f"{shipment['supplier_reliability']:.2f}"
    )


with col3:
    st.metric(
        "Historical Delay",
        f"{shipment['historical_delay_days']:.1f} days"
    )


with col4:
    st.metric(
        "Transportation Cost",
        f"${shipment['transportation_cost']:,.2f}"
    )


# =================================================
# XGBOOST PREDICTION
# =================================================

st.header("🔮 Prediction")

features = [
    "supplier_reliability",
    "distance_km",
    "order_quantity",
    "inventory_level",
    "transportation_cost",
    "weather_risk",
    "supplier_capacity",
    "demand_level",
    "historical_delay_days"
]

prediction_input = (
    shipment[features]
    .to_frame()
    .T
    .astype(float)
)

risk_score = model.predict_proba(
    prediction_input
)[0][1]

predicted_delay = (
    shipment["historical_delay_days"]
    * (1 + risk_score)
)


col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Delay Probability",
        f"{risk_score:.1%}"
    )

with col2:
    st.metric(
        "Predicted Delay",
        f"{predicted_delay:.1f} days"
    )


# =================================================
# RECOMMENDATIONS
# =================================================

st.header("💡 Recommended Actions")

shipment_recommendations = recommendations.copy()

for column in [
    "cost",
    "delivery_delay_days",
    "recommendation_score"
]:
    shipment_recommendations[column] = pd.to_numeric(
        shipment_recommendations[column],
        errors="coerce"
    )


# Keep only feasible actions
shipment_recommendations = shipment_recommendations[
    shipment_recommendations["feasible"] == True
]


# Sort best recommendation first
shipment_recommendations = shipment_recommendations.sort_values(
    by="recommendation_score",
    ascending=False
)


st.dataframe(
    shipment_recommendations[
        [
            "action",
            "cost",
            "delivery_delay_days",
            "feasible",
            "recommendation_score"
        ]
    ],
    use_container_width=True
)


# =================================================
# EXECUTE DECISION
# =================================================

st.header("🚀 Execute Decision")


if len(shipment_recommendations) > 0:

    selected_action = st.selectbox(
        "Choose an action",
        shipment_recommendations["action"].tolist()
    )

    selected_row = shipment_recommendations[
        shipment_recommendations["action"] == selected_action
    ].iloc[0]


    if st.button(
        "Execute Decision",
        type="primary"
    ):

        # -----------------------------------------
        # PREDICTED VALUES
        # -----------------------------------------

        predicted_cost = float(
            selected_row["cost"]
        )

        predicted_delay_value = float(
            selected_row["delivery_delay_days"]
        )


        # -----------------------------------------
        # SIMULATED ACTUAL OUTCOME
        # -----------------------------------------

        actual_cost = (
            predicted_cost * 1.05
        )

        actual_delay = (
            predicted_delay_value * 1.10
        )


        # -----------------------------------------
        # BASELINE
        # -----------------------------------------

        baseline_cost = (
            float(shipment["transportation_cost"])
            * 1.05
        )

        baseline_delay = (
            float(shipment["historical_delay_days"])
            * 1.10
        )


        # Cost assigned to one day of delay
        DELAY_COST_PER_DAY = 500


        # -----------------------------------------
        # BUSINESS IMPACT
        # -----------------------------------------

        baseline_impact = (
            baseline_cost
            + (
                baseline_delay
                * DELAY_COST_PER_DAY
            )
        )

        decision_impact = (
            actual_cost
            + (
                actual_delay
                * DELAY_COST_PER_DAY
            )
        )


        # -----------------------------------------
        # SAVINGS
        # -----------------------------------------

        cost_savings = (
            baseline_impact
            - decision_impact
        )


        # -----------------------------------------
        # ROI
        # -----------------------------------------

        if decision_impact != 0:

            roi = (
                cost_savings
                / decision_impact
            ) * 100

        else:

            roi = 0


        # -----------------------------------------
        # WRITE TO SQLITE
        # -----------------------------------------

        conn = sqlite3.connect(DB_FILE)

        conn.execute(
            """
            INSERT INTO decisions
            (
                shipment_id,
                action,
                predicted_cost,
                actual_cost,
                predicted_delay,
                actual_delay,
                decision_status,
                roi,
                decision_date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                selected_shipment,
                selected_action,
                predicted_cost,
                actual_cost,
                predicted_delay_value,
                actual_delay,
                "Executed",
                roi,
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
            )
        )

        conn.commit()
        conn.close()


        # -----------------------------------------
        # RESULTS
        # -----------------------------------------

        st.success(
            f"Decision executed: {selected_action}"
        )

        st.info(
            "Decision has been written to the operational database."
        )


        result_col1, result_col2 = st.columns(2)


        with result_col1:

            st.metric(
                "Cost Savings vs Baseline",
                f"${cost_savings:,.2f}"
            )


        with result_col2:

            st.metric(
                "Decision ROI",
                f"{roi:.2f}%"
            )


else:

    st.warning(
        "No feasible recommendations available."
    )


# =================================================
# DECISION HISTORY
# =================================================

st.header("📊 Decision History")

conn = sqlite3.connect(DB_FILE)

history = pd.read_sql_query(
    """
    SELECT *
    FROM decisions
    ORDER BY decision_id DESC
    """,
    conn
)

conn.close()


if len(history) > 0:

    st.dataframe(
        history,
        use_container_width=True
    )


    # ---------------------------------------------
    # AVERAGE ROI
    # ---------------------------------------------

    st.header("📈 Decision ROI")

    average_roi = history["roi"].mean()

    st.metric(
        "Average Decision ROI",
        f"{average_roi:.2f}%"
    )

else:

    st.info(
        "No decisions have been executed yet."
    )


# =================================================
# FOOTER
# =================================================

st.divider()

st.caption(
    "Supply Prescript | Closed-Loop Prescriptive Analytics"
)