import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

# Visual styling setup
sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (14, 8)

# =====================================================================
# DATASET 1: Yahoo Finance (yfinance library ke zariye direct fetch)[cite: 1]
# =====================================================================
print("--- 1. Yahoo Finance Data Analysis ---")
ticker = "AAPL"
start_date = "2023-01-01"
end_date = "2024-01-01"

# Yahoo Finance se data download karna[cite: 1]
df_yf = yf.download(ticker, start=start_date, end=end_date)

# MultiIndex columns handle karna
if isinstance(df_yf.columns, pd.MultiIndex):
    df_yf.columns = df_yf.columns.get_level_values(0)

# Indicators calculate karna: Moving Averages aur Daily Returns[cite: 1]
df_yf["SMA_20"] = df_yf["Close"].rolling(window=20).mean()
df_yf["SMA_50"] = df_yf["Close"].rolling(window=50).mean()
df_yf["Daily_Return"] = df_yf["Close"].pct_change()

print("Yahoo Finance Data (Top 5 rows):")
print(df_yf[["Close", "SMA_20", "SMA_50", "Volume"]].head())

# Visualizing Yahoo Finance Data (Price + Moving Averages + Volume)[cite: 1]
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})

ax1.plot(df_yf.index, df_yf["Close"], label=f"{ticker} Close Price", color="black", linewidth=1.5)
ax1.plot(df_yf.index, df_yf["SMA_20"], label="20-Day SMA", color="blue", linestyle="--")
ax1.plot(df_yf.index, df_yf["SMA_50"], label="50-Day SMA", color="red", linestyle="--")
ax1.set_title(f"Yahoo Finance: {ticker} Price & Moving Averages", fontsize=14, fontweight="bold")
ax1.set_ylabel("Price (USD)")
ax1.legend(loc="upper left")

ax2.bar(df_yf.index, df_yf["Volume"], color="teal", alpha=0.6, label="Volume")
ax2.set_ylabel("Volume")
ax2.set_xlabel("Date")
ax2.legend(loc="upper left")

plt.tight_layout()
plt.show()

# =====================================================================
# DATASET 2: Kaggle Dataset (CSV File se load karna)[cite: 1]
# =====================================================================
print("\n--- 2. Kaggle Dataset Analysis ---")

# Kaggle se download ki hui CSV file ka naam/path yahan dein[cite: 1]
# Agar local file abhi nahi hai, toh testing ke liye ek dummy CSV generate kar rahe hain:
csv_filename = "TSLA.csv"

try:
    df_kaggle = pd.read_csv(csv_filename)
except FileNotFoundError:
    # Testing purpose ke liye sample CSV generate kar rahe hain[cite: 1]
    dates = pd.date_range(start="2023-01-01", periods=100)
    prices = 100 + np.cumsum(np.random.randn(100) * 2) # NumPy calculations[cite: 1]
    sample_df = pd.DataFrame({"Date": dates, "Close": prices, "Volume": np.random.randint(10000, 50000, size=100)})
    sample_df.to_csv(csv_filename, index=False)
    df_kaggle = pd.read_csv(csv_filename)

# Date column ko parse aur index set karna
df_kaggle["Date"] = pd.to_datetime(df_kaggle["Date"])
df_kaggle.set_index("Date", inplace=True)

# Daily return calculation[cite: 1]
df_kaggle["Daily_Return"] = df_kaggle["Close"].pct_change()

print("Kaggle Data (Top 5 rows):")
print(df_kaggle.head())

# Seaborn visualization for Kaggle Data (Returns Distribution)[cite: 1]
plt.figure(figsize=(10, 5))
sns.histplot(df_kaggle["Daily_Return"].dropna(), bins=30, kde=True, color="purple")
plt.title("Kaggle Dataset: Daily Returns Distribution (Seaborn)", fontsize=14, fontweight="bold")
plt.xlabel("Daily Return")
plt.ylabel("Frequency")
plt.tight_layout()
plt.show()

# =====================================================================
# COMPARISON: Dono Datasets ki Volatility Compare Karna[cite: 1]
# =====================================================================
yf_volatility = df_yf["Daily_Return"].std() * np.sqrt(252) # NumPy formula[cite: 1]
kaggle_volatility = df_kaggle["Daily_Return"].std() * np.sqrt(252)

print("\n--- Summary & Comparison ---")
print(f"Yahoo Finance Annualized Volatility: {yf_volatility:.4f}")
print(f"Kaggle Dataset Annualized Volatility: {kaggle_volatility:.4f}")