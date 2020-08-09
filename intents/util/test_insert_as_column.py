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
This module contains tests for the functions in insert_as_column.py
"""
import sys
sys.path.append(".")

import pandas
import time
import randstr, random
from util import aspects, enums, insert_as_column

def test_1():
    """
    This test tests the list_index_slicing_passed function of the
    insert_as_column module.
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')

    # selecting only first 20 rows of the table
    table = table.head(20)

    # bool_list contains True/False for each row that passes slicing condition
    bool_list = insert_as_column.list_index_slicing_passed(table, \
        [('Age', enums.Filters.LESS_THAN, 51)])

    print(bool_list)

    expected_bool_list = '[True, False, True, True, False, False, False, False, False, False, True, False, False, True, True, True, False, True, True, False]'

    assert(expected_bool_list == str(bool_list))


def test_2():
    """
    This test tests the list_index_in_topk function of the
    insert_as_column module.
    """
    table = pandas.read_csv('data/data_for_test_aspects/test_1.csv')

    # selecting only first 20 rows of the table
    table = table.head(20)

    # bool_list contains True/False for each row that will it appear in the top-k
    bool_list = insert_as_column.list_index_in_topk(table, 'Age', [], True,
                                                    5,
                                                    slices=[('Age', enums.Filters.LESS_THAN, 51)])
    
    print(bool_list)

    expected_bool_list = '[False, False, True, False, False, False, False, False, False, False, True, False, False, False, True, True, False, False, True, False]'

    assert(expected_bool_list == str(bool_list))

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print('Test cases completed')
