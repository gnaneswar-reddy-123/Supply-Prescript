import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Number of shipments
number_of_shipments = 1000

# Generate shipment IDs
shipment_ids = [
    f"SHP-{1000 + i}"
    for i in range(number_of_shipments)
]

# Generate supply-chain data
data = {
    "shipment_id": shipment_ids,

    "supplier_reliability": np.random.uniform(
        0.60, 1.00, number_of_shipments
    ),

    "distance_km": np.random.randint(
        100, 5000, number_of_shipments
    ),

    "order_quantity": np.random.randint(
        50, 1000, number_of_shipments
    ),

    "inventory_level": np.random.randint(
        20, 1000, number_of_shipments
    ),

    "transportation_cost": np.random.uniform(
        1000, 20000, number_of_shipments
    ),

    "weather_risk": np.random.randint(
        0, 4, number_of_shipments
    ),

    "supplier_capacity": np.random.randint(
        500, 5000, number_of_shipments
    ),

    "demand_level": np.random.randint(
        100, 1000, number_of_shipments
    ),

    "historical_delay_days": np.random.randint(
        0, 15, number_of_shipments
    )
}

df = pd.DataFrame(data)

# Create a realistic delay score
delay_score = (
    (1 - df["supplier_reliability"]) * 10
    + (df["distance_km"] / 1000) * 1.5
    + df["weather_risk"] * 2
    + df["historical_delay_days"] * 0.8
    + np.random.normal(0, 1.5, number_of_shipments)
)

# Convert score into predicted/actual delay days
df["delay_days"] = np.maximum(
    0,
    np.round(delay_score)
).astype(int)

# Create delay classification
df["delayed"] = (df["delay_days"] >= 5).astype(int)

# Save dataset
output_file = "data/supply_chain_data.csv"

df.to_csv(output_file, index=False)

print("Dataset created successfully!")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved to: {output_file}")

print("\nFirst 5 records:")
print(df.head())

print("\nDelay statistics:")
print(df["delay_days"].describe())