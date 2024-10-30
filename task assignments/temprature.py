import pandas as pd
import matplotlib.pyplot as plt

# Load data with error handling
try:
    df = pd.read_csv("temperature_data.csv", parse_dates=["date"])
except FileNotFoundError:
    print("Error: The file 'temperature_data.csv' was not found.")
    exit()

# Ensure the DataFrame has the necessary columns
if "date" not in df.columns or "temperature" not in df.columns:
    print("Error: The DataFrame must contain 'date' and 'temperature' columns.")
    exit()

# Plot setup
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df["date"], df["temperature"], marker='o', color='b', linestyle='-', label="Temperature")

# Labels and title
ax.set_xlabel("Date")
ax.set_ylabel("Temperature (°C)")
ax.set_title("Daily Temperature Variations")

# Find the max and min temperatures and dates in one pass
max_row = df.loc[df["temperature"].idxmax()]
min_row = df.loc[df["temperature"].idxmin()]
max_temp, max_date = max_row["temperature"], max_row["date"]
min_temp, min_date = min_row["temperature"], min_row["date"]

# Annotations for max and min temperatures with dynamic positioning
ax.annotate(f"{max_temp}°C on {max_date.date()}", xy=(max_date, max_temp), xytext=(max_date, max_temp + 2),
            arrowprops=dict(facecolor='green', arrowstyle="->"), color='green', ha='center')
ax.annotate(f"{min_temp}°C on {min_date.date()}", xy=(min_date, min_temp), xytext=(min_date, min_temp - 2),
            arrowprops=dict(facecolor='red', arrowstyle="->"), color='red', ha='center')

# Grid and show plot
ax.grid(True)
plt.show()
