
# 1. Load the cleaned data

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/processed/clean_sales.csv")

# Convert columns into date format
df["order_date"] = pd.to_datetime(df["order_date"])
df["month_start"] = pd.to_datetime(df["month_start"])

print(df.head())


# 2. Check data size, column types, and missing values

print("Number of rows and columns:")
print(df.shape)

print("Column information:")
df.info()

print("Missing values:")
print(df.isna().sum())


# 3. Display summary statistics

print("Summary statistics:")
print(df[["quantity", "unit_price", "revenue"]].describe())


# 4. Calculate and display monthly revenue

monthly = df.groupby("month_start")["revenue"].sum()

print("Monthly revenue:")
print(monthly)

monthly.plot(figsize=(10, 4), title="Monthly Revenue")

plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()


# 5. Find the best products, categories, and regions

print("Top 10 products by revenue:")

product_sales = df.groupby("product")["revenue"].sum()
product_sales = product_sales.sort_values(ascending=False)

print(product_sales.head(10))


print("Revenue by category:")

category_sales = df.groupby("category")["revenue"].sum()
category_sales = category_sales.sort_values(ascending=False)

print(category_sales)


print("Revenue by region:")

region_sales = df.groupby("region")["revenue"].sum()
region_sales = region_sales.sort_values(ascending=False)

print(region_sales)


# 6. Find the strongest months of the year

year_month_sales = df.groupby(["year", "month"])["revenue"].sum()

monthly_average = year_month_sales.groupby("month").mean()

print("Average revenue for each month:")
print(monthly_average.round(0))


# 7. Understand customer behaviour

# Calculate revenue for each order
orders = df.groupby("order_id")["revenue"].sum()

average_order_value = orders.mean()

print("Average order value:", round(average_order_value, 2))


# Count orders for each customer
customer_orders = df.groupby("customer_id")["order_id"].nunique()

# Find customers who placed 2 or more orders
repeat_customers = customer_orders[customer_orders >= 2]

print(
    "Repeat customers:",
    len(repeat_customers),
    "out of",
    len(customer_orders)
)


# 8. Check the relationship between price, quantity, and revenue

correlation = df[["quantity", "unit_price", "revenue"]].corr()

print("Correlation between columns:")
print(correlation.round(2))
