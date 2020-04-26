# contains different functions for fitting data
"""
natural exponential fit
c is the number of days when the virus should have started spreading
"""


def exponential_fit(self, x, a, b, c):  # ,d):
    v = a * np.exp(b * (x + c))  # +d
    return v  # a*np.exp(b*(x+c)) #a*np.exp(b*x + c)
