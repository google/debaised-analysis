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
This module contains the tests for the min_max_date module.
"""
import sys
sys.path.append(".")

import pandas
from util import min_max_date, enums
import date_detection

def test_1():
    """
    Tests the updated column type & order the min_max_date in the
    Company gift shipping dataset.
    """
    # Load the dataset from the csv file
    table = pandas.read_csv('data_for_tests/company_gift_shipping.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {'Order Date': {'type': enums.ColumnTypes.\
    ALL_AMBIGUOUS, 'day_first': None}, 'Shipping Date': {'type': enums.\
    ColumnTypes.CONSISTENT, 'day_first': True}}

    # result contains the updated column type and order dictionary with the
    # min and max values of the dates
    result = min_max_date.update_min_max_date(column_type_and_order, table)

    print(result)
    expected_result = '''{'Order Date': {'type': <ColumnTypes.ALL_AMBIGUOUS: 2>, 'day_first': None, 'min_date': {'day_first_true': '2019-01-04', 'day_first_false': '2019-01-08'}, 'max_date': {'day_first_true': '2020-02-10', 'day_first_false': '2020-10-02'}}, 'Shipping Date': {'type': <ColumnTypes.CONSISTENT: 1>, 'day_first': True, 'min_date': {'day_first_true': '2019-02-04'}, 'max_date': {'day_first_true': '2020-03-14'}}}'''
    assert(expected_result == str(result))

def test_2():
    """
    Tests the updated column type & order the min_max_date in the
    Company gift shipping dataset.
    In this test case the columns are marked as INCONSISTENT & then passed
    to the min_max_date module
    """
    table = pandas.read_csv('data_for_tests/company_gift_shipping.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {'Order Date': {'type': enums.ColumnTypes.\
    INCONSISTENT}, 'Shipping Date': {'type': enums.ColumnTypes.INCONSISTENT}}

    result = min_max_date.update_min_max_date(column_type_and_order, table)
    print(result)
    expected_result = '''{'Order Date': {'type': <ColumnTypes.INCONSISTENT: 3>}, 'Shipping Date': {'type': <ColumnTypes.INCONSISTENT: 3>}}'''
    assert(expected_result == str(result))

def test_3():
    """
    Tests the updated column type & order the min_max_date in the test_1 dataset
    """
    table = pandas.read_csv('data_for_tests/table_1.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {'DATE': {'type': enums.ColumnTypes.INCONSISTENT\
    , 'day_first': None}}

    result = min_max_date.update_min_max_date(column_type_and_order, table)
    print(result)
    expected_result = '''{'DATE': {'type': <ColumnTypes.INCONSISTENT: 3>, 'day_first': None}}'''
    assert(expected_result == str(result))

def test_4():
    """
    Tests the updated column type & order the min_max_date in the test_2 dataset
    """
    table = pandas.read_csv('data_for_tests/table_2.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {'da____t__e': {'type': enums.ColumnTypes.\
    CONSISTENT, 'day_first': True}}

    result = min_max_date.update_min_max_date(column_type_and_order, table)
    print(result)
    expected_result = '''{'da____t__e': {'type': <ColumnTypes.CONSISTENT: 1>, 'day_first': True, 'min_date': {'day_first_true': '1999-12-30'}, 'max_date': {'day_first_true': '2020-12-23'}}}'''
    assert(expected_result == str(result))

def test_5():
    """
    Tests the updated column type & order the min_max_date in the test_3 dataset
    """
    table = pandas.read_csv('data_for_tests/table_3.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {}

    result = min_max_date.update_min_max_date(column_type_and_order, table)
    print(result)
    expected_result = '''{}'''
    assert(expected_result == str(result))

def test_6():
    """
    Tests the updated column type & order the min_max_date in the
    naukri_com dataset
    """
    table = pandas.read_csv('data_for_tests/naukri_com.csv')

    # Hardcode the date columns in the table
    column_type_and_order = {'Crawl Timestamp': {'type': enums.ColumnTypes.\
    CONSISTENT, 'day_first': False}}
    result = min_max_date.update_min_max_date(column_type_and_order, table)
    print(result)
    expected_result = '''{'Crawl Timestamp': {'type': <ColumnTypes.CONSISTENT: 1>, 'day_first': False, 'min_date': {'day_first_false': '2019-07-04'}, 'max_date': {'day_first_false': '2019-08-06'}}}'''
    assert(expected_result == str(result))

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

print(test_6.__doc__)
test_6()

print('Test cases completed')
