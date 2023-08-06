import numpy as np


# Exponentially Weighted Covariance Matrix
def exp_weighted_cov(returns, lambda_=0.97):
    """
    Perform calculation on the input data set with a given λ for exponentially weighted covariance.
    
    Parameters:
    - data: input data set, a pandas DataFrame
    - lambda_: fraction for unpdate the covariance matrix, default 0.97
    
    Returns:
    cov: an exponentially weighted covariance matrix, a numpy array
    """
    
    # Preprocess the data
    returns = returns.values
    mean_return = np.mean(returns, axis=0)
    normalized_returns = returns - mean_return
    
    # Initializing the covariance matrix
    n_timesteps = normalized_returns.shape[0]
    cov = np.cov(returns, rowvar=False)
    
    # Updating the covariance matrix
    for t in range(1, n_timesteps):
        cov = lambda_ * cov + (1 - lambda_) * np.outer(normalized_returns[t], normalized_returns[t])
    return cov

# Exponentially Weighted Matrix
def exp_weighted_matrix(returns, lambda_=0.97):
    """
    Perform calculation on the input data set with a given λ for exponentially weighted covariance.
    
    Parameters:
    - data: input data set, a pandas DataFrame
    - lambda_: fraction for unpdate the covariance matrix, default 0.97
    
    Returns:
   weights_matrix: an exponentially weighted matrix, a numpy array
    """
    
    # Preprocess the data
    returns = returns.values
    
    # Initializing the matrix
    n_timesteps = returns.shape[0]
    weights = np.zeros(n_timesteps)
    
    # Compute the weight for each time step
    for t in range(n_timesteps):
        weights[n_timesteps-1-t]  = (1-lambda_)*lambda_**t
    
    # Normalize the weights_matrix
    weights_matrix = np.diag(weights/sum(weights))

    return weights_matrix

# Cholesky Factorization 
def chol_psd(cov_matrix):
    """
    Perform Cholesky decomposition on the input matrix `covariance`.
    
    Parameters:
    - cov_matrix: input matrix, a numpy array with shape (n_samples, n_samples)
    
    Returns:
    The Cholesky decomposition of the input matrix `covariance`.
    """
    n = cov_matrix.shape[0]
    root = np.zeros_like(cov_matrix)
    for j in range(n):
        s = 0.0
        if j > 0:
            # calculate dot product of the preceeding row values
            s = np.dot(root[j, :j], root[j, :j])
        temp = cov_matrix[j, j] - s
        if 0 >= temp >= -1e-8:
            temp = 0.0
        root[j, j] = np.sqrt(temp)
        if root[j, j] == 0.0:
            # set the column to 0 if we have an eigenvalue of 0
            root[j + 1:, j] = 0.0
        else:
            ir = 1.0 / root[j, j]
            for i in range(j + 1, n):
                s = np.dot(root[i, :j], root[j, :j])
                root[i, j] = (cov_matrix[i, j] - s) * ir
    return root

# Dealing with Non-PSD Matrices - Rebonato and Jackel
def near_psd(matrix, epsilon=0.0):
    """
    Calculates a near positive semi-definite (PSD) matrix from a given non-PSD matrix.

    Parameters:
    - matrix: The input matrix, a 2-dimensional numpy array
    - epsilon: A small non-negative value used to ensure that the resulting matrix is PSD, default value is 0.0

    Returns:
    The output of this function is a 2-dimensional numpy array that represents a near PSD matrix. 
    """
    n = matrix.shape[0]

    invSD = None
    out = matrix.copy()

    # calculate the correlation matrix if we got a covariance
    if np.count_nonzero(np.diag(out) == 1.0) != n:
        invSD = np.diag(1 / np.sqrt(np.diag(out)))
        out = np.matmul(np.matmul(invSD, out), invSD)

    # SVD, update the eigen value and scale
    vals, vecs = np.linalg.eigh(out)
    vals = np.maximum(vals, epsilon)
    T = np.reciprocal(np.matmul(np.square(vecs), vals))
    T = np.diag(np.sqrt(T))
    l = np.diag(np.sqrt(vals))
    B = np.matmul(np.matmul(T, vecs), l)
    out = np.matmul(B, np.transpose(B))

    # Add back the variance
    if invSD is not None:
        invSD = np.diag(1 / np.diag(invSD))
        out = np.matmul(np.matmul(invSD, out), invSD)

    return out

