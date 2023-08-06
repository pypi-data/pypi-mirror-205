from typing import overload

from .core import UNDEFINED, DEFAULT, raw


@overload
def get(name: str) -> str:
    ...


@overload
def get(name: str, default: str | None) -> str | None:
    ...


def get(name: str, default: str | DEFAULT = UNDEFINED):
    return raw.str(name, default=default)


@overload
def get_int(name: str) -> int:
    ...


@overload
def get_int(name: str, default: int | None) -> int | None:
    ...


def get_int(name: str, default: int | DEFAULT = UNDEFINED):
    return raw.int(name, default=default)


@overload
def get_bool(name: str) -> bool:
    ...


@overload
def get_bool(name: str, default: bool | None) -> bool | None:
    ...


def get_bool(name: str, default: bool | DEFAULT = UNDEFINED):
    return raw.bool(name, default=default)


@overload
def get_strs(name: str) -> list[str]:
    ...


@overload
def get_strs(name: str, default: list[str] | None) -> list[str] | None:
    ...


def get_strs(name: str, default: list[str] | DEFAULT = UNDEFINED):
    return raw.list(name, default=default)


@overload
def get_ints(name: str) -> list[int]:
    ...


@overload
def get_ints(name: str, default: list[int] | None) -> list[int] | None:
    ...


def get_ints(name: str, default: list[int] | DEFAULT = UNDEFINED):
    return raw.list(name, default=default, subcast=int)
