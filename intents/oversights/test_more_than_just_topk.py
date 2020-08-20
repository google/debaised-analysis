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
This module contains the tests for more_than_just_topk.py

In these tests first the topk is called and the result table is
created with k = -1, then the result table is used to test the
oversights detection.
"""
import sys
sys.path.append(".")

import pandas
import topk
from oversights import more_than_just_topk

def generate():
    """
    Generates data required for both test_1 & test_2
    dataset used - https://www.contextures.com/xlSampleData01.html

    Top-k query - "Find the top-k Item with maximum UnitCost"

    This function takes stores the result table of the query without
    applying the k condition & stores the result in a csv file.
    """
    table = pandas.read_csv('data/data_for_test_more_than_just_topk/sheet1.csv')
    result_table = topk.topk_results(table, 'UnitCost',
                                     ['Item'], False, -1)[0]
    result_table.to_csv('data/data_for_test_more_than_just_topk/result_table.csv',
                        index=False)

def test_1():
    """
    Tests the more_than_just_topk based on the result table generated & stored
    in data/data_for_test_more_than_just_topk/result_table for the query -
    Top-10 Item based on unit costs.

    In the results the UnitCost of 11th & 12th entry is same as the 10th one,
    so the more_than_just_topk function will suggest to look at the next 2 entries.
    """
    result_table = pandas.read_csv('data/data_for_test_more_than_just_topk/result_table.csv')
    k = 10
    metric = 'UnitCost'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    # suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)
    suggestions = more_than_just_topk.more_than_just_topk(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'change_list': {'topKLimit': 11}, 'suggestion': 'value of UnitCost in some rows after the top-k is similar to the Kth row', 'confidence_score': 0.0, 'oversight': <Oversights.MORE_THAN_JUST_TOPK: 3>}"""

    assert(expected_suggestions == str(suggestions))

def test_2():
    """
    Tests the more_than_just_topk based on the result table generated & stored
    in data/data_for_test_more_than_just_topk/result_table for the query -
    Top-12 Item based on unit costs.

    In the results the UnitCost of 11th & 12th entry is same as the 10th one,
    so the more_than_just_topk function will suggest to look at the next 2 entries.
    """
    result_table = pandas.read_csv('data/data_for_test_more_than_just_topk/result_table.csv')
    k = 12
    metric = 'UnitCost'

    # The data should be already sorted
    assert(result_table[metric].is_monotonic_decreasing)

    # suggestions = oversights.looking_at_tails.looking_at_tails(result_table, k, metric)
    suggestions = more_than_just_topk.more_than_just_topk(result_table, k, metric)

    print(suggestions)
    expected_suggestions = """{'change_list': {'topKLimit': 13}, 'suggestion': 'value of UnitCost in some rows after the top-k is similar to the Kth row', 'confidence_score': 0.0, 'oversight': <Oversights.MORE_THAN_JUST_TOPK: 3>}"""

    assert(expected_suggestions == str(suggestions))

def test_3():
    """
    This test verifies the division by zero case when standard deviation is zero
    Having all the elements will have standard deviation zero
    The table is hardcoded as it's a rare case.
    """
    result_table = pandas.DataFrame()
    result_table['Students'] = pandas.Series(['A', 'B', 'C', 'D'])
    result_table['Marks'] = pandas.Series([100, 100, 100, 10])
    metric = 'Marks'
    k = 3

    suggestions = more_than_just_topk.more_than_just_topk(result_table, k, metric)

    print(suggestions)

    expected_suggestions = 'None'

    assert(expected_suggestions == str(suggestions))



# print('Generating top-k results')
# print(generate.__doc__)
# generate()

print('Running tests')

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print('Test cases completed')