import pandas as pd
import sqlite3
from datetime import datetime

# EXTRACT
df = pd.read_csv("sales_data.csv")

# DATA QUALITY CHECKS

# Remove missing values
df = df.dropna()

# Remove negative quantities
df = df[df["Quantity"] > 0]

# Remove negative prices
df = df[df["Price"] > 0]

# TRANSFORM

# Calculate total sales
df["TotalSales"] = df["Quantity"] * df["Price"]

df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()

# Add ETL run timestamp
df["ETL_Run_Time"] = datetime.now()

# If you have a Date column, uncomment this line:
# df["Month"] = pd.to_datetime(df["Date"]).dt.month_name()

# LOAD TO SQLITE
conn = sqlite3.connect("sales.db")

df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

# VERIFY DATA
result = pd.read_sql(
    "SELECT * FROM sales",
    conn
)

print(result)

# BUSINESS KPIs
print("\nSales Summary")

print("Total Revenue:", df["TotalSales"].sum())

print("Total Orders:", len(df))

print("Average Order Value:",
      round(df["TotalSales"].mean(), 2))

print(df.columns)

conn.close()