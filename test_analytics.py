import pandas as pd

# Original DataFrame
data = {
    "Date": ["2023-01-01", "2023-01-03", "2023-01-05"],
    "Value": [10, 20, 15]
}
df = pd.DataFrame(data)

# Convert 'Date' column to datetime
df["Date"] = pd.to_datetime(df["Date"])

# Get the start (Monday) and end (Sunday) of the current week
current_date = pd.Timestamp.now()  # Today's date
start_of_week = current_date - pd.Timedelta(days=current_date.weekday())  # Monday
end_of_week = start_of_week + pd.Timedelta(days=6)  # Sunday

# Generate full date range for the current week
current_week_dates = pd.date_range(start=start_of_week, end=end_of_week)

# Reindex the DataFrame to include all dates for the current week
df = df.set_index("Date").reindex(current_week_dates, fill_value=0)

# Reset the index and rename the index column back to 'Date'
df = df.reset_index().rename(columns={"index": "Date"})

# Output the resulting DataFrame
print(df)
