"""Collection of general utilities each too small to merit dedicated
publication."""
#  Copyright (c) 2023. Asger Jon Vistisen All Rights Reserved
from __future__ import annotations

from ._maybe import maybe, maybeType, maybeTypeNamed, typeArgs, searchKeys
from ._typenames import DiscFile, DiscList, DiscDict
from ._parseerror import ParseError
from ._discio import parseFilePath, imgLoad
from ._discio import saveTextFile, loadTextFile, saveDisk, loadDisk
from ._hashpipes import intersection
from ._hashpipes import isIterable, flattenIterables, any2Str, str2Int
from ._stringtools import sevenWords, textBetween
from ._stringtools import stringList, monoSpace, removeTrailingSpaces
