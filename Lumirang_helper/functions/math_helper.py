import math


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    if n < 0:
        raise ValueError('Only positive values are acceptable')
    return math.floor(n*multiplier + 0.5) / multiplier
