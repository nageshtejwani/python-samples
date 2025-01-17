import pandas as pd

# Original DataFrame
data = {
    "Date": ["2023-01-01", "2023-01-03", "2023-01-04"],
    "Value": [10, 20, 15]
}
df = pd.DataFrame(data)

# Convert 'Date' column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Get the latest date in the current DataFrame
latest_date = df["Date"].max()

# Generate the next 10 days from the latest date
next_10_days = pd.date_range(start=latest_date + pd.Timedelta(days=1), periods=10, freq='D')

# Create a DataFrame for the next 10 days with dummy value
dummy_data = pd.DataFrame({"Date": next_10_days, "Value": [0] * 10})

# Concatenate the new dummy data to the original DataFrame
df = pd.concat([df, dummy_data], ignore_index=True)

# Output the resulting DataFrame
print(df)
