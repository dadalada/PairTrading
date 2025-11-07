# Pair Trading Strategy with Machine Learning

## Overview

This project implements a pairs trading strategy that combines:
- **Statistical Cointegration Testing**: Uses Engle-Granger test to identify mean-reverting stock pairs
- **Clustering Analysis**: OPTICS algorithm with partial correlation distance to group similar stocks
- **Machine Learning**: Random Forest classifier to predict entry/exit signals
- **Technical Analysis**: Comprehensive feature engineering using 100+ technical indicators
- **Risk Management**: Rolling window backtesting with configurable parameters

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
- Automatic data validation and storage

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
- **Algorithm**: Random Forest Classifier (800 trees, max depth 15)
- **Labels**: Three-class classification (-1: short spread, 0: neutral, 1: long spread)
- **Features**: 100+ technical indicators from both stocks in the pair
- **Validation**: Rolling window out-of-sample testing

### 5. Backtesting System
- Walk-forward analysis with configurable training/testing windows
- Position sizing based on capital allocation
- Transaction cost modeling using VWAP execution
- Multiple pairs portfolio management
- Performance metrics: Sharpe ratio, max drawdown, annualized returns

## Installation

### Prerequisites
- Python 3.8 or higher
- Valid Refinitiv Knowledge Direct API credentials

### Setup Steps

1. **Clone the repository**
```bash
git clone <repository-url>
cd PairTrading
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

To verify your installation, run:
```bash
python3 verify_setup.py
```

This will check if all dependencies are installed and all required files are present.

3. **Configure API credentials**

Edit `RKDRetriever.py` (lines 22-24) with your credentials:
```python
self.username = 'your_email@example.com'
self.password = 'your_password'
self.appid = 'YourApplicationID'
```

⚠️ **Security Note**: For production use, store credentials in environment variables or a secure configuration file, not in the source code.

4. **Prepare ticker data**

Ensure `sp500_tickers_RIC.csv` exists with the format:
```
Ticker,RIC
AAPL,AAPL.O
MSFT,MSFT.O
...
```

## Usage

### Basic Execution

1. **Open the main notebook**
```bash
jupyter notebook Interface2ChangeForFinal.ipynb
```

2. **Configure parameters** (in notebook cell 2):
```python
today = pd.Timestamp('2024-12-31')  # End date
total_months = 36                    # Lookback period
bw = 120                             # Training window (days)
hw = 10                              # Testing window (days)
pvalue_threshold = 0.20              # Cointegration p-value
N_top_pairs = 10                     # Number of pairs to trade
initial_capital = 10000              # Starting capital
```

3. **Run all cells** to execute the full pipeline:
   - Data retrieval
   - Pair selection
   - Feature engineering
   - Model training
   - Backtesting
   - Performance visualization

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

## Performance Metrics

The system calculates and displays:
- **Annualized Return**: Compound annual growth rate
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Sharpe Ratio**: Risk-adjusted return metric
- **Classification Metrics**: Precision, recall, F1-score for ML model
- **Benchmark Comparison**: Strategy vs. S&P 500 performance

## Algorithm Workflow

1. **Data Collection**: Retrieve historical price data for stock universe
2. **Pair Formation**:
   - Calculate partial correlations (removing market factor)
   - Cluster stocks using OPTICS algorithm
   - Test pairs within clusters for cointegration
   - Estimate hedge ratios and half-lives
3. **Feature Engineering**:
   - Compute 100+ technical indicators for each stock
   - Calculate spread characteristics
   - Label training data based on spread returns
4. **Model Training**:
   - Train Random Forest on historical features
   - Predict entry/exit signals for test period
5. **Backtesting**:
   - Execute trades based on model predictions
   - Track positions and calculate P&L
   - Roll forward to next window
6. **Performance Analysis**:
   - Aggregate results across all windows
   - Calculate risk metrics
   - Generate visualizations

## Important Notes

### Data Requirements
- Minimum 3+ years of historical data recommended
- Daily OHLCV data required for all stocks
- Market index data (S&P 500) required for factor adjustment

### Computational Considerations
- Processing time scales with universe size and date range
- First run will download all data (cached for subsequent runs)
- Parallel processing not implemented (potential optimization)

### Risk Warnings
- **Past performance does not guarantee future results**
- Transaction costs and slippage not fully modeled
- Market regime changes can invalidate statistical relationships
- Model requires periodic retraining
- API rate limits may affect data retrieval

## Troubleshooting

### Common Issues

**"Authentication failed"**
- Verify API credentials are correct
- Check if API subscription is active
- Ensure network connectivity to Refinitiv servers

**"No row field, indicating that there may be no data for this period"**
- Stock may have been delisted or not traded during the period
- Verify RIC (Reuters Instrument Code) is correct
- Check date range is valid

**"Skip [RIC]: Lack of columns"**
- Data quality issue for specific stock
- Stock automatically excluded from analysis

**Memory errors**
- Reduce date range or universe size
- Use more powerful machine
- Implement data chunking (requires code modification)

## Extensions and Future Work

Potential improvements:
- **Real-time trading**: Adapt for live market data
- **Alternative ML models**: Neural networks, gradient boosting
- **Transaction cost modeling**: More realistic slippage and commissions
- **Multi-asset pairs**: Extend beyond equities (futures, forex, crypto)
- **Regime detection**: Adaptive parameters based on market conditions
- **Portfolio optimization**: Better capital allocation across pairs
- **Risk management**: Stop-loss, position limits, correlation constraints

## Dependencies

See `requirements.txt` for complete list. Key packages:
- `pandas`: Data manipulation
- `numpy`: Numerical computing
- `scikit-learn`: Machine learning
- `statsmodels`: Statistical tests
- `ta`: Technical analysis indicators
- `matplotlib/seaborn`: Visualization

