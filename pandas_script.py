import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

expected_accounts = ["A123", "B456", "C789", "D012"]

# Dataset of actual accounts for each day
data = pd.DataFrame({
    "Date": ["2023-01-01", "2023-01-01", "2023-01-02", "2023-01-02", "2023-01-03"],
    "Account": ["A123", "B456", "A123", "C789", "A123"]  # Missing B456 on 2023-01-02 and others
})

# Convert the Date column to datetime
data["Date"] = pd.to_datetime(data["Date"])

# Create a DataFrame for all expected accounts for each date
all_dates = pd.DataFrame({"Date": pd.date_range(start=data["Date"].min(), end=data["Date"].max(), freq='D')})
all_accounts = pd.DataFrame({"Account": expected_accounts})
all_combinations = all_dates.merge(all_accounts, how='cross')

# Merge with actual data to find missing accounts
merged_data = all_combinations.merge(data, on=["Date", "Account"], how="left", indicator=True)
merged_data["Missing"] = merged_data["_merge"] == "left_only"

# Count missing accounts per date
missing_counts = merged_data[merged_data["Missing"]].groupby("Date").size().reset_index(name='Missing_Count')

# Plotting with Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x="Date", y="Missing_Count", data=missing_counts, palette="viridis")
plt.xlabel("Date")
plt.ylabel("Number of Missing Accounts")
plt.title("Number of Missing Accounts per Day")
plt.xticks(rotation=45)
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()

# Show the plot
plt.show()
