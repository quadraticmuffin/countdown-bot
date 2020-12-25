from .helpers import *

def num_factors():
    p1 = random.randint (1, 1000)
    q = f'The number {p1} has how many positive factors?'
    a = len([x for x in range(1,p1**2 + 1) if p1%x==0])
    return q,a

def count_divisible():
    p1 = random.randint(1,1000)
    p2 = random.randint(p1+100,10000)
    p3 = random.randint(2,20)
    q=(f'How many integers between {p1} and {p2} are divisible by {p3}?')
    a=len([x for x in range(p1,p2+1) if x%p3==0])
    return {'prob': q, 'ans': a}
