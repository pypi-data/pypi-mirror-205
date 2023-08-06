"""This file contains a number of type names and type aliases for use in
type hinting."""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

import os
import sys
from typing import NoReturn, TypeAlias, Any, Union


def _modules() -> NoReturn:
  """No unused imports!"""
  return [os, sys]


CallMeMaybe = type(_modules)
DiscDict: TypeAlias = dict[str, Any]
DiscList: TypeAlias = list[Any]
DiscFile: TypeAlias = Union[DiscDict, DiscList]
