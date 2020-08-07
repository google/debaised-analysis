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
This module contains tests for the functions in aspects.py
Currently the tests are only for the slicing aspect - to
check it's time complexity.
"""
import sys
sys.path.append(".")

import pandas
import time
import randstr, random
from util import aspects, enums

def generate_1():
    """
    This function hardcodes a pandas dataframe containing 1 Million rows &
    3 columns, and stores it as a csv file in ../data/data_for_test_aspects/.
    Columns = [Name, Age, Gender]
    Around half of the rows would be Gender = Male, and such rows will be placed
    at odd row indices.
    Args:
    Returns:
    Raises:
    """
    number_of_rows = 1000000
    map_gender = {0 : 'Female', 1: 'Male'}

    # Generating a list of random strings as Names
    list_names = [randstr.randstr(16) for row in range(number_of_rows)]

    # Generating a list of random integers between 1 - 100 as Ages
    list_age = [random.randint(1, 100) for row in range(number_of_rows)]

    list_gender = [map_gender[row % 2] for row in range(number_of_rows)]

    # Generating a list of random 'Male' / 'Female'
    table = pandas.DataFrame({'Name' : list_names,
                              'Age' : list_age,
                              'Gender' : list_gender})

    table.to_csv('/data/data_for_test_aspects/test_1.csv', index=False)

def test_1():
    """
    Situation : This test will check the time complexity of the drop
                aspect.
                Alternate rows are dropped in this test case.
                The drop aspect should work in O(number_of_rows *
                average_bytes_per_column). And not in O(number_of_rows *
                number_of_rows * average_bytes_per_column).
                This test checks if the slice_table aspect actually works in
                the desired time complexiy.
    Args:
    Returns:
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')

    # noting the calling time of the slice function
    start_time = time.time()

    table = aspects.slice_table(table, [('Gender', enums.Filters.EQUAL_TO,
                                         'Female')])

    # noting the end return time of the slice function
    end_time = time.time()

    time_taken = end_time - start_time
    print('Execution Time ', time_taken)

    assert(time_taken <= 20)

def test_2():
    """
    Situation : This test will check the time complexity of the drop
                aspect.
                Rows with age > 50 will be dropped, so around half of the
                rows will be dropped.
                The drop aspect should work in O(number_of_rows *
                average_bytes_per_column). And not in O(number_of_rows *
                number_of_rows * average_bytes_per_column).
                This test checks if the slice_table aspect actually works in
                the desired time complexiy.
    Args:
    Returns:
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')

    # noting the calling time of the slice function
    start_time = time.time()

    table = aspects.slice_table(table, [('Age', enums.Filters.LESS_THAN, 51)])

    # noting the end return time of the slice function
    end_time = time.time()

    time_taken = end_time - start_time
    print('Execution Time ', time_taken)

    assert(time_taken <= 20)


def test_3():
    """
    Situation : This tests the median aspect.
                In the same randomly generated dataset calculate the median
                age group by gender
    Args:
    Returns:
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')

    result_table = aspects.group_by(table, ['Gender'], enums.SummaryOperators.MEDIAN)

    print(result_table)

    expected_result = """   Gender  Age
0  Female   50
1    Male   51"""

    assert(result_table.to_string() == expected_result)

def test_4():
    """ Test for summary operator = PROPORTION_OF_COUNT
    Proportion of count of gender for each race/ethnicity
    Dataset used : https://www.kaggle.com/spscientist/students-performance-in-exams
    Args:
    Returns:
    """
    table = pandas.read_csv('data/data_for_test_aspects/student_performance.csv')

    result_table = aspects.group_by(table, ['race/ethnicity'], 
                             enums.SummaryOperators.PROPORTION_OF_COUNT)
    
    result_table = aspects.crop_other_columns(result_table, ['race/ethnicity', 'gender'])
    
    # Sum of proportion column should be(close to) 1.0
    assert(result_table['gender'].sum() == 1.0)

    print(result_table)

    expected_result_table = """  race/ethnicity  gender
0        group A   0.089
1        group B   0.190
2        group C   0.319
3        group D   0.262
4        group E   0.140"""

    assert(expected_result_table == result_table.to_string())

def test_5():
    """ Test for summary operator = PROPORTION_OF_SUM
    Proportion of sum of reading score for each race/ethnicity
    Dataset used : https://www.kaggle.com/spscientist/students-performance-in-exams
    Args:
    Returns:
    """
    table = pandas.read_csv('data/data_for_test_aspects/student_performance.csv')

    result_table = aspects.group_by(table, ['race/ethnicity'], 
                             enums.SummaryOperators.PROPORTION_OF_SUM)
    
    result_table = aspects.crop_other_columns(result_table, ['race/ethnicity', 'reading score'])
    
    # Sum of proportion column should be(close to) 1.0
    assert(float(format(result_table['reading score'].sum(), '.5f')) == 1)

    print(result_table)

    expected_result_table = """  race/ethnicity  reading score
0        group A       0.083216
1        group B       0.185011
2        group C       0.318698
3        group D       0.265263
4        group E       0.147812"""

    assert(expected_result_table == result_table.to_string())

# print(generate_1.__doc__)
# generate_1()

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print(test_4.__doc__)
test_4()

print(test_5.__doc__)
test_5()

print('Test cases completed')
