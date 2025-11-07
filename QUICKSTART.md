# Quick Start Guide

Get up and running in 5 minutes.

## Prerequisites

- Python 3.8+
- Refinitiv API credentials ([Get them here](https://developers.refinitiv.com/))

## Installation (3 steps)

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd PairTrading
pip install -r requirements.txt
```

### 2. Configure API Credentials

Edit `RKDRetriever.py` lines 23-25:

```python
self.username = 'your_email@example.com'
self.password = 'your_password'
self.appid = 'YourApplicationID'
```

### 3. Run

```bash
jupyter notebook Interface2ChangeForFinal.ipynb
```

Run all cells. The system will:
- Download historical stock data
- Select cointegrated pairs
- Train ML models
- Backtest the strategy
- Display performance metrics

## What You'll Get

- **Portfolio Performance**: Annualized return, Sharpe ratio, max drawdown
- **Trade Log**: All entry/exit signals with timestamps
- **Visualizations**: Equity curve vs benchmark

## Configuration (Optional)

Edit notebook cell 2 to customize:

```python
bw = 120              # Training window (days)
hw = 10               # Testing window (days)
N_top_pairs = 10      # Number of pairs to trade
initial_capital = 10000
```

## Verify Your Setup

```bash
python3 verify_setup.py
```

This checks all dependencies and files.

## Troubleshooting

**Problem**: `ModuleNotFoundError`
**Solution**: `pip install -r requirements.txt`

**Problem**: Authentication failed
**Solution**: Check API credentials in `RKDRetriever.py`

**Problem**: No data for some stocks
**Solution**: Normal - some stocks may be delisted or not traded during the period

## Next Steps

- Read [README.md](README.md) for detailed documentation
- See [SETUP_GUIDE.md](SETUP_GUIDE.md) for bilingual setup guide
- Customize parameters for your strategy

## Project Structure

```
RKDRetriever.py        → Data retrieval
DataProcessor.py       → Data cleaning
PairsSelection.py      → Cointegration testing
FeatureEngineering.py  → Technical indicators
Interface2ChangeForFinal.ipynb → Main execution
```

---

**Need help?** Check the full [README.md](README.md) or open an issue.
