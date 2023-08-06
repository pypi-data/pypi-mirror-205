from inspect import signature
import re


class Behaviour:
    NO_SIGNATURE = object()
    PUBLIC = r"[a-zA-Z]\w*"
    PRIVATE = f"_{PUBLIC}"
    SPECIAL = r"__\w+__"
    PUBLIC_AND_SPECIAL = f"({PUBLIC}|{SPECIAL})"

    def __new__(cls, obj):
        return obj if isinstance(obj, cls) else super().__new__(cls)

    def __init__(self, obj):
        if not isinstance(obj, self.__class__):
            self.obj = obj

    def __repr__(self):
        return f"<Behaviour of {repr(self.obj)}>"

    def implemented_by(self, other):
        return self.__class__(other).implements(self)

    def implements(self, other):
        return self.signatures() >= self.__class__(other).signatures()

    def signatures(self, scope=PUBLIC_AND_SPECIAL):
        pattern = re.compile(scope)
        contents = dir(self.obj)
        included = filter(pattern.match, contents)
        candidates = map(self._name_and_attribute, included)
        callables = filter(_callable, candidates)
        return {(name, _safe_signature(func)) for name, func in callables}

    def _name_and_attribute(self, name):
        return name, getattr(self.obj, name)


def _callable(name_and_attribute):
    return callable(name_and_attribute[1])


def _safe_signature(func):
    try:
        return signature(func)
    except ValueError:
        return Behaviour.NO_SIGNATURE
