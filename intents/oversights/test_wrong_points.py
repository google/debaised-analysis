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
This module contains tests for the wrong_points oversight
"""

import sys  
sys.path.append(".")

import pandas
from oversights import wrong_points
import data.spider_eval.evaluation


def test_1():
    """
    Tests the wrong point oversight on a table in which entries represent 
    NO data.
    """
    table = pandas.DataFrame()
    table['A'] = pandas.Series([1, -99, -99, 0, 2, 54, 2, 4, -99, -99, 2, -99, -99])

    suggestion = wrong_points.wrong_points(table)

    print(suggestion)

    expected_suggestion = """{'oversight': <Oversights.WRONG_POINTS: 12>, 'suggestion': 'Some cells in the table may be wrongly written, maybe to represent NO data', 'confidence_score': 0.46153846153846156}"""

    assert(expected_suggestion == str(suggestion))

def test_2():
    """
    Tests the wrong point oversight on a table in which there a an extra 0
    in one of the entries.
    """
    table = pandas.DataFrame()
    table['Person'] = pandas.Series(['Aman', 'Naman', 'Manan', 'Binod', 'Banan'])
    table['Height'] = pandas.Series([140, 130, 149, 150, 1300])

    suggestion = wrong_points.wrong_points(table)

    print(suggestion)

    expected_suggestion = """{'oversight': <Oversights.WRONG_POINTS: 12>, 'suggestion': 'Some of the entry in the table may have been wrongly typed as they excede the sum of other entries'}"""

    assert(expected_suggestion == str(suggestion))


def test_3():
    """
    This test tests the wrong point oversight detection on a randomly
    picked table from the spyder dataset.
    """
    table = data.spider_eval.evaluation.get_table('farm', 'farm_competition')

    suggestion = wrong_points.wrong_points(table)

    print(suggestion)

    expected_suggestion = 'None'

    assert(expected_suggestion == str(suggestion))



print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print('Test case completed')
