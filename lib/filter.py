# coding: utf-8
import time

class Filter:
    @staticmethod
    def ts2dt(value):
        format = '%Y-%m-%d %H:%M:%S'
        value = time.localtime(int (value))
        dt = time.strftime(format, value)
        return dt
