"""This module contains the enumerations"""

import enum

class SummaryOperators(enum.Enum):
    """This attributes of this class like summary_operators.sum , .mean , etc. are enum members

    The operators are listed in an arbitrary order.
    And currently sum, mean, count, max, min, standard deviation, variance,
    first, last, count unique are used.
    sum, max, min are replaced by summation, maximum, mimimum respectively as,
    the are keywords in python.
    """
    summation = 1
    mean = 2
    count = 3
    maximum = 4
    minimum = 5
    std = 6
    var = 7
    first = 8
    last = 9
    distinct = 10

class Granularities(enum.Enum):
    """This attributes of this class like granularity.daily , .annualy , etc. are enum members

    The granularities are listed in an arbitrary order.
    And currently annually, monthly, daily, hourly are used.
    """
    annually = 1
    monthly = 2
    daily = 3
    hourly = 4
