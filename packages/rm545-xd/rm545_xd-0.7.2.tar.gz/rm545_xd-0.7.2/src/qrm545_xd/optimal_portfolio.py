import numpy as np
import pandas as pd
from scipy.optimize import minimize

def sharp_ratio(weights, returns, cov_matrix, rf_rate):
    port_return = np.sum(returns * weights)
    port_std_dev = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    sharpe_ratio = (port_return - rf_rate) / port_std_dev
    return sharpe_ratio

def Optweight_sr(stocks, stockMeans, covar, rf, bound=(0,None)):

    # Define Sharpe ratio function
    def sr(w):
        m = np.dot(w, stockMeans) - rf
        s = np.sqrt(np.dot(w.T, np.dot(covar, w)))
        return m / s

    n = len(stocks)

    # Define optimization problem
    bounds = [bound] * n
    cons = {"type": "eq", "fun": lambda w: np.sum(w) - 1}
    result = minimize(lambda w: -sr(w), np.ones(n) / n, method="SLSQP", bounds=bounds, constraints=cons)

    # Extract optimal weights and other information
    w = result.x
    w = w / np.sum(w)
    OptWeights = pd.DataFrame({"Stock": stocks, "Weight": w, "cEr": stockMeans * w})

    return OptWeights, sr(w)


def Optweight_sr_two_assets(assets, except_return, covariance_matrix, rf, bound=(0,1)):
    
    def _sr(w):
        m = np.dot(w, except_return) - rf
        s = np.sqrt(np.dot(w.T, np.dot(covariance_matrix, w)))
        return m / s

    # Brute Force Find the maximum
    rng = np.arange(bound[0],bound[1]+0.00001,0.0001)
    vals = np.zeros((len(rng), 3))

    for i, a in enumerate(rng):
        s = _sr(np.array([a, 1 - a]))
        vals[i,:] = [a, 1 - a, s]

    max_idx = np.argmax(vals[:, 2])
    result = vals[max_idx, [0, 1]]
    Optweights = pd.DataFrame({"Weight":result}, index=assets)
    return Optweights, _sr(result)