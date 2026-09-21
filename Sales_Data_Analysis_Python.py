import pandas as pd
import matplotlib.pyplot as plt

# Load raw sales data
df = pd.read_csv("Python_Sales_Analysis_Raw_Data.csv")

# -----------------------------
# Data quality checks
# -----------------------------
missing_values = df.isna().sum()
duplicate_order_ids = df.duplicated(subset="Order_ID").sum()

print("Missing values by column:")
print(missing_values)
print(f"Duplicate Order_IDs: {duplicate_order_ids}")

# -----------------------------
# Data cleaning
# -----------------------------
df["Region"] = df["Region"].fillna("Unknown")
df["Sales_Rep"] = df["Sales_Rep"].fillna("Unassigned")
df = df.drop_duplicates(subset="Order_ID", keep="first")

# Recalculate business metrics
df["Sales"] = df["Quantity"] * df["Unit_Price"]
df["Profit"] = df["Sales"] - df["Cost"]
df["Profit_Margin"] = df["Profit"] / df["Sales"] * 100

# -----------------------------
# Exploratory analysis
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])
monthly_sales = df.groupby(df["Date"].dt.to_period("M"))["Sales"].sum()
category_sales = df.groupby("Category")["Sales"].sum()
region_profit = df.groupby("Region")["Profit"].sum()

print("\nTop sales categories:")
print(category_sales.sort_values(ascending=False))

print("\nProfit by region:")
print(region_profit.sort_values(ascending=False))

# -----------------------------
# Visualization
# -----------------------------

# =========================
# DASHBOARD
# =========================

fig = plt.figure(figsize=(16, 10))
fig.suptitle("Sales Data Analysis Dashboard", fontsize=22, fontweight="bold")

# KPI 1 - Total Sales
ax1 = plt.subplot(2, 3, 1)
ax1.axis("off")
ax1.text(0.5, 0.55, f"C$ {df['Sales'].sum():,.2f}",
         ha="center", va="center", fontsize=24, fontweight="bold")
ax1.text(0.5, 0.25, "TOTAL SALES",
         ha="center", fontsize=12)

# KPI 2 - Total Profit
ax2 = plt.subplot(2, 3, 2)
ax2.axis("off")
ax2.text(0.5, 0.55, f"C$ {df['Profit'].sum():,.2f}",
         ha="center", va="center", fontsize=24, fontweight="bold")
ax2.text(0.5, 0.25, "TOTAL PROFIT",
         ha="center", fontsize=12)

# KPI 3 - Orders
ax3 = plt.subplot(2, 3, 3)
ax3.axis("off")
ax3.text(0.5, 0.55, f"{df['Order_ID'].nunique():,}",
         ha="center", va="center", fontsize=24, fontweight="bold")
ax3.text(0.5, 0.25, "TOTAL ORDERS",
         ha="center", fontsize=12)

# KPI 4 - Profit Margin
ax4 = plt.subplot(2, 3, 4)
ax4.axis("off")

profit_margin = df["Profit"].sum() / df["Sales"].sum() * 100

ax4.text(0.5, 0.55, f"{profit_margin:.1f}%",
         ha="center", va="center", fontsize=24, fontweight="bold")
ax4.text(0.5, 0.25, "PROFIT MARGIN",
         ha="center", fontsize=12)

# Sales by Category
ax5 = plt.subplot(2, 3, 5)

category_sales = df.groupby("Category")["Sales"].sum().sort_values(
    ascending=False
)

ax5.bar(category_sales.index, category_sales.values)
ax5.set_title("Sales by Category")
ax5.set_ylabel("Sales (CAD)")
ax5.tick_params(axis="x", rotation=30)

# Profit by Region
ax6 = plt.subplot(2, 3, 6)

region_profit = df.groupby("Region")["Profit"].sum().sort_values(
    ascending=False
)

ax6.bar(region_profit.index, region_profit.values)
ax6.set_title("Profit by Region")
ax6.set_ylabel("Profit (CAD)")
ax6.tick_params(axis="x", rotation=30)

plt.tight_layout()
plt.show()
