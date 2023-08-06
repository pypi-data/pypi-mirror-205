import numpy as np
from scipy import stats
from scipy.optimize import minimize 


def MLE_Norm(params, x, y):
    yhat = params[0] + params[1]*x # predictions
    negLL = -1 * np.sum(stats.norm.logpdf(y, yhat, params[2]))
    return(negLL)

def MLE_T(params, x, y):
    yhat = params[0] + params[1]*x # predictions
    negLL = -1 * np.sum(stats.t.logpdf(y-yhat, params[2], scale=params[3]))
    return(negLL)

def R_square(x, y, intercept, beta):   
    y_predicted = intercept + beta * x
    y_mean = np.mean(y)
    error = y - y_predicted
    ss_tot = sum((y - y_mean) ** 2)
    ss_res = sum((error - np.mean(error)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared