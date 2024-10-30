import pandas as pd

# Load data
df = pd.read_csv("sales_data.csv")

# Calculate total sales for each row
df["total_sales"] = df["price"] * df["quantity"]

# Group by region and calculate total sales for each region
region_sales = df.groupby("region")["total_sales"].sum().reset_index()

# Calculate average price per unit for each product_id
df["average_price_per_unit"] = df.groupby("product_id")["price"].transform("mean")

# Filter dataset to include only rows where total sales exceed ₹10,000
filtered_df = df[df["total_sales"] > 10000]

print("Total Sales by Region:")
print(region_sales)

print("\nFiltered Data (Total Sales > ₹10,000):")
print(filtered_df)
