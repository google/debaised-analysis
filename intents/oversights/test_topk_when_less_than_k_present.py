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
This module contains the tests for the topk_when_less_than_k_present
module
"""

import sys  
sys.path.append(".")

import pandas
from oversights import topk_when_less_than_k_present

def test_1():
    """
    This test will test the case when the oversight should not be
    given.
    The result_table is hardcoded and then sent to the oversights
    layer.
    """
    # Hardcoding the results of the top-k for the query -
    # Top-5 Students with maximum marks
    metric = 'marks'
    k = 5

    result_table = pandas.DataFrame()
    result_table['Students'] = pandas.Series(['A', 'B', 'C', 'D', 'E'])
    result_table['marks'] = pandas.Series([10, 9, 8, 7, 6])

    # The data should be already sorted in descreasing order
    assert(result_table[metric].is_monotonic_decreasing)

    suggestion = topk_when_less_than_k_present.topk_when_less_than_k_present(result_table,
    	                                                                     k)

    print(suggestion)

    expected_suggestion = """None"""

    assert(str(suggestion) == expected_suggestion)

def test_2():
    """
    This test will test the case when the oversight should be
    given.
    The result_table is hardcoded and then sent to the oversights
    layer.
    The results contain only 5 entries & k = 6 so the suggestion
    should be returned
    """
    # Hardcoding the results of the top-k for the query -
    # Top-6 Students with maximum marks
    metric = 'marks'
    k = 6

    result_table = pandas.DataFrame()
    result_table['Students'] = pandas.Series(['A', 'B', 'C', 'D', 'E'])
    result_table['marks'] = pandas.Series([10, 9, 8, 7, 6])

    print(result_table)

    # The data should be already sorted in descreasing order
    assert(result_table[metric].is_monotonic_decreasing)

    suggestion = topk_when_less_than_k_present.topk_when_less_than_k_present(result_table,
    	                                                                     k)

    print(suggestion)

    expected_suggestion = """{'suggestion': 'Instead of 6 only 5 rows are present in the results', 'oversight_name': 'Top10 when 9 are present'}"""

    assert(str(suggestion) == expected_suggestion)

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print('Test cases completed')
