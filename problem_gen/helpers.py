import random
import math

def check_integer(nums):
    for num in nums:
        if num != int(num): 
            raise TypeError('Argument must be an integer')
def check_nonneg_int(nums):
    try:
        check_integer(nums)
    except:
        raise TypeError('Argument must be a nonnegative integer')
    for num in nums:
        if num < 0:
            raise ValueError('Argument must be a nonnegative integer')
def check_pos_int(nums):
    try:
        check_integer(nums)
    except:
        raise TypeError('Argument must be a positive integer')
    for num in nums:
        if num < 1:
            raise ValueError('Argument must be a positive integer')

def gen_rand_poly(deg_lower_limit = 1, deg_upper_limit = 10, coeff_limit = 10):
    """
    Generates a random polynomial with integer coefficients.
    """
    deg = random.randint(deg_lower_limit,deg_upper_limit)
    coeffs = [random.randint(-coeff_limit, coeff_limit) for _ in range(deg+1)]

    # Never have 0 as leading coefficient
    if coeffs[deg] == 0:
        coeffs[deg] = 1

    def term(coeff, d):
        if coeff == 0:
            return ''
        elif d == 0:
            return (' + ' if coeff>0 else ' - ') + str(abs(coeff))
        elif d == 1:
            return (' + ' if coeff>0 else ' - ') + (f'{abs(coeff)}x' if abs(coeff)!=1 else 'x')
        elif d == deg:
            return ('' if coeff>0 else '-') + (f'{abs(coeff)}x^{d}' if abs(coeff)!=1 else f'x^{d}')
        else:
            return (' + ' if coeff>0 else ' - ') + (f'{abs(coeff)}x^{d}' if abs(coeff)!=1 else f'x^{d}')

    terms = [term(coeffs[d], d) for d in range(deg+1)]
    return deg, coeffs, ''.join([terms[d]for d in range(deg,-1,-1)]).strip('+ ')

def lcm(a,b):
    check_pos_int([a,b])
    out = a
    while out % b != 0:
        out += a
    return out

def gcf(a,b):
    check_pos_int([a,b])
    if a != round(a) or b != round(b):
        raise TypeError('Argument must be a positive integer')
    if a < 1 or b < 1:
        raise ValueError('Argument must be a positive integer')
    [x,y] = sorted([a,b])
    while (y % x != 0):
        y -= x
        [x,y] = sorted([x,y])
    return x

def factorial(n):
    check_nonneg_int([n])
    if n == 0:  return 1
    return n * factorial(n-1)

def choose (n, k):
    check_nonneg_int([n,k])
    if n < k: return 0
    if k > n/2: 
        k = n-k
    numer, denom = 1, 1
    for i in range(k):
        numer *= n-i
        denom *= i+1
    return int(numer/denom)

