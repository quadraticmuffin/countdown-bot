import random
import math
import pickle


####################
# HELPER FUNCTIONS #
####################

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

############
# PROBLEMS #
############

def num_factors():
    p1 = random.randint (1, 1000)
    q = f'The number {p1} has how many positive factors?'
    a = len([x for x in range(1,p1**2 + 1) if p1%x==0])
    return {'q': q, 'a': a}

def count_divisible():
    p1 = random.randint(1,100)
    p2 = random.randint(p1+10,1000)
    p3 = random.randint(2,20)
    q=(f'How many integers between {p1} and {p2} inclusive are divisible by {p3}?')
    a=len([x for x in range(p1,p2+1) if x % p3 == 0])
    return {'q': q, 'a': a}

def crt_easy():
    m1 = random.randint(2,15)
    m2 = random.randint(m1+1, 25)
    r = random.randint(1,m1)
    q = f'What is the smallest positive integer n such that n is {m1-r} mod {m1} and {m2-r} mod {m2}?'
    a = lcm(m1,m2)-r
    return {'q': q, 'a': a}

def dec_to_bin():
    n = random.randint(9,100)
    q = f'Convert {n} to binary.'
    a = int(str(bin(n))[2:])
    return {'q': q, 'a': a}

def sum_of_roots():
    deg, coeffs, str_ = gen_rand_poly(2,7,12)
    q = (f'What is the sum of the roots of the polynomial {str_}?')
    a = -coeffs[deg-1]/coeffs[deg]
    return {'q': q, 'a': a}

def product_of_roots():
    deg, coeffs, str_ = gen_rand_poly(2,7,12)
    q = (f'What is the product of the roots of the polynomial {str_}?')
    a = coeffs[0]/coeffs[deg]
    return {'q': q, 'a': a}

def infinite_series():
    rd = random.randint(2,6)
    rn = random.randint(1,rd-1)
    r = rn/rd

    a1 = random.randint(1,100) * rd
    a3 = a1*(r**2)
    a3 = f'{a3:.2f}' if a3 != int(a3) else int(a3)

    q=(f'Find the sum of the infinite geometric series that starts '
        f'{a1}, {int(a1*r)}, {a3},...')
    a = a1/(1-r)

    return {'q': q, 'a': a}

all_probs = [num_factors, count_divisible, crt_easy, 
    dec_to_bin, sum_of_roots, product_of_roots, infinite_series]
