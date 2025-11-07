import pandas as pd
import numpy as np
from sklearn.cluster import OPTICS
from itertools import combinations
from statsmodels.tsa.stattools import coint

def compute_partial_corr(x, y, m):
    """
    Compute the partial correlation between two variables x and y, controlling for a third variable m.
    Parameters:
        x: array-like, first variable
        y: array-like, second variable
        m: array-like, third variable (market returns)
    """
    if np.nanstd(m) == 0:
        return np.corrcoef(x, y)[0, 1]
    
    r_xy = np.corrcoef(x, y)[0, 1]
    r_xm = np.corrcoef(x, m)[0, 1]
    r_ym = np.corrcoef(y, m)[0, 1]
    denom = np.sqrt((1 - r_xm**2) * (1 - r_ym**2))
    if denom == 0:
        return 0.0
    return (r_xy - r_xm * r_ym) / denom

def compute_pc_distance_matrix(df_returns, market_returns):
    """
    Compute the pairwise partial correlation distance matrix for stock returns.
    Parameters:
        df_returns: DataFrame, each column is the log return of a stock, index is date
        market_returns: Series, market return (index matches df_returns)
    Returns:
        pc_distance: DataFrame, symmetric matrix, index and columns are stock codes
        and the value is the partial correlation distance
    """
    stocks = df_returns.columns
    n = len(stocks)
    pc_distance = pd.DataFrame(np.zeros((n, n)), index=stocks, columns=stocks)
    
    # Convert market returns to a 1D array
    market_returns_1d = market_returns.values.squeeze()
    
    for i in range(n):
        for j in range(i, n):
            if i == j:
                pc_distance.iloc[i, j] = 0.0
            else:

                x = df_returns.iloc[:, i].values
                y = df_returns.iloc[:, j].values
                m = market_returns_1d
                pcorr = compute_partial_corr(x, y, m)
                # Partial correlation distance
                distance = 1 - abs(pcorr)
                pc_distance.iloc[i, j] = distance
                pc_distance.iloc[j, i] = distance
    return pc_distance

def select_pairs_from_clusters(labels, stock_list):
    
    """
    Select pairs of stocks from the same cluster based on clustering labels.
    Parameters:
        labels: array-like, clustering labels for each stock
        stock_list: list, list of stock codes corresponding to the labels
    Returns:
        pairs: list of tuples, each tuple contains two stock codes
    """
    df_labels = pd.DataFrame({'Stock': stock_list, 'Label': labels})
    pairs = []
    # For each unique label, find the stocks in that cluster and generate pairs
    # Note: -1 is used to indicate noise points in OPTICS clustering
    
    for label in df_labels['Label'].unique():
        if label == -1:
            continue  
        group = df_labels[df_labels['Label'] == label]['Stock'].tolist()
        
        if len(group) >= 2:
            cluster_pairs = [(s1, s2, label) for s1, s2 in combinations(group, 2)]
            pairs.extend(cluster_pairs)
    return pairs



def Engle_Granger_test(pairs, df, pvalue_threshold):
    cointegrated_pairs = []
    for s1_name, s2_name, cluster in pairs:
        s1 = df[s1_name]
        s2 = df[s2_name]
        
        score, pvalue, _ = coint(s1, s2, trend='c', maxlag=1)
        # Cointegration test p-value
        if pvalue < pvalue_threshold:
            
            hedge_ratio = np.polyfit(s1, s2, 1)[0]
            spread = s2 - hedge_ratio * s1 
            
            # Estimate half-life using the Ornstein-Uhlenbeck process
            spread_lag  = spread.shift(1).dropna()
            spread_diff = spread.diff().dropna()
            spread_lag  = spread_lag.iloc[1:] 
            spread_diff = spread_diff.iloc[1:]
            
            
            beta = np.polyfit(spread_lag, spread_diff, 1)[0]
            theta = -beta  
            half_life = np.log(2) / theta if theta > 0 else np.nan
            
            cointegrated_pairs.append({
                'pair':        (s1_name, s2_name),
                'pvalue':      pvalue,
                'hedge_ratio': hedge_ratio,
                'half_life':   half_life,
                'cluster':     cluster
            })
    
    return pd.DataFrame(cointegrated_pairs)

def pairs_selection(features_train_returns, SPX_train_returns, features_train_close, min_sample, pvalue_threshold):
    pc_distance_matrix = compute_pc_distance_matrix(features_train_returns, SPX_train_returns)
    optics_model = OPTICS(min_samples=2, metric="precomputed")
    labels = optics_model.fit_predict(pc_distance_matrix.values)
    stock_list = list(pc_distance_matrix.index)
    pairs = select_pairs_from_clusters(labels, stock_list)
    
    coin_pairs = Engle_Granger_test(pairs,features_train_close,pvalue_threshold)
    
    return coin_pairs


# Compute the distance matrix using partial correlation


# Use the distance matrix to cluster stocks
# Here we use the OPTICS clustering algorithm
# OPTICS is a density-based clustering algorithm that can handle noise and varying densities
# min_samples: the minimum number of samples in a neighborhood for a point to be considered a core point
# metric: the distance metric to use, here we use precomputed distance matrix
# Note: When using a precomputed distance matrix, set metric="precomputed"





