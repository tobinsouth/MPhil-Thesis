import numba
from numba import jit, prange
import numpy as np
import math
import nltk

from ProcessEntropy.Preprocessing import *

@jit(nopython = True)
def get_all_self_lambdas(source, lambdas):
    """ 
	Internal function.

	Finds the Lambda value for each index in the source.

	Lambda value denotes the longest subsequence of the source, 
	starting from the index, that in contained contigiously in the source,
	before the index.
    
    Args:        
        source: Arry of ints, usually corresponding to hashed words.
            
        lambdas: A premade array of length(target), usually filled with zeros. 
            Used for efficiency reasons.
        
    Return:
        A list of ints, denoting the value for Lambda for each index in the target. 
    
    """
    
    N = len(source)
    
    for i in prange(1, N): 
    
        # The target process is everything ahead of i.
        t_max = 0
        c_max = 0

        for j in range(0, i): # Look back at the past
            if source[j] == source[i]: # Check if matches future's next element
                c_max = 1
                for k in range(1,min(N-i, i-j)): # Look through more of future
                    if source[j+k] != source[i+k]:
                        break
                    else:
                        c_max = c_max+1

                if c_max > t_max:
                    t_max = c_max 

        lambdas[i] = t_max+1
            
    return lambdas



def self_entropy_rate(source, get_lambdas = False):
    """
    Args:
        source: The source is an array of ints.
    Returns: 
        The non-parametric estimate of the entropy rate based on match lengths.
        
        
    $$
    \hat{h}(S)=\frac{N \log _{2} N{\sum_{i=1}^{N \Lambda_{i}(S)}
    $$
    
    This is described mathematically in [1] as,
     
    [1] I. Kontoyiannis, P.H. Algoet, Yu.M. Suhov, and A.J. Wyner. Nonparametric entropy 
    esti mation for stationary processes and random fields, with applications to English text. 
    IEEE Transactions on Information Theory, May 1998.
        
    """
    
    N = len(source)
    source = np.array(source)
    lambdas = np.zeros(N)
    lambdas = get_all_self_lambdas(source, lambdas)
    
    if get_lambdas:
        return lambdas
    else:
        return N*math.log(N,2) / np.sum(lambdas)


def text_array_self_entropy(token_source):
	"""
	This is a wrapper for `self_entropy_rate' to allow for raw text to be used.

	Args:
		token_source: A list of token strings (hint: a list of words).

	Returns: 
        The non-parametric estimate of the entropy rate based on match lengths.

	"""
	return self_entropy_rate(np.array([fnv(word)  for word in token_source]))

def tweet_self_entropy(tweets_source):
	"""
	This is a wrapper for `self_entropy_rate' to allow for raw tweets to be used.

	Args:
		tweets_source: A list of long strings (hint: a list of tweets). 
			If it detects that you have added a list of time, tweet pairs 
			(as in timeseries_cross_entropy) it will recover.

	Returns: 
        The non-parametric estimate of the entropy rate based on match lengths.

	"""
	source = []

	if type(tweets_source[0]) == tuple:
		# This is for the case of a 
		for time, text in tweets_source:
			source.extend(tweet_to_hash_array(text))
	else:
		for text in tweets_source:
			source.extend(tweet_to_hash_array(text))

	return self_entropy_rate(source)

        
