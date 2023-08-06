from .core import raw
from .main import get, get_int, get_ints, get_strs, get_bool

raw.read_env()
for _path in get_strs("ENVPATH", []):
    raw.read_env(_path)

__all__ = ["raw", "get", "get_int", "get_ints", "get_strs", "get_bool"]