# Dealing with Non-PSD Matrices - Higham
def Pu(matrix):
    """The first projection for Higham method with the assumption that weight martrix is diagonal."""
    result = matrix.copy()
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if i==j:
                result[i][i]=1
    return result

def Ps(matrix, weight):
    """The second projection for Higham method."""
    matrix = np.sqrt(weight)@ matrix @np.sqrt(weight)
    vals, vecs = np.linalg.eigh(matrix)
    vals = np.array([max(i,0) for i in vals])
    result = np.sqrt(weight)@ vecs @ np.diagflat(vals) @ vecs.T @ np.sqrt(weight)
    return result

def Frobenius_Norm(matrix_1, matrix_2):
    distance = matrix_1 - matrix_2
    result = 0
    for i in range(len(distance)):
        for j in range(len(distance)):
            result += distance[i][j]**2
    return result

def Higham_psd(matrix, weight = None, epsilon = 1e-9, max_iter = 1000, tolerance = 1e-8):
    """
    Calculates a near positive semi-definite (PSD) matrix from a given non-PSD matrix.

    Parameters:
    - matrix: The input covariance matrix, a 2-dimensional numpy array
    - weight: Assume weight is a diagonal matrix, if unweighted, set 𝑊 = 𝐼
    - epsilon: Used to check the smallest eigenvalue from the result
    - max_iter: Restriction on the maximum iteration loops
    - tolerance: A small non-negative value used to restrict the distance for the original matrix, default value is 1e-8

    Returns:
    The output of this function is a 2-dimensional numpy array that represents a nearest PSD matrix. 
    """
    if weight is None:
        weight = np.identity(len(matrix))
        
    norml = np.inf
    Yk = matrix.copy()
    Delta_S = np.zeros_like(Yk)
    
    invSD = None
    if np.count_nonzero(np.diag(Yk) == 1.0) != matrix.shape[0]:
        invSD = np.diag(1 / np.sqrt(np.diag(Yk)))
        Yk = np.matmul(np.matmul(invSD, Yk), invSD)
    
    Y0 = Yk.copy()

    for i in range(max_iter):
        Rk = Yk - Delta_S
        Xk = Ps(Rk, weight)
        Delta_S = Xk - Rk
        Yk = Pu(Xk)
        norm = Frobenius_Norm(Yk, Y0)
        minEigVal = np.real(np.linalg.eigvals(Yk)).min()
        if abs(norm - norml) < tolerance and minEigVal > -epsilon:
            break
        else:
            norml = norm
    
    if invSD is not None:
        invSD = np.diag(1 / np.diag(invSD))
        Yk = np.matmul(np.matmul(invSD, Yk), invSD)
    return Yk

# Check the matrix is PSD or not
def is_psd(matrix):
    """For a given matrix, check if the matrix is psd or not."""
    eigenvalues = np.linalg.eigh(matrix)[0]
    return np.all(eigenvalues >= -1e-8)


def missing_cov(x, skipMiss=True, fun=np.corrcoef):
    n, m = x.shape
    nMiss = np.sum(np.isnan(x), axis=0)

    # nothing missing, just calculate it.
    if np.sum(nMiss) == 0:
        return fun(x)

    idxMissing = [set(np.where(np.isnan(x[:, i]))[0]) for i in range(m)]

    if skipMiss:
        # Skipping Missing, get all the rows which have values and calculate the covariance
        rows = set(range(n))
        for c in range(m):
            for rm in idxMissing[c]:
                if rm in rows:
                    rows.remove(rm)
        rows = sorted(list(rows))
        return fun(x[rows,:].T)

    else:
        # Pairwise, for each cell, calculate the covariance.
        out = np.empty((m, m))
        for i in range(m):
            for j in range(i+1):
                rows = set(range(n))
                for c in (i,j):
                    for rm in idxMissing[c]:
                        if rm in rows:
                            rows.remove(rm)
                rows = sorted(list(rows))
                out[i,j] = fun(x[rows,:][:,[i,j]].T)[0,1]
                if i != j:
                    out[j,i] = out[i,j]
        return out