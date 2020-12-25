from .helpers import gen_rand_poly

def sum_of_roots():
    deg, coeffs, poly = gen_rand_poly(2,7,12)
    q = (f'What is the sum of the roots of the polynomial {poly}?')
    a = -coeffs[deg-1]/coeffs[deg]
    return {'prob': q, 'ans': a}

def product_of_roots():
    deg, coeffs, poly = gen_rand_poly(2,7,12)
    q = (f'What is the product of the roots of the polynomial {poly}?')
    a = coeffs[0]/coeffs[deg]
    return {'prob': q, 'ans': a}
