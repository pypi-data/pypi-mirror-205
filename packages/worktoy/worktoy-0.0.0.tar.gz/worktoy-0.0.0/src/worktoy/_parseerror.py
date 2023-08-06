"""ParseError is a subclass Exception raised by parser functions when
they fail to parse arguments to the target type."""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations


class ParseError(Exception):
  """ParseError is a subclass Exception raised by parser functions when
  they fail to parse arguments to the target type."""

  def __init__(self, type_: type) -> None:
    self._type = type_

  def __str__(self) -> str:
    """String representation of the error"""
    return """Failed to parse arguments to %s!""" % (self._type)
