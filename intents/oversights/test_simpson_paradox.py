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
import sys  
sys.path.append(".")

import pandas

import simpson_paradox
from util.enums import SummaryOperators
from util.enums import Filters

def test_1():
    """
        question :  compare total salary of 'A' and 'B' for year 2019.
     """
    table = pandas.read_csv('data/salary_list_modified.csv')
    query_result = simpson_paradox.simpson_paradox(table, 'salary',
                                                   ['Person name'],
                                                   ['Person name', 'month'],
                                                   ['Person name', 'A', 'B'],
                                                   SummaryOperators.SUM)
    print(query_result)

    expected_result = "['month', 'Person name'] these group of columns have different results than initial columns so you might also look for the given group of columns"
    assert(query_result == expected_result)

def test_2():
    """
        question :  compare avg run for 'MI' and 'CSK' by city.
     """
    table = pandas.read_csv('data/ipl_example.csv')
    query_result = simpson_paradox.simpson_paradox(table, 'run_scored',
                                                   ['team_name', 'city'],
                                                   ['team_name', 'city'],
                                                   ['team_name', 'MI', 'CSK'],
                                                   SummaryOperators.MEAN)
    print(query_result)

    expected_result = "['team_name'] these group of columns have different results than initial columns so you might also look for the given group of columns"
    assert(query_result == expected_result)

print("\ncompare total salary of 'A' and 'B' for year 2019.")
test_1()

print("\ncompare avg run for 'MI' and 'CSK' by city.")
test_2()

print("\nTest cases completed")
