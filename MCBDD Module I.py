# -*- coding: utf-8 -*-
"""
Created on Tue Mar 11 19:01:22 2025

@author: Lauris
"""

import matplotlib.pyplot as plt
import numpy as np


# 0.00001 <= P(I) <= .5 
p_infected = 0.005

# P( Negative Test | Healthy)
specificity = [.99, .999, .9999, .99999]

# P( Positive Test | Infected)
sensitivity = .99


def bayes(p_infected=0.05, specificity=[.99, .999, .9999, .99999],
          sensitivity=.99):
    p_positive_given_healthy = 1 - np.array(specificity)
    p_healthy = 1 - p_infected
    
    return (sensitivity * p_infected) / (sensitivity * p_infected + 
                                         p_positive_given_healthy * p_healthy)

#I made the x-axis evenly spaced since the specificity values would be too 
#                                       close together to see the data points.
plt.plot(bayes(p_infected, specificity, sensitivity), 'bo', label="Bayes's Theorem")
plt.ylim(0, 1.1)
plt.xlabel("different specifisities (x-values corresponds to the array index)")
plt.ylabel("P( Infected | positive test)")


# =============================================================================
# Integer Exlpanation
# =============================================================================

#Some hypothetical population
population = 100000

#                            Truth 
#             | True Positive  | False Positive |
# Test Result |----------------|----------------|
#             | False Negative | True Negative  |
#
# Using the data from above we can fill this table with numbers:
    
infected = int(population * p_infected)
healthy = population - infected

true_positives = int(sensitivity * infected)
false_negatives = infected - true_positives

true_negatives = np.array(specificity) * healthy
true_negatives = true_negatives.astype(int)
false_positives = healthy - true_negatives
 
print(infected)
print(healthy)
print(true_positives, false_negatives)
print(true_negatives, false_positives)

# this should return the population in each case
print(true_positives + false_negatives + true_negatives + false_positives)
#
# Therefore we fill the table with the results for a specificity of .99.

#                           Truth 
#             | True Positive  | False Positive |
#             |     4950       |      950       |
# Test Result |----------------|----------------|
#             | False Negative | True Negative  |
#             |      50        |     94050      | 
#
# Therefore P( Infected | Positive Test) = true positives / (true positives + false positives) 
#                                        = 4950 / (4950 + 950) = 83.89%
# This is consistent with the results above 


p_infected_given_positive = true_positives / (false_positives + true_positives)

plt.plot(p_infected_given_positive, '-', color="green", label="Integer calculation")
plt.ylim(0, 1.1)
plt.xlabel("different specifisities (x-values corresponds to the array index)")
plt.ylabel("P( Infected | positive test)")
plt.legend()


