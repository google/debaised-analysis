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
This module contains tests for the weighted_mean_with_different_weights
module.
"""

import sys  
sys.path.append(".")

import pandas
from oversights.weighted_mean_with_different_weights import weighted_mean_with_different_weights 

def test_1():
    """
    This test initializes the dataframe & checks for the oversight
    in it.
    The user queried for Show average 'GDP'. So, we will suggest the 
    user for Mean of 'GDP' weighted by 'Percentage Population'.
    """
    table = pandas.DataFrame()
    table['Country'] = ['India', 'Pakistan', 'USA', 'China', 'Bhutan']
    table['GDP'] = [12, 23, 42, 12, 53]
    table['Population percentage'] = [20, 12, 38, 23, 7]
    metric = 'GDP'

    suggestion = weighted_mean_with_different_weights(table, metric)

    print(suggestion)

    expected_suggestion = """{'oversight_name': 'Weighted mean with different weights', 'suggestion': "Consider using ['Population percentage'] as the weights for computing weighted mean.", 'is_column_level_suggestion': True, 'col_list': ['Population percentage']}"""

    assert(expected_suggestion == str(suggestion))


def test_2():
    """
    This test initializes the dataframe & checks for the oversight
    in it.
    Let's say the user used the suggestion in test_1 & queried for mean
    of GDP wieghted by percentage population. But this time there is another
    column 'Proportion of Working population'
    """
    table = pandas.DataFrame()
    table['Country'] = ['India', 'Pakistan', 'USA', 'China', 'Bhutan']
    table['GDP'] = [12, 23, 42, 12, 53]
    table['Population percentage'] = [20, 12, 38, 23, 7]
    table['Proportion of Working population'] = [.1, .2, .3, .25, .15]
    metric = 'GDP'
    weight_col  = 'Population percentage'

    suggestion = weighted_mean_with_different_weights(table, metric,
                                                      weight_col=weight_col)

    print(suggestion)

    expected_suggestion = """{'oversight_name': 'Weighted mean with different weights', 'suggestion': "Consider using ['Proportion of Working population'] as the weights for computing weighted mean.", 'is_column_level_suggestion': True, 'col_list': ['Proportion of Working population']}"""

    assert(expected_suggestion == str(suggestion))

def test_3():
    """
    This tests the case when no suggestion needs to be given.
    The user queried for Show average 'P'. So, we will suggest the 
    user for Mean of 'GDP' weighted by 'Percentage Population'.
    """
    table = pandas.DataFrame()
    table['Country'] = ['India', 'Pakistan', 'USA', 'China', 'Bhutan']
    table['GDP'] = [12, 23, 42, 12, 53]
    table['Population'] = [2023254, 1221345, 321548, 2453134, 71245]
    metric = 'Population'

    suggestion = weighted_mean_with_different_weights(table, metric)

    print(suggestion)

    expected_suggestion = 'None'

    assert(expected_suggestion == str(suggestion))


print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print('Test cases completed')
