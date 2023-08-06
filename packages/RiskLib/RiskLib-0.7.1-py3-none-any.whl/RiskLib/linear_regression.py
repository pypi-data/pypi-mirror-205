import numpy as np
from scipy.optimize import fsolve, minimize
from scipy.stats import t, kurtosis

# fit regression model with T errors
def fit_regression_t(y, x):
    n = x.shape[0]

    # create a matrix with ones as the first column
    X = np.column_stack((np.ones(n), x))
    nB = X.shape[1]

    # define a function to calculate the negative log-likelihood
    def neg_log_likelihood(params):
        b, s, nu = params[:nB], params[nB], params[nB+1]
        errors = y - X @ b
        errorModel = t(df=nu, loc=0, scale=s)
        return -np.sum(np.log(errorModel.pdf(errors)))

    #approximate values based on moments and OLS
    b_start = np.linalg.inv(X.T @ X) @ X.T @ y
    e = y - X @ b_start
    start_m = np.mean(e)
    start_nu = 6.0 / kurtosis(e) + 4
    start_s = np.sqrt(np.var(e) * (start_nu - 2) / start_nu)

    # set initial parameter values
    params_start = np.concatenate((b_start, [start_s, start_nu]))

    # define bounds for parameters
    bounds = [(None, None)] * nB + [(1e-6, None), (2.0001, None)]

    # minimize negative log-likelihood
    result = minimize(neg_log_likelihood, params_start, bounds=bounds)

    # extract parameter estimates and calculate fitted values
    beta = result.x[:nB]
    s = result.x[nB]
    nu = result.x[nB+1]
    errorModel = t(df=nu, loc=0, scale=s)
    fitted_values = X @ beta + errorModel.ppf(0.5)

    # Calculate the regression errors and their U values
    errors = y - fitted_values
    params = {'alpha': beta[0], 'beta': beta[1]}

    return params, errors