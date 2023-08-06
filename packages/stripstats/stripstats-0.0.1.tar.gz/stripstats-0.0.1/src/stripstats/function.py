"""
Statistical Functions.
======================

Working on adding all the basic statistical functions needed for
data analysis.



"""


def frequency(L:list, X:int):
    # Counts the frequency of given integer (X) in list (L)
    count = 0
    for i in L:
        if (i == X):
            count += 1
    return count

def mode(X:list):
    # Runs a for loop through given data, counting each values appearances
    # Comaping to maxV until it reaches the end and returns the max appearnces
    maxV = 0
    mode = 0
    for i in X:
        count = frequency(X, i)
        if (count > maxV):
            maxV = count
            mode = i
    
    return mode

def median(X:list):
    """Finds the median of a given list.

    Args:
        X (list): List of ints

    Returns:
        int: median
    """
    N = len(X)
    X.sort()
    if N % 2 == 0: 
        return ((X[N//2]) + (X[N//2 - 1])) / 2
    # else use the middle
    return X[N//2]

def mean(X):
    """Finds the mean given the array.

    Parameters
    ----------
    X : array_like
        An array of values

    Returns
    -------
    mean : float
        mean of array
    """
    return sum(X) / len(X)

def sum_squares(X:list):
    """Sum of squares

    Args:
        X (list): _description_

    Returns:
        _type_: _description_
    """
    squared = []
    for i in X:
        squared.append(i**2)
    return sum(squared) - ((sum(X))**2)/len(X)

def variance(X:list, ddof=1):
    """Finds the variance.

    Parameters
    ----------
    X : array_like
        An array of values
    ddof : int, optional
        Delta degrees of freedom. Defaults to 1.
    
    Returns
    -------
    var : float
        Variance

    Notes
    -----
    'var' computes the sample variance by default, it uses
    n - 1 in the denominator; Use a ddof of 0 to find the population
    variance.

    Examples
    --------


    """
    return sum_squares(X) / (len(X) - ddof)

def std(X:list, ddof=1):
    """Compute the standard deviation.

    Parameters
    ----------
    X : array_like
        An array of values
    ddof : int, optional
        Delta degrees of freedom, by default 1

    Returns
    -------
    std : float
        Standard deviation.

    Notes
    -----
    'std' computes the sample standard deviation by default, it uses
    n - 1 in the denominator; Use a ddof of 0 to find the population
    standard deviation.

    Examples
    --------
    >>> from hewstats import std
    >>> import numpy as np
    >>> x = np.arange(20)
    >>> std(x)
    5.916079783099616
    >>> std(x, ddof=0)
    5.766281297335398
    """
    return (variance(X, ddof))**0.5

def standard_error(X:list, ddof=1):
    """Finds standard error.

    Parameters
    ----------
    X : array_like
        An array of values
    ddof : int, optional
        Delta degrees of freedom, by default 1

    Returns
    -------
    SE : float
        The standard error
    
    Notes
    -----
    'std' computes the sample standard deviation by default, it uses
    n - 1 in the denominator; Use a ddof of 0 to find the population
    SE.

    Examples
    --------
    """
    return std(X, ddof) / ((len(X))**0.5)

def coeffvar(X:list, ddof=1):
    # Finds the coefficient of variation, returns value as a percent through *100
    return (std(X, ddof) / mean(X)) * 100

def z_score(SCORE, X:list):
    M = mean(X)
    SD = std(X, "sample")
    return (SCORE - M) / SD

def cohen(A, B, ddofA=1, ddofB=1):
    """Compute the Cohen's D effect size.

    Parameters
    ----------
    A : array_like
        An array of values
    B : array_like
        An array of values
    ddofA : int, optional
        Delta degrees of freedom related to array A. Defaults to 1.
    ddofB : int, optional
        Delta degrees of freedom related to array B. Defaults to 1.

    Returns
    -------
    d : float
        The effect size

    Notes
    -----
    Solves for Cohen's D.

    Examples
    --------

    """
    return (mean(A) - mean(B)) / (((len(A) - 1) * pow(std(A, ddof=ddofA), 2)) + 
            ((len(B) - 1) * pow(std(B, ddof=ddofB), 2)) / (len(A) + len(B) - 2))**0.5