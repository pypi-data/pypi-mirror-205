"""This file contains the 'maybe' function along with similar and derived
ones."""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

from typing import Any


def maybe(*args, ) -> Any:
  """The maybe function is a None-aware function implementing null
  coalescence behaviour similarly to the ?? operator from the language which
  shall not be named. Given an arbitrary number of positional arguments,
  maybe returns the first argument encountered that is different from None.
  If all positional arguments are None, None is return.
  #  Copyright (c) 2023.
  #  Asger Jon Vistisen All Rights Reserved"""
  for arg in args:
    if arg is not None:
      return arg
  return None


def maybeTypeNamed(type_: str, *args) -> Any:
  """Returns the first positional argument whose type is named type_. If
  no such argument is found, None is returned."""
  for arg in args:
    if type_ in [arg.__class__.__name__, arg.__class__.__qualname__]:
      return arg
  return None


def maybeType(type_: type, *args) -> Any:
  """Returns the first positional argument whose type is type_. If type_
  is a string, maybeTypeNamed defined above is called instead."""
  if isinstance(type_, str):
    return maybeTypeNamed(type_, *args)
  for arg in args:
    if isinstance(arg, type_):
      return arg
  if type_ is float:
    return maybeType(int, *args)


def typeArgs(type_: type, *args, **kwargs) -> list[Any]:
  """Returns all positional arguments belonging to given 'type'.
  Keyword Arguments
    Keyword: padLength
      Pads the output list to padLength
    Keyword: padChar
      Character used by padding defined above. Default character is None."""

  if type_ is float:
    type_ = (float, int)
  out = [arg for arg in args if isinstance(arg, type_)]
  padChar = kwargs.get('padChar', None)
  padLength = kwargs.get('padLength', len(out))
  while len(out) < padLength:
    out.append(padChar)
  return out[:padLength]


def searchKeys(*args, **kwargs) -> Any:
  """Searches the given keyword arguments for all positional arguments of
  type string returning the first one found. If no match can be found, None
  is returned instead."""
  lowerKeys = {}
  for (key, val) in kwargs.items():
    lowerKeys |= {key.lower(): val}
  for arg in typeArgs(str, *args):
    res = lowerKeys.get(arg.lower(), None)
    if res is not None:
      return res
  return None
