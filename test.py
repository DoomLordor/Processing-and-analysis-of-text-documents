from multiprocessing import Pool
from itertools import repeat


def dec(*args, **kwargs):
    return f(*args, **kwargs)


def f(a, b, c, i=1, d=1):
    return a, b, c, i, d


if __name__ == '__main__':
    a = list(range(10))
    b = list(range(10, 20))
    c = list(range(20, 30))
    i = list(repeat({'d': 2}, 10))
    iter = list(zip(a, b, c, i))
    dec(1, 2, 3, d=2)
    pool = Pool(processes=4)
    e = pool.starmap(dec, iter)
    print(e)
