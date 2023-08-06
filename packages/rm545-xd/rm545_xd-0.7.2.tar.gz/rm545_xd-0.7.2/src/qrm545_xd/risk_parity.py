import numpy as np
import pandas as pd
from scipy.optimize import minimize

def vol_risk_parity(stockMeans, covar, b=None):
    n = len(stockMeans)
    
    # Function for Portfolio Volatility
    def pvol(w):
        x = np.array(w)
        return np.sqrt(x.dot(covar).dot(x))
    
    # Function for Component Standard Deviation
    def pCSD(w, b=None, last = False):
        x = np.array(w)
        pVol = pvol(w)
        csd = x * (covar.dot(x)) / pVol
        if last:
            return csd
        if b is not None:
            csd /= b
        return csd
    
    # Sum Square Error of cSD
    def sseCSD(w):
        csd = pCSD(w, b)
        mCSD = np.sum(csd) / n
        dCsd = csd - mCSD
        se = dCsd * dCsd
        return 1.0e5 * np.sum(se) # Add a large multiplier for better convergence
    
    # Define the optimization problem
    m = minimize(sseCSD, [1/n]*n, method='SLSQP', bounds=[(0, None)]*n, constraints={'type': 'eq', 'fun': lambda w: np.sum(w)-1})
    
    w = m.x
    
    # Compute RPWeights
    RPWeights = pd.DataFrame({
        'Weight': w,
        'cEr': stockMeans * w,
        'CSD': pCSD(w, b, True)
    })
    
    return RPWeights


def es_risk_parity(stock, stockMeans, simReturn, b=None):
    # internal ES function
    def _ES(*w):

        def ES(a, alpha=0.05):
            x = np.sort(a)
            nup = int(np.ceil(a.size * alpha))
            ndn = int(np.floor(a.size * alpha))
            v = 0.5 * (x[nup] + x[ndn])
            
            es = np.mean(x[x <= v])
            return -es
        r = simReturn @ w
        return ES(r)

    # Function for the component ES
    def CES(w, b=None, last = False):
        x = list(w)
        n = len(x)
        ces = np.empty(n)
        es = _ES(*x)
        e = 1e-6
        for i in range(n):
            old = x[i]
            x[i] = x[i] + e
            ces[i] = old * (_ES(*x) - es) / e
            x[i] = old
        if last:
            return ces
        if b is not None:
            ces /= b
        return ces 

    # SSE of the Component ES
    def SSE_CES(*w):
        ces = CES(*w,b)
        ces = [x - sum(ces) / len(ces) for x in ces]
        return 1e3 * (sum([x ** 2 for x in ces]))
    
    n = len(stock)
    w0 = np.full(n, 1/n)
    bounds = [(0, None)] * n
    res = minimize(SSE_CES, w0, method='SLSQP', bounds=bounds, constraints=[{'type': 'eq', 'fun': lambda w: sum(w) - 1}])
    w = res.x
    
    # Compute RPWeights
    ES_RPWeights = pd.DataFrame({
        'Stock': stock,
        'Weight': w,
        'cEr': stockMeans * w,
        'CES': CES(w, b, True)
    }).set_index('Stock')
    
    return ES_RPWeights

