from enum import Enum

class Stats(Enum):
    MOMENT = 1
    CDF = 2
    PDF = 3
    CMOMENT = 4
    CCDF = 5
    CPDF = 6
    SIMULATION = 7
    TIMING = 8
    SAVE = 9

    @classmethod
    def is_member(cls, value):
        return value in cls
