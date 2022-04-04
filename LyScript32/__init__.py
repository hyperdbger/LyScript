# -*- coding: utf-8 -*-
import socket,struct
from ctypes import *

class MyStruct(Structure):
    _pack_ = 1
    _fields_ = [
        ("Command_String_A", c_char * 256),
        ("Command_String_B", c_char * 256),
        ("Command_String_C", c_char * 256),
        ("Command_String_D", c_char * 256),
        ("Command_String_E", c_char * 256),
        ("Command_int_A",c_int),
        ("Command_int_B", c_int),
        ("Command_int_C", c_int),
        ("Command_int_D", c_int),
        ("Command_int_E", c_int),
        ("Count", c_int),
        ("Flag", c_int),
    ]
