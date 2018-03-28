import re, math
from datetime import date


def myround(n,offset):
    scale = int(-math.floor(math.log10(abs(n))))
    if scale <= 0:
        scale = 1
    scale = scale + offset
    factor = 10**scale
    val = str(math.floor(abs(n)*factor)/factor)
    if offset == 1: val = val + '0'
    return val

def format_signal(s,e,p):
    return {'symbol': s,
            'exchanges': ', '.join(map(str, e)),
            'price': myround(p, 2),
            'stoplost': myround(p - p * 0.1, 1),
            'short': myround(p + p * 0.1, 1),
            'mid': myround(p + p * 0.3, 1),
            'long': myround(p + p * 0.5, 1),
            'data': date.today().strftime('%d/%m/%Y')
    }