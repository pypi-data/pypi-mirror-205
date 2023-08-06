"""This file contains a number of functions relating to saving and loading
from disc"""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

import json
import os
from typing import Optional, NoReturn

from PIL import Image

from worktoy import maybe, DiscFile, searchKeys, typeArgs, ParseError


def imgLoad(fid: str, fmt: str = None, **kwargs) -> Optional[Image.Image]:
  """Why is the following code necessary outside the module??"""
  fmt = maybe(kwargs.get('fmt', None), fmt, 'RGBA')
  if not os.path.exists(fid):
    imgPath = os.getenv('IMAGEPATH')
    dirName, fileName = os.path.split(fid)
    if imgPath and dirName != imgPath:
      return imgLoad(os.path.join(imgPath, fileName))
    e = """Could not locate file %s!""" % (fileName)
    if kwargs.get('strict', True):
      raise FileNotFoundError(e)
    return None
  with Image.open(fid) as im:
    return im.convert(fmt)


def loadDisk(name: str, **kwargs) -> DiscFile | None:
  """Loads the file at the given name assuming it to be a json file. The
  function raises FileNotFoundError unless the keyword argument strict to
  False."""
  if os.path.exists(name):
    with open(name, 'r') as f:
      return json.load(f, )
  if kwargs.get('strict', True):
    e = 'Failed to find file named %s!' % (name)
    raise FileNotFoundError(e)
  return None


def saveDisk(data: DiscFile, name: str, **kwargs) -> NoReturn:
  """Saves data to name. The function creates the file if it does not
  already exist, and raises an error if it does, unless the keyword
  argument 'overwrite' is set to True."""
  if os.path.exists(name) and not kwargs.get('overwrite', False):
    e = 'File named %s already exists and overwrite flag was set to False!'
    raise FileExistsError(e % (name))
  with open(name, 'w') as f:
    json.dump(data, f, indent=4, )


def parseFilePath(*args, **kwargs) -> str:
  """Parses arguments to a particular filePath."""
  filePathKwarg = searchKeys('filePath', 'fullPath', **kwargs)
  fileNameKwarg = searchKeys('fileName', 'fid', **kwargs)
  dirNameKwarg = searchKeys('dirName', 'dir', **kwargs)
  strArgs = typeArgs(str, *args, padLength=2, padChar=None)
  fileNameArg, dirNameArg = strArgs
  dirName = maybe(dirNameKwarg, dirNameArg, None)
  fileName = maybe(fileNameKwarg, fileNameArg, None)
  if dirName is None or fileName is None:
    if filePathKwarg is None:
      raise ParseError(str)
    if os.path.isfile(filePathKwarg):
      return filePathKwarg
    dirName = os.path.dirname(filePathKwarg)
    if os.path.isdir(dirName):
      return filePathKwarg
    raise NotADirectoryError('Given directory: %s not found!' % dirName)
  filePath = os.path.join(dirName, fileName)
  return parseFilePath(filePath=filePath)


def loadTextFile(*args, **kwargs) -> str | bool:
  """Loads a text-file named fileName from dirName. Alternatively, provide
  the name of an environment variable at the keyword argument 'env'."""
  filePath = parseFilePath(*args, **kwargs)
  try:
    if not os.path.isfile(filePath):
      if kwargs.get('strict', True):
        raise FileNotFoundError('Could not find %s' % filePath)
      else:
        return False
    with open(filePath, 'r', encoding='utf-8') as f:
      return f.read()
  except UnicodeEncodeError as e:
    print(filePath)


def saveTextFile(obj: str, *args, **kwargs) -> NoReturn:
  """Saves given object to specified file"""
  filePath = parseFilePath(*args, **kwargs)
  with open(filePath, 'w', encoding='utf-8') as f:
    return f.write(obj)
