import abc
from typing import TypeVar, Union, Generic, List,Tuple
from enum import Enum
from plum import dispatch
from ctypes import *

from spire.common import *


class IntPtrArray(Structure):
    _fields_ = [
        ('size',c_int),
        ('data',(c_uint)*20)
    ]
class IntPtrWithTypeName(Structure):
    _fields_ = [
        ('intPtr',(c_uint)*2),
        ('typeName', c_wchar_p)
    ]
def GetIntPtrArray(intPtrArray:IntPtrArray):
    ret = []
    size = intPtrArray.size
    if(size == 0):
        return ret
    r0 = intPtrArray.data[0] + (intPtrArray.data[1]<<32)
    if(size <= 10):
        ret.append(r0)
        for i in range(1,size):
            ret.append(intPtrArray.data[i*2] + (intPtrArray.data[i*2+1]<<32))
    else:
        r = cast(r0, POINTER(c_void_p))
        for i in range(1,size):
            ret.append(r[i-1])

    return ret

def GetByteArray(intPtrArray:IntPtrArray):
    ret = []
    size = intPtrArray.size
    if(size == 0):
        return ret
    r0 = intPtrArray.data[0] + (intPtrArray.data[1]<<32)
    r = cast(r0, POINTER(c_void_p))
    for i in range(0,size):
        ret.append(r[i])

    return ret

T = TypeVar("T")
def GetVectorFromArray(intPtrArray:IntPtrArray, t):
    ret:List = []
    #obj = self.__orig_bases__[0].__args__[0]
    #intPtr = GetByteArray(intPtrArr);
    size = intPtrArray.size
    if(size == 0):
        return ret
    r0 = intPtrArray.data[0] + (intPtrArray.data[1]<<32)
    r = cast(r0, POINTER(t))
    for i in range(0,size):
        ret.append(r[i])
    return ret

def GetObjVectorFromArray(intPtrArray:IntPtrArray, t):
    ret:List = []
    arr = GetIntPtrArray(intPtrArray)
    size = intPtrArray.size
    if(size == 0):
        return ret
    for i in range(0,size):
        obj = t(arr[i])
        ret.append(obj)
    return ret

def GetIntValue(ptr:c_void_p, valueName:str, paraValues:str)->int:
    dlllib.Spire_GetIntValue.argtypes=[c_void_p, c_wchar_p, c_wchar_p]
    dlllib.Spire_GetIntValue.restype=c_int
    ret = dlllib.Spire_GetIntValue(ptr, valueName, paraValues)
    return ret
def GetObjIntPtr(ptr:c_void_p, valueName:str, paraValues:str)->c_void_p:
    dlllib.Spire_GetIntValue.argtypes=[c_void_p, c_wchar_p, c_wchar_p]
    dlllib.Spire_GetIntValue.restype=c_void_p
    ret = dlllib.Spire_GetIntPtr(ptr, valueName, paraValues)
    return ret

