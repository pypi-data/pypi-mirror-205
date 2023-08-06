import os
import platform
from ctypes import *
from typing import TypeVar,Union,Generic,List,Tuple

def LoadLib(path:str):
    fileExists = os.path.isfile(path)
    if fileExists:
        return cdll.LoadLibrary(path)
    return None


os_name = platform.system()
os_version = platform.release()
if os_name == "Windows":
    lib_pathXls = r'.\Spire.Xls.Base.dll'
    lib_pathDoc = r'.\Spire.Doc.Base.dll'
    lib_pathPdf = r'.\Spire.Pdf.Base.dll'
    lib_pathPpt = r'.\Spire.Presentation.Base.dll'
elif os_name == "Linux":
    lib_pathXls = r'./Spire.Xls.Base.so'
    lib_pathDoc = r'.\Spire.Doc.Base.so'
    lib_pathPdf = r'.\Spire.Pdf.Base.so'
    lib_pathPpt = r'.\Spire.Presentation.Base.so'
elif os_name =="Darwin":
    lib_pathXls = r'./Spire.Xls.Base.dylib'
    lib_pathDoc = r'.\Spire.Doc.Base.dylib'
    lib_pathPdf = r'.\Spire.Pdf.Base.dylib'
    lib_pathPpt = r'.\Spire.Presentation.Base.dylib'
else:
    lib_pathXls = r'.\Spire.Xls.Base.dll'
    lib_pathDoc = r'.\Spire.Doc.Base.dll'
    lib_pathPdf = r'.\Spire.Pdf.Base.dll'
    lib_pathPpt = r'.\Spire.Presentation.Base.dll'
dlllibXls = None
dlllibXls = LoadLib(lib_pathXls)
dlllibDoc = LoadLib(lib_pathDoc)
dlllibPdf = LoadLib(lib_pathPdf)
dlllibPpt = LoadLib(lib_pathPpt)
dlllib = dlllibXls
if dlllibXls != None:
    dlllib = dlllibXls
elif dlllibDoc != None:
    dlllib = dlllibDoc
elif dlllibPdf != None:
    dlllib = dlllibPdf
elif dlllibPpt != None:
    dlllib = dlllibPpt

def GetDllLibXls():
    #if dlllibXls != None:
    #    dlllibXls = LoadLib(lib_pathXls)
    #if dlllibXls != None:
    dlllib = dlllibXls
    return dlllibXls;

def GetDllLibDoc():
    #if dlllibDoc == None:
    #    dlllibDoc = LoadLib(lib_pathDoc)
    #if dlllibDoc != None:
    dlllib = dlllibDoc
    return dlllibDoc;
def GetDllLibPdf():
    #if dlllibPdf == None:
    #    dlllibPdf = LoadLib(lib_pathPdf)
    #if dlllibPdf != None:
    dlllib = dlllibPdf
    return dlllibPdf;
def GetDllLibPpt():
    #if dlllibPpt == None:
    #    dlllibPpt = LoadLib(lib_pathPpt)
    #if dlllibPpt != None:
    dlllib = dlllibPpt
    return dlllibPpt;
def ChangeHandleToXls():
    GetDllLibXls()
def ChangeHandleToDoc():
    GetDllLibDoc()
def ChangeHandleToPdf():
    GetDllLibPdf()
def ChangeHandleToPpt():
    GetDllLibPpt()


from spire.common.SpireObject import SpireObject

from spire.common.Common import IntPtrArray
from spire.common.Common import GetObjVectorFromArray
from spire.common.Common import GetVectorFromArray
from spire.common.Common import GetIntPtrArray
from spire.common.Common import GetByteArray
from spire.common.Common import GetIntValue


from spire.common.CultureInfo import CultureInfo
from spire.common.Boolean import Boolean
from spire.common.Byte import Byte
from spire.common.Char import Char
from spire.common.Int16 import Int16
from spire.common.Int32 import Int32
from spire.common.Int64 import Int64
from spire.common.PixelFormat import PixelFormat
from spire.common.Size import Size
from spire.common.SizeF import SizeF
from spire.common.Point import Point
from spire.common.PointF import PointF
from spire.common.Rectangle import Rectangle
from spire.common.RectangleF import RectangleF
from spire.common.Single import Single
from spire.common.TimeSpan import TimeSpan
from spire.common.UInt16 import UInt16
from spire.common.UInt32 import UInt32
from spire.common.UInt64 import UInt64
from spire.common.ImageFormat import ImageFormat
from spire.common.Stream import Stream
from spire.common.License import License
from spire.common.Color import Color
from spire.common.Image import Image
from spire.common.Bitmap import Bitmap
from spire.common.DateTime import DateTime
from spire.common.Double import Double
from spire.common.EmfType import EmfType
from spire.common.Encoding import Encoding
from spire.common.FontStyle import FontStyle
from spire.common.Font import Font
from spire.common.GraphicsUnit import GraphicsUnit
from spire.common.ICollection import ICollection
from spire.common.IDictionary import IDictionary
from spire.common.IEnumerable import IEnumerable
from spire.common.IEnumerator import IEnumerator
from spire.common.IList import IList
from spire.common.String import String
