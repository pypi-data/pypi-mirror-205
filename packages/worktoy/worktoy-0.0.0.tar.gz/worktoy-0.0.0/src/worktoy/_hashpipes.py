"""HashPipes provide functions for hashing arbitrary objects"""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

from typing import Any


def isIterable(arg: Any) -> bool:
  """Tests if the argument given is iterable. This should probably be
  replaced by a builtin function or a standard method, but I cannot be
  bothered to search through documentation any further. Please note that
  strings despite supporting for-loops, are not regarded as iterables in
  this context."""
  if isinstance(arg, str):
    return False
  try:
    for _ in arg:
      return True
  except TypeError as _:
    return False


def flattenIterables(*args, **kwargs) -> list[Any]:
  """Flattens the argument and returns them in a combined list. """
  flatArgs = []
  for (key, val) in kwargs.items():
    flatArgs.append(key)
    flatArgs.append(val)
  for arg in args:
    if isIterable(arg):
      for item in arg:
        flatArgs.append(item)
    else:
      flatArgs.append(arg)
  if any([isIterable(arg) for arg in flatArgs]):
    return flattenIterables(*flatArgs)
  return flatArgs


def any2Str(*args, **kwargs) -> list[str]:
  """Casts all arguments as strings and returns the strings in a list"""
  out = []
  for arg in flattenIterables(*args, **kwargs):
    out.append(str(arg))
  return out


def str2Int(arg: str, divisor: int = None) -> int:
  """Computes an integer from the given string"""
  base = bytes(arg, encoding='utf-8')
  out = int.from_bytes(base, 'big')
  if divisor is None:
    return out
  if divisor > 1:
    return out % divisor
  return out


def intersection(*args) -> list:
  """For any number of containers, this method transforms them to sets and
  the returns a list of items being members in each."""
  argIters = [arg for arg in args if isIterable(arg)]
  argSets = [set(arg) for arg in argIters]
  base = argSets.pop()
  for s in argSets:
    base &= s
  return list(base)
