from .helpers import *


def crt_easy():
    m1 = random.randint(2,15)
    m2 = random.randint(m1+1, 25)
    r = random.randint(1,m1)
    q = f'What is the smallest positive integer n such that n is {m1-r} mod {m1} and {m2-r} mod {m2}?'
    a = lcm(m1,m2)-r
    return {'prob': q, 'ans': a}

def dec_to_bin():
    n = random.randint(9,100)
    q = f'Convert {n} to binary.'
    a = int(str(bin(n))[2:])
    return {'prob': q, 'ans': a}