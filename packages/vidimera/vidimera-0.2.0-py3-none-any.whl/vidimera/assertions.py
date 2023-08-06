from .behaviour import Behaviour


def assert_implements(obj, expected):
    if delta := Behaviour(obj).implements(expected):
        return delta
    else:
        raise AssertionError(str(delta))
