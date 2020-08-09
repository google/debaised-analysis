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

"""This module will return the list of results that pass the slicing
and those which are in the top-k.

The functions use the index of the table to check which all rows in
the initial tbale are present in the final table.
reset_index is not called, as the indices in the original table are
needed.
"""

from util import aspects

def list_index_slicing_passed(table, slices,  **kwargs):
    """
    This function returns a list of Bools, 1 for each row,
    denoting that did the row pass the slicing & date range condition

    0 indexing is followed.

    Args :
        table : Type-Pandas dataframe
            Contents of the sheets
        slices : Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Returns :
        List of True/False, list[i] denotes that ith row
        passes the slicing condition or not
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    bool_list = [False for _ in range(table.shape[0])]

    table = aspects.slice_table(table, slices, reset_index=False)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name,
                                     date_format,
                                     reset_index=False)
    for index in list(table.index):
        bool_list[index] = True

    return bool_list

def list_index_in_topk(table, metric, dimensions, is_asc, k, **kwargs):
    """
    This function returns the list of the rows in the original table
    that are in the top-k after applying all the operations.

    0 indexing is followed.

    Args: (Same as top-k only summary_operator is required
           as when grouping is done insert_as_column option would 
           not be given)
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort,
            and in the case when grouping has to be done,
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'top 5 batsman according to runs', dimension is 'batsman'.
            When summary_operator is not None, we group by dimensions.
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        k: Type-int
            It is the number of entries to be taken. Also k = -1 means taking
            all entries
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
    
    Returns :
        List of True/False, list[i] denotes that ith row
        is in the top-k or not
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    bool_list = [False for _ in range(table.shape[0])]

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, date_format,
                                     reset_index=False)

    table = aspects.slice_table(table, slices, reset_index=False)
    
    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    table = table.sort_values(by=[metric], ascending=is_asc, kind='mergesort')

    # selecting only the top-k
    if k != -1:
        table = table.head(k)

    for index in list(table.index):
        bool_list[index] = True

    return bool_list
