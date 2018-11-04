from dataclasses import dataclass, fields
from typing import List, Tuple, Dict, Set, Union, Optional


def _is_type(ty, expect):
    if not hasattr(ty, "_subs_tree"):
        return False
    return ty._subs_tree()[0] is expect


def _params(ty):
    return ty._subs_tree()[1:]


def _is_opt(ty):
    if not _is_type(ty, Union):
        return False
    return _params(ty)[1] is type(None)


def punp(cls):
    def unpack(ty, val):
        if ty is Wrapper:
            return ty(val)
        elif _is_opt(ty):
            return None if val is None else unpack(_params(ty)[0], val)
        elif _is_type(ty, Union):
            for t in _params(ty):
                try:
                    return unpack(t, val)
                except:
                    continue
            raise ValueError(f'compatible type not found')
        elif _is_type(ty, List):
            return [unpack(_params(ty)[0], v) for v in val]
        elif _is_type(ty, Set):
            return set(unpack(_params(ty)[0], v) for v in val)
        elif _is_type(ty, Tuple):
            return tuple(unpack(_params(ty)[i], v) for i, v in enumerate(val))
        elif _is_type(ty, Dict):
            return {unpack(_params(ty)[0], k):unpack(_params(ty)[1], v) for k, v in val.items()}
        else:
            return ty(val)

    class Wrapper(cls):
        def __init__(self, obj):
            self._unpack_dict(obj)

        def _unpack_dict(self, obj):
            if not isinstance(obj, dict):
                raise ValueError(f'expect dict but found: {obj.__class__}')

            for f in fields(self):
                self._unpack_one(f, obj)

        def _unpack_one(self, f, obj):
            if not _is_opt(f.type) and not f.name in obj:
                raise KeyError(f'member "{f.name}" not found')

            val = obj.get(f.name)

            try:
                val = unpack(f.type, val)
            except Exception as e:
                raise ValueError(f'couldn\'t unpack for "{f.name}": {e}')

            setattr(self, f.name, val)

    return Wrapper
