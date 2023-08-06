import numpy as np
import pandas as pd
from . import cov_matrix
from scipy.stats import t, norm
from scipy.optimize import minimize 

# Multivariate Normal Simulation
def multivariate_normal_simulation(covariance_matrix, n_samples, method='direct', mean = 0, explained_variance=1.0, seed=1234):
    """
    A function to simulate multivariate normal distributions with different methods.
    
    Parameters:
    - covariance_matrix (np.array): The covariance matrix for the multivariate normal distribution
    - n_samples (int): The number of samples to generate
    - method (str, optional): The method to use for simulation, either 'direct' or 'pca', default 'direct'
         'direct': simulate directly from the covariance matrix.
         'pca': simulate using principal component analysis (PCA).
    - explained_variance (float, optional): The percentage of explained variance to keep when using PCA, default 1.0
    
    Returns:
     np.array: An array with shape (covariance_matrix.shape[0], n_samples) with the simulated samples.
    """
    np.random.seed(seed)
    
    # If the method is 'direct', simulate directly from the covariance matrix
    if method == 'direct':
        
        L = cov_matrix.chol_psd(covariance_matrix)
        normal_samples = np.random.normal(size=(covariance_matrix.shape[0], n_samples))
        
        samples = np.transpose(np.dot(L, normal_samples) + mean)
        
        return samples
    
    # If the method is 'pca', simulate using PCA
    elif method == 'pca':
        eigenvalues, eigenvectors = np.linalg.eigh(covariance_matrix)
        
        # Only consider eigenvalues greater than 0
        idx = eigenvalues > 1e-8
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Sort the eigenvalues in descending order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]
        
        # Update the explained_variance incase the explained_variance is higher than the cumulative sum of the eigenvalue
        if explained_variance == 1.0:
            explained_variance = (np.cumsum(eigenvalues)/np.sum(eigenvalues))[-1]
        
        # Determine the number of components to keep based on the explained variance ratio
        n_components = np.where((np.cumsum(eigenvalues)/np.sum(eigenvalues))>= explained_variance)[0][0] + 1
        eigenvectors = eigenvectors[:,:n_components]
        eigenvalues = eigenvalues[:n_components]

        normal_samples = np.random.normal(size=(n_components, n_samples))
        
        # Simulate the multivariate normal samples by multiplying the eigenvectors with the normal samples
        B = np.dot(eigenvectors, np.diag(np.sqrt(eigenvalues)))
        samples = np.transpose(np.dot(B, normal_samples))
        
        return samples
    


# Fitting T
# MLE fitted T distribution

def Fitting_t_MLE(returns):

    def MLE_T(params, returns):
        negLL = -1 * np.sum(t.logpdf(returns, df=params[0], loc=params[1], scale=params[2]))
        return(negLL)
    
    constraints=({"type":"ineq", "fun":lambda x: x[0]-1}, 
                 {"type":"ineq", "fun":lambda x: x[2]})
    
    returns_t = minimize(MLE_T, x0=[10, np.mean(returns), np.std(returns)], args=returns, constraints=constraints)
    df, loc, scale = returns_t.x[0], returns_t.x[1], returns_t.x[2]
    return df, loc, scale


def gaussian_copula(returns, fitting_model=None, n_sample=10000, seed=12345):
    stocks = returns.columns.tolist()
    n = len(stocks)

    if fitting_model is None:
        fitting_model = np.full(n, 't')


    # Fitting model for each stock
    parameters = []
    assets_returns_cdf = pd.DataFrame()
    for i, stock in enumerate(stocks):
        if fitting_model[i] == 't':
            params = Fitting_t_MLE(returns[stock])
            fitting = 't'
        elif fitting_model[i] == 'n':
            params = norm.fit(returns[stock])
            fitting = 'n'
        parameters.append(params)
        assets_returns_cdf[stock] = t.cdf(returns[stock],df=params[0], loc=params[1], scale = params[2]) if fitting == 't' else norm.cdf(returns[stock],loc=params[0], scale = params[1])

    # Simulate N samples with spearman correlation matrix
    np.random.seed(seed)
    spearman_corr_matrix = assets_returns_cdf.corr(method='spearman')
    sim_sample = multivariate_normal_simulation(spearman_corr_matrix, n_sample, method='pca',seed=seed)
    sim_sample = pd.DataFrame(sim_sample, columns=stocks)

    # Convert simulation result with cdf of standard normal distribution
    sim_sample_cdf = pd.DataFrame()
    for stock in stocks:
        sim_sample_cdf[stock] = norm.cdf(sim_sample[stock],loc=0,scale=1)
            
    # Convert cdf matrix to return matrix with parameter
    sim_returns = pd.DataFrame()
    for i, stock in enumerate(stocks):
        if fitting_model[i] == 't':       
            sim_returns[stock] = t.ppf(sim_sample_cdf[stock], df=parameters[i][0], loc=parameters[i][1], scale = parameters[i][2])
        elif fitting_model[i] == 'n':
            sim_returns[stock] = norm.ppf(sim_sample_cdf[stock],  loc=parameters[i][0], scale = parameters[i][1])
    
    return sim_returns, pd.DataFrame(parameters,index=[stocks,fitting_model])