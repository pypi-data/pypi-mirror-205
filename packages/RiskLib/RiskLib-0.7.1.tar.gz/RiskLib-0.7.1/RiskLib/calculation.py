import numpy as np
import pandas as pd


# Calculate the return
def return_calculate(prices, method="DISCRETE", dateColumn="Date"):
    vars_ = prices.columns
    nVars = len(vars_)
    vars_ = [var for var in vars_ if var != dateColumn]
    if nVars == len(vars_):
        raise ValueError(f"dateColumn: {dateColumn} not in DataFrame: {vars_}")
    nVars = nVars - 1

    p = prices[vars_].to_numpy()
    n, m = p.shape
    p2 = np.empty((n-1, m))

    for i in range(n-1):
        for j in range(m):
            p2[i, j] = p[i+1, j] / p[i, j]

    if method.upper() == "DISCRETE":
        p2 = p2 - 1.0
    elif method.upper() == "LOG":
        p2 = np.log(p2)
    else:
        raise ValueError(f"method: {method} must be in (\"LOG\",\"DISCRETE\")")

    dates = prices[dateColumn].iloc[1:n].to_numpy()
    out = pd.DataFrame({dateColumn: dates})
    for i in range(nVars):
        out[vars_[i]] = p2[:, i]

    return out


def get_portfolio_price(portfolio, prices, portfolio_code, Delta=False):
    """Get the price for each asset in portfolio and calculate the current price."""
    
    if portfolio_code == "All":
        assets = portfolio.drop('Portfolio',axis=1)
        assets = assets.groupby(["Stock"], as_index=False)["Holding"].sum()
    else:
        assets = portfolio[portfolio["Portfolio"] == portfolio_code]
        
    stock_codes = list(assets["Stock"])
    assets_prices = pd.concat([prices["Date"], prices[stock_codes]], axis=1)
    
    current_price = np.dot(prices[assets["Stock"]].tail(1), assets["Holding"])
    holdings = assets["Holding"]
    
    if Delta == True:
        asset_values = assets["Holding"].values.reshape(-1, 1) * prices[assets["Stock"]].tail(1).T.values
        delta = asset_values / current_price
        
        return current_price, assets_prices, delta
    
    return current_price, assets_prices, holdings