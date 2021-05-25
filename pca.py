# GRADED FUNCTION: DO NOT EDIT THIS LINE

# ===YOU SHOULD EDIT THIS FUNCTION===
def normalize(X):
    """Normalize the given dataset X to have zero mean.
    Args:
        X: ndarray, dataset of shape (N,D)
    
    Returns:
        (Xbar, mean): tuple of ndarray, Xbar is the normalized dataset
        with mean 0; mean is the sample mean of the dataset.
    """    
    mu = X.mean(0)
    Xbar = X - mu
    return Xbar, mu
    


# GRADED FUNCTION: DO NOT EDIT THIS LINE
# ===YOU SHOULD EDIT THIS FUNCTION===

def eig(S):
    """Compute the eigenvalues and corresponding eigenvectors
        for the covariance matrix S.
    Args:
        S: ndarray, covariance matrix

    Returns:
        (eigvals, eigvecs): ndarray, the eigenvalues and eigenvectors

    Note:
        the eigenvals and eigenvecs should be sorted in descending
        order of the eigen values
    """
    # YOUR CODE HERE
    # Uncomment and modify the code below
    # Compute the eigenvalues and eigenvectors
    # You can use library routines in `np.linalg.*` 
    # https://numpy.org/doc/stable/reference/routines.linalg.html
    # for this
    eigvals, eigvecs = np.linalg.eig(S)
    
    # The eigenvalues and eigenvectors need to be
    # sorted in descending order according to the eigenvalues
    # We will use `np.argsort` (https://docs.scipy.org/doc/numpy/reference/generated/numpy.argsort.html)
    # to find a permutation of the indices
    # of eigvals that will sort eigvals in ascending order and
    # then find the descending order via [::-1], which reverse
    # the indices
    sort_indices = np.argsort(eigvals)[::-1]
    
    # Notice that we are sorting the columns (not rows) of
    # eigvecs since the columns represent the eigenvectors.
    return eigvals[sort_indices], eigvecs[:, sort_indices]



# GRADED FUNCTION: DO NOT EDIT THIS LINE
# ===YOU SHOULD EDIT THIS FUNCTION===

def projection_matrix(B):
    """Compute the projection matrix onto the space spanned by `B`
    Args:
        B: ndarray of dimension (D, M), the basis for the subspace
    
    Returns:
        P: the projection matrix
    """
    P =  B @ np.linalg.inv(B.T @ B) @ B.T
    return P



# GRADED FUNCTION: DO NOT EDIT THIS LINE
# ===YOU SHOULD EDIT THIS FUNCTION===

def PCA(X, num_components):
    """
    Args:
        X: ndarray of size (N, D), where D is the dimension of the data,
           and N is the number of datapoints
        num_components: the number of principal components to use.
    Returns:
        the reconstructed data, the sample mean of the X, principal values
        and principal components
    """
    N, D = X.shape
    
    # first perform normalization on the digits so that they have zero mean and unit variance
    X_normalized, mean = normalize(X)
    
    # Then compute the data covariance matrix S
    S = np.cov(X_normalized/ N, rowvar=False, bias=True)

    # Next find eigenvalues and corresponding eigenvectors for S
    eig_vals, eig_vecs = eig(S)
    
    # Take the top `num_components` of eig_vals and eig_vecs,
    # This will be the corresponding principal values and components
    principal_vals = eig_vals[:num_components]
    principal_components = eig_vecs[:, :num_components]

    # reconstruct the data from the using the basis spanned by the principal components
    # Notice that we have subtracted the mean from X so make sure that you add it back
    # to the reconstructed data
    P = projection_matrix(principal_components)  # projection matrix
    reconst = (P @ X_normalized.T).T + mean
    return reconst, mean, principal_vals, principal_components
  
    
