# -*- coding: utf-8 -*-
from six import PY2


def u(a):
    if isinstance(a, str):
        if PY2:
            return a.decode('utf-8')
        else:
            return a
    elif isinstance(a, list):
        if PY2:
            a_ = []
            for a_elem in a:
                if isinstance(a_elem, str):
                    a_.append(a_elem.decode('utf-8'))
                else:
                    a_.append(a_elem)
            return a_
        else:
            return a
    else:
        return a
