"""This file provides files relating to strings."""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

from worktoy import maybe


def monoSpace(text: str, newLine=None) -> str:
  """Replaces whitespace in the text with a single space. Line breaks may
  be included explicitly in the text using tags such as <br> (default).
  Use second argument 'newLine' to define a string which will be replaced
  with a new line character. To prevent the explicit new line, set the
  second positional argument to False or None."""
  text = text.replace('\n', ' ')
  text = text.replace('\r', ' ')
  while '  ' in text:
    text = text.replace('  ', ' ')
  newLine = maybe(newLine, '<br>')
  if newLine:
    return text.replace(newLine, '\n')
  return text


def removeTrailingSpaces(arg: str) -> str:
  """The removeTrailingSpaces function takes a string and returns it with
  beginning and ending spaces removed."""
  while arg[0] == ' ':
    arg = arg[1:]
  while arg[-1] == ' ':
    arg = arg[:-1]
  return arg


def textBetween(text: str, first: str, last: str) -> str:
  """The textBetween function takes a string as argument along with a pair of
  delimiters. It finds the index of the first delimiter searching from the
  beginning. Then it finds the index of the end delimiter searching from the
  end. It then returns the string contained between them.
  #  Copyright (c) 2023.
  #  Asger Jon Vistisen, All Rights Reserved"""

  firstIndex, lastIndex = 0, len(text)
  for char in text:
    if char == first:
      break
    firstIndex += 1
  for char in reversed([c for c in text]):
    if char == last:
      break
    lastIndex -= 1
  return text[firstIndex: lastIndex]


def stringList(strList: str, separator: str = None) -> list[str]:
  """Allows for creation of list of strings from one long string, which is
  more convenient to type out. First positional argument is the string
  typed out and second is the string used to indicate separation. This
  defaults to ', '.
  For example:
    stringList('one, two, three', ', ') == ['one', 'two', 'three']
    Is True
  """
  return strList.split(maybe(separator, ', '))


def setList(strList: str, separator: str = None) -> set[str]:
  """Same as stringList except returning the set"""
  return set(stringList(strList, separator))


def sevenWords() -> list[str]:
  """Seven words you cannot say on TV"""
  return stringList('shit, piss, fuck, cunt, cocksucker, motherfucker, tits')
