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
from util import aspects, enums
import insert_as_column

def test_1():
    """
    This test checks the formulas for the EQUAL TO filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_1.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Grade'] = 'B'
    cheader_to_clabel['Date of Test'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slice_condition = ('Grade',enums.Filters.EQUAL_TO,'A')
    slices = [slice_condition]

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where (B=\\'A\\')\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where (B=\\'A\\')\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))


def test_2():
    """
    This test checks the formulas for the NOT EQUAL TO filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_1.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Grade'] = 'B'
    cheader_to_clabel['Date of Test'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slice_condition = ('Grade',enums.Filters.NOT_EQUAL_TO,'A')
    slices = [slice_condition]

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where (B!=\\'A\\')\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where (B!=\\'A\\')\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))

def test_3():
    """
    This test checks the formulas for the LESS THAN filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_2.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Marks'] = 'B'
    cheader_to_clabel['Date of Test'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slice_condition = ('Marks',enums.Filters.LESS_THAN,70)
    slices = [slice_condition]

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where (B<70)\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where (B<70)\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))

def test_4():
    """
    This test checks the formulas for the IN filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_3.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Grade'] = 'B'
    cheader_to_clabel['Date of Test'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slice_condition = ('Grade',enums.Filters.IN,['A','B'])
    slices = [slice_condition]

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where ((B=\\'A\\') or (B=\\'B\\'))\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))

def test_5():
    """
    This test checks the formulas for the IN along with LESS THAN filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_4.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Marks'] = 'B'
    cheader_to_clabel['Grade'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slice_condition_of_IN = ('Grade',enums.Filters.IN,['A','B'])
    slice_condition_of_LESS_THAN = ('Marks',enums.Filters.LESS_THAN,70)
    slices = [slice_condition_of_IN, slice_condition_of_LESS_THAN]

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where ((C=\\'A\\') or (C=\\'B\\')) and (B<70)\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))


def test_6():
    """
    This test checks the formulas for date range filter
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_5.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Score'] = 'B'
    cheader_to_clabel['Date of Test'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    slices = []

    date_column_name = 'Date of Test'
    date_range = ('2019-01-21','2019-01-24')

    list_of_formulas = insert_as_column.insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, slices=slices ,date_column_name=date_column_name , date_range=date_range )

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:C2, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A3:C3, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A4:C4, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A5:C5, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A6:C6, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A7:C7, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))', '=NOT(ISNA(QUERY(A8:C8, \"select A where (C >= date \\'2019-01-21\\' and C <= date \\'2019-01-24\\')\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))

def test_7():
    """
    This test checks the formulas of top-k column
    """
    table = pandas.read_csv('data/data_for_test_insert_as_column/test_6.csv')

    cheader_to_clabel = {}
    cheader_to_clabel['Student Name'] = 'A'
    cheader_to_clabel['Grade'] = 'B'
    cheader_to_clabel['Marks'] = 'C'
         
    row_start_label = 2
    row_end_label = 8

    column_start_label = 'A'
    column_end_label = 'C'

    filter_column_label = 'D'

    metric = 'Marks'
    is_asc = True
    k = 3

    list_of_formulas = insert_as_column.insert_as_column_topk_column(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, filter_column_label, metric, is_asc, k)

    for formula in list_of_formulas :
        print(formula)

    expected_list_of_formulas = "['=NOT(ISNA(QUERY(A2:D2, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A3:D3, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A4:D4, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A5:D5, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A6:D6, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A7:D7, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))', '=NOT(ISNA(QUERY(A8:D8, \"select A where (D=true) and (C >= \"&large(filter(C2:C8,D2:D8=TRUE),3)&\")\")))']"

    assert(expected_list_of_formulas == str(list_of_formulas))

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

print('Test cases completed')