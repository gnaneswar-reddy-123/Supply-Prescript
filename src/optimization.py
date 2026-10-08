import pandas as pd
from scipy.optimize import linprog


# Load dataset
data_file = "data/supply_chain_data.csv"
df = pd.read_csv(data_file)

print("Dataset loaded successfully!")


# Select one shipment for optimization
shipment = df.iloc[0]

shipment_id = shipment["shipment_id"]
transportation_cost = shipment["transportation_cost"]
historical_delay = shipment["historical_delay_days"]


print("\n--------------------------------")
print("SHIPMENT INFORMATION")
print("--------------------------------")

print("Shipment ID:", shipment_id)
print("Transportation Cost:", transportation_cost)
print("Historical Delay:", historical_delay)


# -------------------------------------------------
# BUSINESS CONSTRAINTS
# -------------------------------------------------

MAX_BUDGET = 20000
MAX_DELAY = 20


# -------------------------------------------------
# THREE ALTERNATIVE ACTIONS
# -------------------------------------------------

actions = [
    {
        "action": "Air Freight",
        "cost": transportation_cost * 2.5,
        "delay_days": max(1, historical_delay * 0.3),
        "capacity": 1
    },
    {
        "action": "Secondary Supplier",
        "cost": transportation_cost * 1.10,
        "delay_days": max(2, historical_delay * 0.6),
        "capacity": 1
    },
    {
        "action": "Standard Shipping",
        "cost": transportation_cost,
        "delay_days": historical_delay,
        "capacity": 1
    }
]


# -------------------------------------------------
# OPTIMIZATION
# -------------------------------------------------

# Objective:
# Minimize total cost

costs = [action["cost"] for action in actions]

# One action must be selected
A_eq = [[1, 1, 1]]
b_eq = [1]

# Every action is either selected or not selected
bounds = [
    (0, 1),
    (0, 1),
    (0, 1)
]


result = linprog(
    c=costs,
    A_eq=A_eq,
    b_eq=b_eq,
    bounds=bounds,
    method="highs"
)


# -------------------------------------------------
# CREATE RECOMMENDATIONS
# -------------------------------------------------

recommendations = []

for action in actions:

    feasible = (
        action["cost"] <= MAX_BUDGET
        and action["delay_days"] <= MAX_DELAY
    )

    # Recommendation score
    score = (
        (MAX_BUDGET - action["cost"]) / MAX_BUDGET * 50
        +
        (MAX_DELAY - action["delay_days"]) / MAX_DELAY * 50
    )

    recommendations.append({
        "shipment_id": shipment_id,
        "action": action["action"],
        "cost": round(action["cost"], 2),
        "delivery_delay_days": round(action["delay_days"], 2),
        "feasible": feasible,
        "recommendation_score": round(score, 2)
    })


# Convert to DataFrame
recommendations_df = pd.DataFrame(recommendations)


# Sort best recommendation first
recommendations_df = recommendations_df.sort_values(
    by="recommendation_score",
    ascending=False
)


# -------------------------------------------------
# SAVE RESULTS
# -------------------------------------------------

output_file = "outputs/recommendations.csv"

recommendations_df.to_csv(
    output_file,
    index=False
)


# -------------------------------------------------
# DISPLAY RESULTS
# -------------------------------------------------

print("\n--------------------------------")
print("OPTIMIZATION RESULTS")
print("--------------------------------")

print(
    recommendations_df.to_string(index=False)
)

print("\n--------------------------------")

if result.success:
    print("Optimization completed successfully!")
else:
    print("Optimization could not find a solution.")

print(f"Recommendations saved to: {output_file}")

print("--------------------------------")