# -*- coding: utf-8 -*-
from six import PY2


def u(a):
    if isinstance(a, str):
        if PY2:
            return a.decode('utf-8')
        else:
            return a
    else:
        return a
