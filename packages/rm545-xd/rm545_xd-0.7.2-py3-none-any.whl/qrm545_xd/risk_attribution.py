import numpy as np
import pandas as pd

def risk_contrib(w, covar):
    risk_contrib = w * covar.dot(w) / np.sqrt(w.dot(covar).dot(w))
    return risk_contrib

def expost_attribution(w, upReturns):
    _stocks = list(upReturns.columns)
    n = upReturns.shape[0]
    pReturn = np.empty(n)
    weights = np.empty((n, len(w)))
    lastW = np.copy(w)
    matReturns = upReturns[_stocks].values

    for i in range(n):
        # Save Current Weights in Matrix
        weights[i,:] = lastW

        # Update Weights by return
        lastW = lastW * (1.0 + matReturns[i,:])

        # Portfolio return is the sum of the updated weights
        pR = np.sum(lastW)
        # Normalize the wieghts back so sum = 1
        lastW = lastW / pR
        # Store the return
        pReturn[i] = pR - 1

    # Set the portfolio return in the Update Return DataFrame
    upReturns['Portfolio'] = pReturn

    # Calculate the total return
    totalRet = np.exp(np.sum(np.log(pReturn + 1))) - 1
    # Calculate the Carino K
    k = np.log(totalRet + 1) / totalRet

    # Carino k_t is the ratio scaled by 1/K 
    carinoK = np.log(1.0 + pReturn) / pReturn / k
    # Calculate the return attribution
    attrib = pd.DataFrame(matReturns * (weights * carinoK[:, np.newaxis]), columns=_stocks)

    # Set up a Dataframe for output.
    Attribution = pd.DataFrame({'Value': ["TotalReturn", "Return Attribution"]})

    _ss = list(upReturns.columns)
    _ss.append('Portfolio')
    
    for s in _ss:
        # Total Stock return over the period
        tr = np.exp(np.sum(np.log(upReturns[s] + 1))) - 1
        # Attribution Return (total portfolio return if we are updating the portfolio column)
        atr =  attrib[s].sum() if s != 'Portfolio' else tr
        # Set the values
        Attribution[s] = [tr, atr]

        # Y is our stock returns scaled by their weight at each time
        Y =  matReturns * weights
        # Set up X with the Portfolio Return
        X = np.column_stack((np.ones((pReturn.shape[0], 1)), pReturn))
        # Calculate the Beta and discard the intercept
        B = (np.linalg.inv(X.T @ X) @ X.T @ Y)[1,:]
        # Component SD is Beta times the standard Deviation of the portfolio
        cSD = B * np.std(pReturn)

        Expost_Attribution = pd.concat([Attribution,    
            pd.DataFrame({"Value": ["Vol Attribution"], 
                        **{_stocks[i]: [cSD[i]] for i in range(len(_stocks))},
                        "Portfolio": [np.std(pReturn)]})
        ], ignore_index=True)

    return Expost_Attribution


def expost_factor(w, upReturns, upFfData, Betas):
    stocks = upReturns.columns
    factors = list(upFfData.columns)
    
    n = upReturns.shape[0]
    m = len(stocks)
    
    pReturn = np.empty(n)
    residReturn = np.empty(n)
    weights = np.empty((n, len(w)))
    factorWeights = np.empty((n, len(factors)))
    lastW = w.copy()
    matReturns = upReturns[stocks].to_numpy()
    ffReturns = upFfData[factors].to_numpy()

    for i in range(n):
        # Save Current Weights in Matrix
        weights[i,:] = lastW

        #Factor Weight
        factorWeights[i,:] = Betas.T @ lastW

        # Update Weights by return
        lastW = lastW * (1.0 + matReturns[i,:])

        # Portfolio return is the sum of the updated weights
        pR = np.sum(lastW)
        # Normalize the weights back so sum = 1
        lastW = lastW / pR
        # Store the return
        pReturn[i] = pR - 1

        # Residual
        residReturn[i] = (pR-1) - factorWeights[i,:] @ ffReturns[i,:]

    # Set the portfolio return in the Update Return DataFrame
    upFfData["Alpha"] = residReturn
    upFfData["Portfolio"] = pReturn

    # Calculate the total return
    totalRet = np.exp(np.sum(np.log(pReturn + 1))) - 1
    # Calculate the Carino K
    k = np.log(totalRet + 1) / totalRet

    # Carino k_t is the ratio scaled by 1/K 
    carinoK = np.log(1.0 + pReturn) / pReturn / k
    # Calculate the return attribution
    attrib = pd.DataFrame(ffReturns * (factorWeights * carinoK[:, np.newaxis]), columns=factors)
    attrib["Alpha"] = residReturn * carinoK

    # Set up a DataFrame for output.
    Attribution = pd.DataFrame({"Value": ["TotalReturn", "Return Attribution"]})

    
    newFactors = factors[:]
    newFactors.append('Alpha')

    ss = factors[:]
    ss.append('Alpha')
    ss.append('Portfolio')

    # Loop over the factors
    for s in ss:
        # Total Stock return over the period
        tr = np.exp(np.sum(np.log(upFfData[s] + 1))) - 1
        # Attribution Return (total portfolio return if we are updating the portfolio column)
        atr = sum(attrib[s]) if s != "Portfolio" else tr
        # Set the values
        Attribution[s] = [tr, atr]

    # Realized Volatility Attribution

    # Y is our stock returns scaled by their weight at each time
    Y = np.hstack((ffReturns * factorWeights, residReturn[:,np.newaxis]))
    # Set up X with the Portfolio Return
    X = np.hstack((np.ones((n,1)), pReturn[:,np.newaxis]))
    # Calculate the Beta and discard the intercept
    B = np.linalg.inv(X.T @ X) @ X.T @ Y
    B = B[1,:]
    # Component SD is Beta times the standard Deviation of the portfolio
    cSD = B * np.std(pReturn)

    # Check that the sum of component SD is equal to the portfolio SD
    assert np.isclose(np.sum(cSD), np.std(pReturn))

    # Add the Vol attribution to the output
    Expost_Attribution = pd.concat([Attribution, 
        pd.DataFrame({"Value": "Vol Attribution", **{newFactors[i]:cSD[i] for i in range(len(newFactors))}, "Portfolio":np.std(pReturn)}, index=[0])
    ])

    return Expost_Attribution