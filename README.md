# Stock Market Analysis

## Project Overview
This project performs exploratory data analysis and trend identification on historical stock market data. It analyzes price movements, trading volumes, and returns using technical indicators like Simple Moving Averages (SMA) and rolling volatility. The project incorporates two distinct data sources: real-time/historical feeds from Yahoo Finance and local historical records from Kaggle.

---

## Datasets

1. **Yahoo Finance API (`yfinance`)**
   - Source: Directly retrieved using the `yfinance` Python library.
   - Asset: Apple Inc. (Ticker: `AAPL`).
   - Period: January 1, 2023 to January 1, 2024.
   - Attributes: Date, Open, High, Low, Close, Adj Close, Volume.

2. **Kaggle Historical Stock Dataset**
   - Source: Kaggle Stock Market Datasets.
   - File: `TSLA.csv` (Tesla, Inc. historical trading records).
   - Attributes: Date, Close, Volume, and related pricing attributes.

---

## Tools and Libraries

- **Python 3.x**: Primary execution runtime.
- **Pandas**: Data manipulation, cleaning, time-series indexing, and rolling window operations.
- **NumPy**: Numerical operations, logarithmic returns, and annualized volatility estimation.
- **Matplotlib**: Primary figure generation and multi-panel chart layouts.
- **Seaborn**: Statistical distributions, probability density estimation, and theme formatting.
- **yfinance**: Automated data fetching from the Yahoo Finance API.

---

## Technical Indicators and Methodologies

- **Simple Moving Averages (SMA)**:
  - 20-Day SMA: Captures short-term trends and momentum shifts.
  - 50-Day SMA: Identifies medium-term market trajectory.
- **Daily Returns**:
  - Computed via percentage change in closing prices to evaluate day-to-day fluctuations.
- **Annualized Volatility**:
  - Derived by scaling the standard deviation of daily returns across 252 trading days.
- **Volume Correlation**:
  - Secondary subplot overlay to analyze trading activity across price swings.

---

## Assumptions

1. **Trading Days per Year**: The standard convention of 252 annual trading days is used for volatility annualization.
2. **Missing Values**: Missing records and NaN values created during rolling calculations are dropped for statistical distribution plots.
3. **Data Uniformity**: It is assumed that both data sources adhere to standard exchange trading schedules and calendar configurations.

---

## Project Structure

```text
├── stock_analysis.py       # Main Python script with data processing and plots
├── TSLA.csv                # Kaggle dataset for Tesla historical prices
├── README.md               # Project documentation and setup guide
└── requirements.txt        # Python package dependencies

[Chirag Kori]
