# -*- coding: utf-8 -*-
from six import PY2

if PY2:
    # noinspection PyUnresolvedReferences
    from __builtin__ import long
else:
    # noinspection PyUnresolvedReferences
    from builtins import int as long


def s(a, encoding='utf-8'):
    if PY2:
        if isinstance(a, unicode):
            return a.encode(encoding)
        elif isinstance(a, list):
            a_ = []
            for a_elem in a:
                if isinstance(a_elem, unicode):
                    a_.append(a_elem.encode(encoding))
                else:
                    a_.append(a_elem)
            return a_
        else:
            return a
    else:
        return a


def u(a, encoding='utf-8'):
    if PY2:
        if isinstance(a, str):
            return a.decode(encoding)
        elif isinstance(a, list):
            a_ = []
            for a_elem in a:
                if isinstance(a_elem, str):
                    a_.append(a_elem.decode(encoding))
                else:
                    a_.append(a_elem)
            return a_
        else:
            return a
    else:
        return a
