from enum import Enum
from plum import dispatch
from typing import TypeVar,Union,Generic,List,Tuple
from spire.common import *
#from spire.xls import *
from ctypes import *
import abc

from spire.common.IEnumerator import IEnumerator

T = TypeVar("T", bound=SpireObject)
class IEnumerable (SpireObject, Generic[T]) :
    """

    """
    def __iter__(self)->IEnumerator[T]:
        return self.GetEnumerator()

    def GetEnumerator(self)->IEnumerator[T]:
        """

        """
        dlllib.IEnumerable_GetEnumerator.argtypes=[c_void_p]
        dlllib.IEnumerable_GetEnumerator.restype=c_void_p
        intPtr = dlllib.IEnumerable_GetEnumerator(self.Ptr)
        ret = None if intPtr==None else IEnumerator(intPtr)
        ret._gtype = self.__orig_bases__[0].__args__[0]
        return ret


