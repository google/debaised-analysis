"""
Copyright 2020 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

https://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
"""This module contains the enumerations"""

import enum

class SummaryOperators(enum.Enum):
    """The attributes of this class like summary_operators.SUM ,
    .MEAN , etc. are enum members

    The operators are listed in an arbitrary order.
    And currently sum, mean, count, max, min, standard deviation, variance,
    first, last, count unique are used.
    sum, max, min are replaced by summation, maximum, mimimum respectively as,
    the are keywords in python.
    """
    SUM = 1
    MEAN = 2
    COUNT = 3
    MAX = 4
    MIN = 5
    STD = 6
    VAR = 7
    FIRST = 8
    LAST = 9
    DISTINCT = 10
    MEDIAN = 11
    PROPORTION_OF_SUM = 12
    PROPORTION_OF_COUNT = 13

class Granularities(enum.Enum):
    """The attributes of this class like granularity.DAILY ,
    .ANNUALY , etc. are enum members

    The granularities are listed in an arbitrary order.
    And currently annually, monthly, daily, hourly are used.
    """
    ANNUALLY = 1
    MONTHLY = 2
    DAILY = 3
    HOURLY = 4

class Filters(enum.Enum):
    """The attributes of this class like Filters.EQUALTO ,
    .NOTEQUALTO , etc. are enum members

    The Filters are listed in an arbitrary order.
    And currently =, !=, <, <=, >, >=, in, not in are used
    """
    EQUAL_TO = 1
    NOT_EQUAL_TO = 2
    LESS_THAN = 3
    LESS_THAN_EQUAL_TO = 4
    GREATER_THAN = 5
    GREATER_THAN_EQUAL_TO = 6
    IN = 7
    NOT_IN = 8

class Oversights(enum.Enum):
    """The attributes of this class like Oversights.MEAN_VS_MEDIAN ,
    .TOPK_VS_OTHERS , etc. are enum members

    The Oversights are listed in an arbitrary order.
    """
    DUPLICATES_IN_TOPK = 1
    TOPK_WHEN_LESS_THAN_K_PRESENT = 2
    MORE_THAN_JUST_TOPK = 3
    REGRESSION_TO_THE_MEAN = 4
    LOOKING_AT_TAILS_TO_FIND_CAUSES = 5
    TOPK_VS_OTHERS = 6
    MEAN_VS_MEDIAN = 7
    SIMPSONS_PARADOX = 8
    TOP_DOWN_ERROR = 9
    BENCHMARK_SET_TOO_DIFFERENT = 10
    ATTRIBUTION_WITH_HIDDEN_NEGATIVES = 11
    CALENDAR_VS_EXPERIENCE_IN_TIME_SERIES = 12
