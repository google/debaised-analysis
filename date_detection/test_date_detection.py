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
This module contains the tests for the date_detection module.
"""

import pandas
import date_detection

def test_1():
    """
    Detect the date columns in table_1.csv
    dates are in such format - '02-02-2001'
    """
    table = pandas.read_csv('data_for_tests/table_1.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'DATE': {'type_str': 'Inconsistent', 'day_first': None}}'''
    assert(expected_result == str(result))

def test_2():
    """
    Detect the date columns in table_2.csv
    Date column name is 'da____t__e'
    """
    table = pandas.read_csv('data_for_tests/table_2.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'da____t__e': {'type_str': 'Constient', 'day_first': True}}'''
    assert(expected_result == str(result))

def test_3():
    """
    Detect the date columns in table_3.csv
    Inconsistent date column is present. Two dates exists -
    '23-12-2020', '14-27-2016'
    """
    table = pandas.read_csv('data_for_tests/table_3.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{}'''
    assert(expected_result == str(result))


def test_4():
    """
    Detect the date columns in naukri_com.csv
    Example date present - '2019-07-06 09:20:22 +0000'
    """
    table = pandas.read_csv('data_for_tests/naukri_com.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'Crawl Timestamp': {'type_str': 'Constient', 'day_first': False}}'''
    assert(expected_result == str(result))

def test_5():
    """
    Detect the date columns in orders.csv
    Example date present - '10/13/2010'
    """
    table = pandas.read_csv('data_for_tests/orders.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'Order Date': {'type_str': 'Constient', 'day_first': False}}'''
    assert(expected_result == str(result))

def test_6():
    """
    Detect the date columns in austin_weather.csv
    Example date present - '2013-12-21'
    """
    table = pandas.read_csv('data_for_tests/austin_weather.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'Date': {'type_str': 'Constient', 'day_first': False}}'''
    assert(expected_result == str(result))

def test_7():
    """
    Detect the date columns in austin_weather.csv
    Here 2 date columns are present with different formats.
    """
    table = pandas.read_csv('data_for_tests/table_7.csv')
    result = date_detection.detect(table)
    print(result)
    expected_result = '''{'date': {'type_str': 'Constient', 'day_first': True}, ' date__new': {'type_str': 'Constient', 'day_first': False}}'''
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

print(test_7.__doc__)
test_7()
