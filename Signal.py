"""
    -- coding: utf-8 --
    @Author: codeking
    @Data : 2022/5/3 19:20
    @File : Signal.py
"""
from PySide6.QtCore import QObject, Signal


class MySignal(QObject):
    GenerateNums=Signal()

my_signal=MySignal()