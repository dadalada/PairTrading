# Pair Trading Strategy with Machine Learning

## Overview

This project implements a pairs trading strategy that combines:
- **Statistical Cointegration Testing**: Uses Engle-Granger test to identify mean-reverting stock pairs
- **Clustering Analysis**: OPTICS algorithm with partial correlation distance to group similar stocks
- **Machine Learning**: Random Forest classifier to predict entry/exit signals
- **Technical Analysis**: Comprehensive feature engineering using 100+ technical indicators

## Project Structure

```
PairTrading/
│
├── RKDRetriever.py           # Data retrieval from Refinitiv Knowledge Direct API
├── DataProcessor.py          # Data processing and preparation
├── FeatureEngineering.py     # Technical indicator calculation
├── PairsSelection.py         # Pair selection using cointegration and clustering
├── stdout.py                 # Utility functions for file management
├── Interface2ChangeForFinal.ipynb  # Main execution notebook
├── sp500_tickers_RIC.csv     # Stock ticker mappings (required)
├── requirements.txt          # Python dependencies
├── verify_setup.py           # Setup verification script
└── README.md                 # This file
```

## Features

### 1. Data Retrieval (RKDRetriever.py)
- Connects to Refinitiv Knowledge Direct (RKD) API
- Supports both interday and intraday data
- Smart caching system to avoid redundant API calls

### 2. Pairs Selection (PairsSelection.py)
- **Partial Correlation**: Removes market factor influence when measuring stock correlation
- **OPTICS Clustering**: Density-based clustering to group similar stocks
- **Engle-Granger Test**: Statistical cointegration test for pair validation
- **Half-Life Calculation**: Estimates mean-reversion speed using Ornstein-Uhlenbeck process

### 3. Feature Engineering (FeatureEngineering.py)
Technical indicators across multiple categories:
- **Momentum**: RSI, Williams %R, PPO, MACD
- **Volume**: CMF, Force Index, VPT, Volume ratios
- **Trend**: Aroon, CCI, Moving averages
- **Volatility**: Parkinson volatility estimator
- **Microstructure**: Illiquidity measures, spread analysis

### 4. Machine Learning Model
- **Algorithm**: Random Forest Classifier
- **Labels**: Three-class classification (-1: short spread, 0: neutral, 1: long spread)
- **Features**: 100+ technical indicators from both stocks in the pair
- **Validation**: Rolling window out-of-sample testing

### 5. Backtesting System

## Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Configure API credentials**

Edit `RKDRetriever.py` (lines 22-24) with your credentials:
```python
self.username = 'your_email@example.com'
self.password = 'your_password'
self.appid = 'YourApplicationID'
```

3. **Prepare ticker data**

Ensure `sp500_tickers_RIC.csv` exists with the format:
```
Ticker,RIC
AAPL,AAPL.O
MSFT,MSFT.O
...
```

## Usage

### Basic Execution

1. **Configure parameters** (in notebook cell 2):
```python
today = pd.Timestamp('2024-12-31')   # End date
total_months = 36                    # Lookback period
bw = 120                             # Training window (days)
hw = 10                              # Testing window (days)
pvalue_threshold = 0.20              # Cointegration p-value
N_top_pairs = 10                     # Number of pairs to trade
initial_capital = 10000              # Starting capital
```

2. **Run all cells** to execute the full pipeline:

### Module Usage Examples

#### Retrieve Market Data
```python
from RKDRetriever import RKDRetriever

retr = RKDRetriever()
retr.CreateAuthorization()
data, _ = retr.smartRetrieveInterday('.SPX', '2020-01-01T00:00:00', '2023-12-31T23:59:59')
```

#### Select Pairs
```python
from PairsSelection import pairs_selection

pairs = pairs_selection(
    features_train_returns,  # Stock returns DataFrame
    SPX_train_returns,       # Market returns Series
    features_train_close,    # Stock prices DataFrame
    min_sample=2,
    pvalue_threshold=0.20
)
```

#### Calculate Technical Indicators
```python
from FeatureEngineering import FeatureEngineering

fe = FeatureEngineering()
fe.setParams(stock_data, ['RSI', 'MACD', 'CMF'])
fe.process()
features = fe.data
```

## Configuration Parameters

### Trading Parameters
- `bw` (120): Training window size in business days
- `hw` (10): Testing window size in business days
- `lag_days` (1): Holding period for positions
- `vol_thr` (0.7): Volatility threshold multiplier for entry signals
- `window_thr` (10): Rolling window for spread statistics

### Model Parameters
- `n_estimators` (800): Number of trees in Random Forest
- `max_depth` (15): Maximum tree depth
- `class_weight`: Balanced weighting for classes {-1: 1, 0: 1, 1: 1}

### Pair Selection
- `pvalue_threshold` (0.20): Maximum p-value for cointegration test
- `N_top_pairs` (10): Number of pairs to include in portfolio
- `min_sample` (2): Minimum samples for OPTICS clustering

## Output Files

The system generates several output files:

- `data/`: Cached market data (Excel files)
- `portfolio_nav.csv`: Daily portfolio NAV time series
- `all_trades.csv`: Complete trade log with entry/exit details
- `period_summaries.csv`: Rolling window performance summary

