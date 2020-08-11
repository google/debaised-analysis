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
"""
This module contains tests for rank_oversights.py
"""
import sys
sys.path.append(".")

from util import enums, oversights_order, rank_oversights

def test_1():
    """
    The list of suggestions for top-k intent.
    Hardcodes the list of suggestions & applies ranking on it
    """
    suggestion1 = {'oversight' : enums.Oversights.REGRESSION_TO_THE_MEAN}
    suggestion2 = {'oversight' : enums.Oversights.DUPLICATES_IN_TOPK}
    suggestion3 = {'oversight' : enums.Oversights.TOPK_VS_OTHERS}

    suggestions = [suggestion1, suggestion2, suggestion3]

    order = oversights_order.ORDER_IN_TOPK

    ranked_suggestions = rank_oversights.rank_oversights(suggestions, order)

    print(ranked_suggestions)

    expected_ranked_suggestions = [suggestion2, suggestion1, suggestion3]

    assert(expected_ranked_suggestions == ranked_suggestions)

def test_2():
    """
    The list of suggestions for slice-compare intent.
    Hardcodes the list of suggestions & applies ranking on it
    """
    suggestion1 = {'oversight' : enums.Oversights.BENCHMARK_SET_TOO_DIFFERENT}
    suggestion2 = {'oversight' : enums.Oversights.TOP_DOWN_ERROR}
    suggestion3 = {'oversight' : enums.Oversights.MEAN_VS_MEDIAN}

    suggestions = [suggestion1, suggestion2, suggestion3]

    order = oversights_order.ORDER_IN_SLICE_COMPARE

    ranked_suggestions = rank_oversights.rank_oversights(suggestions, order)

    print(ranked_suggestions)

    expected_ranked_suggestions = [suggestion3, suggestion2, suggestion1]

    assert(expected_ranked_suggestions == ranked_suggestions)


def test_3():
    """
    The list of suggestions for Top-k intent.
    Hardcodes the list of suggestions & applies ranking on it

    This test checks for an empty list of suggestions
    """

    suggestions = []

    order = oversights_order.ORDER_IN_TOPK

    ranked_suggestions = rank_oversights.rank_oversights(suggestions, order)

    print(ranked_suggestions)

    expected_ranked_suggestions = []

    assert(expected_ranked_suggestions == ranked_suggestions)



print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print('Test cases completed')
