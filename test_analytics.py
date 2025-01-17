import pandas as pd

# Original DataFrame
data = {
    "Date": ["2023-01-01", "2023-01-03", "2023-01-04"],
    "Value": [10, 20, 15]
}
df = pd.DataFrame(data)

# Convert 'Date' column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Calculate yesterday's date
yesterdays_date = pd.Timestamp.now().normalize() - pd.Timedelta(days=1)

# Check if yesterday's date already exists to avoid duplicates
if yesterdays_date not in df["Date"].values:
    # Create a new row for yesterday with Value = 0
    dummy_row = pd.DataFrame({"Date": [yesterdays_date], "Value": [0]})

    # Append the dummy row to the existing DataFrame
    df = pd.concat([df, dummy_row], ignore_index=True)

# Sort the DataFrame by date
df = df.sort_values(by="Date").reset_index(drop=True)

# Output the resulting DataFrame
print(df)
