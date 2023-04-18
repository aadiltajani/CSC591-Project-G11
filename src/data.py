import math
import utility as util
from cols import COLS
from collections.abc import Iterable
from utility import *
import update

class DATA:

    def __init__(self, src, rows = None):
        self.rows = []
        self.cols = None
        add = lambda t: update.row(self, t)
        if isinstance(src, str):
            util.readCSV(src, add)
        else:
            self.cols = COLS(src.cols.names)
            if rows:
                for row in rows:
                    add(row)

    def read(self, sFile):
        data = DATA()
        callback = lambda t: update.row(data, t)
        util.readCSV(sFile, callback)
        return data

    def clone(self, data, ts = None):

        data1 = update.row(DATA(), data.cols.names)
        for t in (ts or []):
            update.row(data1, t)
        return data1
