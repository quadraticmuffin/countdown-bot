import random

def problems():
    return [infinite_series]

def infinite_series():
    p3 = random.randint(2,6)
    p1 = random.randint(1,100) * p3
    p2 = random.randint(1,p3-1)
    a3 = p1*(p2**2)/(p3**2)
    a3 = f'{a3:.2f}' if a3 != int(a3) else int(a3)
    q=(f'Find the sum of the infinite geometric series that starts '
        f'{p1}, {int(p1*p2/p3)}, {a3},...')
    a = p1/(1-p2/p3)
    return {'prob': q, 'ans': a}