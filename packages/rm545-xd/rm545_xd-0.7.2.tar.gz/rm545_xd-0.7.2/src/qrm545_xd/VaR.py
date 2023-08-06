import numpy as np

def calculate_var(data, mean=0, alpha=0.05):
  return mean - np.quantile(data, alpha)

def calculate_ES(a, alpha=0.05):
    x = np.sort(a)
    nup = int(np.ceil(a.size * alpha))
    ndn = int(np.floor(a.size * alpha))
    v = 0.5 * (x[nup] + x[ndn])
    
    es = np.mean(x[x <= v])
    return -es