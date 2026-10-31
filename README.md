# Stock Analyzer

A compact Python script for exploratory analysis of stock price data. It loads price history from **two different sources** (live from Yahoo Finance and from a local Kaggle-style CSV file), computes common technical indicators, draws charts, and compares the **annualized volatility** of the two datasets.

It is a good starter project for learning how `pandas`, `NumPy`, `matplotlib`, `seaborn` and `yfinance` fit together in a basic financial-data workflow.

> **Disclaimer:** This project is for learning and exploration only. It is not financial advice and should not be used on its own to make investment decisions.

---

## Table of Contents

1. [Features](#features)
2. [Project Structure](#project-structure)
3. [Requirements and Installation](#requirements-and-installation)
4. [Quick Start](#quick-start)
5. [The Data](#the-data)
6. [How the Code Works](#how-the-code-works)
7. [Metrics and Formulas](#metrics-and-formulas)
8. [Output](#output)
9. [Configuration and Customization](#configuration-and-customization)
10. [Known Limitations](#known-limitations)
11. [Troubleshooting](#troubleshooting)
12. [Possible Improvements](#possible-improvements)
13. [License](#license)

---

## Features

- **Live market data**: downloads daily OHLCV data for a ticker (default `AAPL`) through the `yfinance` library.
- **Local CSV analysis**: loads `TSLA.csv`, a daily price history for Tesla.
- **Technical indicators**: 20-day and 50-day Simple Moving Averages (SMA) and daily percentage returns.
- **Visualizations**:
  - Price chart with SMA 20 / SMA 50 overlays and a volume bar panel (matplotlib).
  - Histogram of daily returns with a KDE curve (seaborn).
- **Risk comparison**: annualized volatility for both datasets, printed side by side.
- **Self-healing demo mode**: if the CSV is missing, the script generates a random sample file so it can still run (see [Known Limitations](#known-limitations) before relying on this).

---

## Project Structure

```
Stock_Analyzer/
├── stock_analysis.py   # The whole analysis pipeline (single script, ~100 lines)
├── TSLA.csv            # Tesla daily price history (639 rows, Sep 2019 to Apr 2022)
└── README.md           # This file
```

There is no package, no configuration file and no test suite. Everything lives in `stock_analysis.py` and runs top to bottom.

---

## Requirements and Installation

**Python:** 3.9 or newer is recommended. The script was run successfully on Python 3.13 with `yfinance` 1.7.0.

**Libraries:**

| Library      | Used for                                                   |
|--------------|------------------------------------------------------------|
| `pandas`     | DataFrames, CSV loading, rolling windows, `pct_change()`   |
| `numpy`      | Square root for annualization, random sample generation    |
| `matplotlib` | Price/volume figure and figure layout                      |
| `seaborn`    | Theme and the returns histogram with KDE                   |
| `yfinance`   | Downloading historical data from Yahoo Finance             |

**Install:**

```bash
# 1. Clone the repository
git clone https://github.com/korichirag-arch/Stock_Analyzer.git
cd Stock_Analyzer

# 2. (Recommended) create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install numpy pandas matplotlib seaborn yfinance
```

The repository does not ship a `requirements.txt`. If you want one, create it with the five package names above.

---

## Quick Start

```bash
python stock_analysis.py
```

Run it from the repository folder so that `TSLA.csv` is found. The script will:

1. Print a header and download AAPL data (internet connection required).
2. Print the first 5 rows of the indicator table.
3. Open the **price + moving averages + volume** chart. **Close the window to continue**, because `plt.show()` blocks execution.
4. Load `TSLA.csv`, print its first 5 rows, and open the **daily returns histogram**. Close it to continue.
5. Print the volatility comparison.

On a server or any machine without a display, run it with a non-interactive backend so that `plt.show()` does not block:

```bash
MPLBACKEND=Agg python stock_analysis.py
```

---

## The Data

### Dataset 1: Yahoo Finance (live)

| Setting      | Value                     |
|--------------|---------------------------|
| Ticker       | `AAPL` (Apple Inc.)       |
| Start date   | `2023-01-01`              |
| End date     | `2024-01-01` (exclusive)  |
| Frequency    | Daily                     |

Fetched at run time with `yf.download(...)`. The result contains `Open`, `High`, `Low`, `Close` and `Volume`. Note that `yfinance` adjusts prices by default in recent versions, so `Close` is already split/dividend adjusted.

### Dataset 2: `TSLA.csv` (local, Kaggle style)

| Property     | Value                                                      |
|--------------|------------------------------------------------------------|
| Rows         | 639 trading days                                           |
| Date range   | 2019-09-30 to 2022-04-11                                   |
| Columns      | `Date, High, Low, Open, Close, Volume, Adj Close`          |
| Missing data | None (0 null values in every column)                       |
| Duplicates   | None; dates are sorted ascending                           |
| Price range  | Close from about 46.29 to about 1229.91                    |

Notes about this file:

- `Adj Close` is identical to `Close` in every row, so it adds no extra information.
- The prices look adjusted for Tesla's 2020 stock split but not for the 2022 split, which happened after the last date in the file. Keep this in mind when comparing levels with other sources.

---

## How the Code Works

`stock_analysis.py` is organized into three labelled blocks.

### 0. Setup (lines 1 to 9)

- Imports `numpy`, `pandas`, `matplotlib.pyplot`, `seaborn`, `yfinance`.
- Applies the seaborn `whitegrid` theme and sets the default figure size to 14 x 8 inches.

### 1. Dataset 1: Yahoo Finance (lines 11 to 50)

1. Defines `ticker`, `start_date`, `end_date`.
2. Downloads data with `yf.download(...)` into `df_yf`.
3. **Flattens MultiIndex columns.** Newer `yfinance` versions return columns like `("Close", "AAPL")`. The script keeps only the first level so you can write `df_yf["Close"]`.
4. Adds three columns:
   - `SMA_20`: 20-day rolling mean of `Close`
   - `SMA_50`: 50-day rolling mean of `Close`
   - `Daily_Return`: day-over-day percentage change of `Close`
5. Prints the first 5 rows of `Close`, `SMA_20`, `SMA_50`, `Volume`. The first rows of the SMA columns show `NaN` because the rolling window is not yet full.
6. Draws a 2-row figure that shares the x-axis, with height ratio 3:1:
   - **Top:** black close-price line, blue dashed SMA 20, red dashed SMA 50.
   - **Bottom:** teal volume bars.

### 2. Dataset 2: Kaggle CSV (lines 52 to 88)

1. Tries to read `TSLA.csv` into `df_kaggle`.
2. **If the file is not found**, it generates a 100-day synthetic dataset (a random walk starting near 100 plus random volume), saves it as `TSLA.csv`, and loads it. This is a convenience for testing only.
3. Converts the `Date` column to `datetime` and sets it as the index.
4. Adds `Daily_Return` (percentage change of `Close`).
5. Prints the first 5 rows.
6. Plots a seaborn histogram of `Daily_Return` with 30 bins and a KDE curve (purple).

### 3. Comparison (lines 90 to 98)

Computes annualized volatility for both datasets and prints them:

```python
yf_volatility     = df_yf["Daily_Return"].std() * np.sqrt(252)
kaggle_volatility = df_kaggle["Daily_Return"].std() * np.sqrt(252)
```

---

## Metrics and Formulas

| Metric | Definition | In the code |
|--------|------------|-------------|
| **Simple Moving Average (SMA)** | Mean of the last *N* closing prices. Smooths short-term noise. | `Close.rolling(window=N).mean()` |
| **Daily Return** | `(P_t / P_(t-1)) - 1`, the percentage change from the previous close. | `Close.pct_change()` |
| **Annualized Volatility** | `std(daily returns) x sqrt(252)`. 252 is the typical number of trading days in a year. A higher value means larger price swings. | `.std() * np.sqrt(252)` |

How to read the charts:

- **Price above both SMAs** usually signals an uptrend. **Price below both** usually signals a downtrend.
- **SMA 20 crossing above SMA 50** is a common (but not reliable on its own) bullish signal, often called a "golden cross" when it happens on the 50/200 pair. **Crossing below** is the bearish counterpart.
- A **wide, fat-tailed returns histogram** means the stock has frequent large moves.

---

## Output

### Console

```
--- 1. Yahoo Finance Data Analysis ---
Yahoo Finance Data (Top 5 rows):
   Close  SMA_20  SMA_50  Volume
   ...

--- 2. Kaggle Dataset Analysis ---
Kaggle Data (Top 5 rows):
   High  Low  ...  Adj Close  Daily_Return
   ...

--- Summary & Comparison ---
Yahoo Finance Annualized Volatility: <value for AAPL, 2023>
Kaggle Dataset Annualized Volatility: 0.7173
```

The Kaggle value above (**0.7173**, about 71.7% annualized) was computed from the included `TSLA.csv`. The Yahoo value depends on live data at run time.

### Charts

1. **Yahoo Finance: AAPL Price & Moving Averages**, with a volume panel underneath.
2. **Kaggle Dataset: Daily Returns Distribution (Seaborn)** for TSLA.

Charts are only displayed, not saved. To save them, add `plt.savefig("name.png", dpi=150)` before each `plt.show()`.

### Notable facts from the TSLA data

- Mean daily return is about 0.57% with a standard deviation of about 4.52%.
- The largest one-day gain was about +19.9% (2020-02-03) and the largest one-day drop about -21.1% (2020-09-08).

---

## Configuration and Customization

All settings are plain variables near the top of each block. There is no CLI or config file.

| What to change      | Where                          | Example                              |
|---------------------|--------------------------------|--------------------------------------|
| Stock ticker        | `ticker = "AAPL"`              | `ticker = "MSFT"`                    |
| Date range          | `start_date`, `end_date`       | `"2022-01-01"` to `"2025-01-01"`     |
| SMA windows         | `rolling(window=20)` / `50`    | `window=10`, `window=200`            |
| CSV file            | `csv_filename = "TSLA.csv"`    | `"my_data.csv"`                      |
| Histogram bins      | `bins=30`                      | `bins=50`                            |
| Chart size / theme  | lines 8 and 9                  | `figsize=(12, 6)`                    |

**Using your own CSV:** it needs at least a `Date` column and a `Close` column. A `Volume` column is only needed if you extend the script to plot it. Dates should be parseable by `pd.to_datetime`, and rows should be in chronological order, because `pct_change()` compares each row to the previous one.

---

## Known Limitations

These are things the code does today that are worth knowing about before you build on it.

1. **Silent failure when Yahoo Finance is unreachable.** If the download fails (no internet, blocked network, rate limit), `yfinance` prints an error but returns an empty table. The script does not stop. It prints an empty DataFrame and reports the Yahoo volatility as `nan`.
2. **The fallback can overwrite your data file.** If `TSLA.csv` is missing, the script writes random sample data to that same filename. Do not mistake that file for real Tesla prices.
3. **The volatility comparison is not like for like.** It compares AAPL over calendar 2023 against TSLA over 2019 to 2022. Different companies and very different time windows (and market regimes) are being compared, so the numbers are not directly comparable.
4. **Indicators differ between the datasets.** SMAs and the price chart are only produced for the Yahoo data. The CSV data only gets daily returns and a histogram.
5. **Charts block execution** because `plt.show()` waits for the window to close. Use `MPLBACKEND=Agg` for unattended runs.
6. **Hardcoded settings and a single script.** There are no functions, no `if __name__ == "__main__":` guard, no CLI arguments, no tests and no `requirements.txt`.
7. **Cosmetic leftovers in comments.** Some comments contain stray `[cite: 1]` markers and are written in Hinglish. They do not affect behaviour.
8. **Estimates, not forecasts.** Volatility and moving averages describe the past only.

---

## Troubleshooting

| Problem | Likely cause and fix |
|---------|----------------------|
| `ModuleNotFoundError: No module named 'yfinance'` (or another library) | Run `pip install numpy pandas matplotlib seaborn yfinance`. |
| Yahoo volatility prints `nan` and the table is empty | The download failed. Check your internet connection, try again later, or try a different date range. A network that blocks Yahoo will always produce this. |
| Script seems to hang after printing a table | A chart window is open (possibly behind other windows). Close it to continue, or use `MPLBACKEND=Agg`. |
| `KeyError: 'Close'` | The column layout of the downloaded data changed. Print `df_yf.columns` to inspect it. The MultiIndex-flattening step is meant to handle the common case. |
| `TSLA.csv` looks like random data starting near 100 | The original file was missing and the fallback generator replaced it. Restore the real file with `git checkout TSLA.csv`. |
| No window appears on a headless server | Set `MPLBACKEND=Agg` and add `plt.savefig(...)` calls to write images to disk. |

---

## Possible Improvements

- Wrap the logic in functions (`load_yahoo`, `load_csv`, `add_indicators`, `plot_...`) and add a `main()` guard.
- Accept ticker, dates and CSV path as command-line arguments (`argparse`).
- Fail loudly when a download returns no rows instead of continuing with `nan`.
- Remove the dummy-data fallback, or write it to a different filename.
- Compare both assets over the **same** date range for a fair volatility comparison.
- Add more indicators: RSI, MACD, Bollinger Bands, rolling volatility, max drawdown, Sharpe ratio.
- Add SMA and volume charts for the CSV dataset too.
- Save charts to a `plots/` folder and add a `requirements.txt`.
- Add unit tests for the indicator calculations.

---

## License

No license file is included in this repository yet. Add one (for example MIT) if you want others to reuse the code.
