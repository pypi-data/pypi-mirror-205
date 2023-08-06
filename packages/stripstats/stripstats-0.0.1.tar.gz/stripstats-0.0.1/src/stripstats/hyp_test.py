"""
Hypothesis Statistical Tests.
======================

Working on adding all the hypothesis statistical tests needed for
data analysis.



"""
from collections import namedtuple
from stripstats.function import cohen, mean, sum_squares
from scipy.stats import ttest_1samp
import scipy.stats

def CHI_SQR(O, E):
    """Compute the the chi-squared, The Chi-Squared Test of Independence.

    Parameters
    ----------
    O : array_like
        An array of observed values
    E : array_like
        An array of expected values

    Returns
    -------
    chi_sqr : float
        chi-squared.

    Notes
    -----
    'chi_sqr' computes the chi-squared by default. Found by the sum of each observed 
    value minus expected value, squared divided by the expected.

    Examples
    --------
    >>> from stripstats.hyp_test import chi_sqr
    >>> chi_sqr(_o, _e)
    >>> _o = [23, 16, 14, 19, 28]
    >>> _e = [20, 20, 20, 20, 20]
    >>> chi_sqr(_o, _e)

    """
    tot = 0
    for i in range(len(O)):
        tot += ((pow(O[i] - E[i], 2)) / E[i])
    return tot

tTEST_ONESAMP_RESULT=namedtuple('tTEST_ONESAMP_RESULT', ('t-stat', 'p-value', 'effect size'))

def tTEST_ONESAMP(pop, sample, q=0.05, alternative='two-sided'):
  df = len(sample) - 1
  t, p = ttest_1samp(sample, sum(pop)/len(pop))
  print("t-Stat: " + str(t))
  print("p-Value: " + str(p))

  t_crit = scipy.stats.t.ppf(q=1 - q/2,df=df)

  if (p < q):
    d = cohen(sample, pop, ddofB=0)
    print("t-Test proved significant...returning effect size: ", d)
    return tTEST_ONESAMP_RESULT(t, p, d)
  else: 
    print("Not significant.")
    return tTEST_ONESAMP_RESULT(t, p, None)

def tTEST_PAIRED():
   return t, p

def ttest_indsamp():
   return t, p

def _tTest_finish(df, t, alternative):
    """Shared code among all 3 t-test types"""
    if alternative=='less':
        p = scipy.stats.distributions.t.cdf(t, df)
    elif alternative == 'greater':
        p = scipy.stats.distributions.t.sf(t, df)
    elif alternative == 'two-sided':
        p = 2 * scipy.stats.distributions.t.sf(np.abs(t), df)
    else:
        raise ValueError("alternative must be "
                         "'less', 'greater' or 'two-sided'")
   
    return t, p

def ztest_paired():
   return 0

def ztest_ind():
   return 0

Cola=[88,90,92]
ClubSoda=[83,95,87]
Water=[80,82,84]

ANOVA_ONEWAY_RESULT=namedtuple('ANOVA_ONEWAY_RESULT', 
                        ('f-stat', 'p-value', 'effect size'))

def ANOVA_ONEWAY(*samples, q=0.05):
    if len(samples) < 2:
        raise TypeError('at least two inputs are required;'
                        f' got {len(samples)}.')
    
    N=len(samples)

    sum_squares_between=0
    sum_squares_within=0
    for i in range(len(samples)):
        M=mean(samples[i])
        for j in range(len(samples[i])):
            sum_squares_between+=(samples[i][j]-((sum(M))/len(samples[0])))**2
            sum_squares_within+=(samples[i][j]-M)**2
    dfB=len(samples)-1
    dfW=sum([sum(i) for i in samples]) - N
    print(dfB, dfB)

    mean_squares_between=SSB/dfB
    mean_squares_within=SSW/dfW

    f=mean_squares_between/mean_squares_within
    p=scipy.stats.f.cdf(f)
    #fcrit=scipy.stats.f()
    if (p < q):
        partial_eta_squared=sum_squares_between/(sum_squares_between + sum_squares_within)
        print("ANOVA proved significant...returning effect size: ", d)
        return ANOVA_ONEWAY_RESULT(f, p, partial_eta_squared)
    else: 
        print("Not significant.")
        return ANOVA_ONEWAY_RESULT(f, p, None)




ANOVA_ONEWAY(Cola, ClubSoda, Water)