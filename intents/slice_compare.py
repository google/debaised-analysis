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

"""This module contains the slice-compare intent.
The slice-compare intent can give the result so that user can easily
compare the data according to the way user want.
Also it supports some operations like cropping based on date range,
slicing(removing rows that do not follow the conditions), group by.
Some of the operations are optional.
"""

from util import aspects
from oversights.simpson_paradox import simpson_paradox
from util.enums import SummaryOperators, Filters
# from oversights.benchmark_set_too_different
import pandas

def slice_compare(table, metric, dimensions, all_dimension, all_metric,
                  slice_compare_column, summary_operator, **kwargs):
    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.
    Some of the oversights considered in this intent are-
    1. simpson's paradox
    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which grouping will be done.
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            'compare batsman A and B according to total_runs',
             dimension is 'batsman'. we group by dimensions.
        all_dimension: Type-list of str
            It is the list of dimension columns in the initial table
        all_metric: Type-list of str
            It is the list of metric columns in the initial table
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
        slice_compare_column: Type-list of string
            first element denotes the column name by which we will do comparision.
            rest elements will the value belongs to that column by which we
            will compare the slices.
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done
    Returns:
        The function will return both suggestions and the results in a tuple.
        (results, suggestions)
        results: Type - pandas dataframe, The results of the intended slice-compare
        suggestions: Type - List of strings, List of suggestions.
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    if slice_compare_column[2] == "*":
        result_table = _slice_compare_results_for_all(table.copy(), metric, 
                                                      dimensions.copy(),
                                                      slice_compare_column, 
                                                      summary_operator,
                                                      slices = slices,
                                                      date_column_name = date_column_name,
                                                      date_range = date_range, 
                                                      date_format = date_format)
        suggestions = []
        # below function will be implemented
        # if SummaryOperators.MEAN == summary_operator or SummaryOperators.MEDIAN == summary_operator:
        #     suggestions = benchmark_set_too_different(table)
        return (result_table, suggestions)

    result_table = _slice_compare_results(table.copy(), metric, dimensions.copy(),
                                          slice_compare_column, 
                                          summary_operator,
                                          slices = slices,
                                          date_column_name = date_column_name,
                                          date_range = date_range, 
                                          date_format = date_format)

    suggestions = []

    simpson_paradox_suggestion = simpson_paradox(table, metric, dimensions,
                                                 all_dimension,
                                                 slice_compare_column,
                                                 summary_operator,
                                                 date_column_name = date_column_name,
                                                 date_range = date_range, 
                                                 date_format = date_format)
    if len(simpson_paradox_suggestion) > 0:
        suggestions.append(simpson_paradox_suggestion)

    return (result_table, suggestions)

def _slice_compare_results(table, metric, dimensions,
                           slice_compare_column,
                           summary_operator, **kwargs):
    """This function will implement the slice-compare intent

    Also removes the tuples that do not lie in the given date range.
    The arguments 'table, metric,dimension,slices_compare_column,
    summary_operator' are not optional, so they are passed as it is,
    'date_range','slices' will be passed in kwargs.
    If some the optional args are None(not passed),
    it is assumed that we don't have to apply them.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which grouping will be done.
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            'compare batsman A and B according to total_runs'
             dimension is 'batsman'. we group by dimensions.
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
        slice_compare_column: Type-list of string
            first element denotes the column name by which we will do comparision.
            rest elements will the value belongs to that column by which we
            will compare the slices.
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done

    Returns:
        The function will return the `table(a pandas dataframe object)`
        after applying the intent on the
        given `table(a pandas dataframe object)``

    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     date_format)

    if slices == None:
        slices = [(slice_compare_column[0], Filters.IN, 
                  [slice_compare_column[1], slice_compare_column[2]])]
    else:
        slices.append((slice_compare_column[0], Filters.IN, 
                      [slice_compare_column[1], slice_compare_column[2]]))
    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    # slice_compare_column should be the last element of the group
    # so that groupby will show them together for every grouping
    dimensions.remove(slice_compare_column[0])
    dimensions.append(slice_compare_column[0])
    table = aspects.group_by(table, dimensions, summary_operator)

    return table

def _slice_compare_results_for_all(table, metric, dimensions, 
                                   slice_compare_column, 
                                   summary_operator, **kwargs):
    
    """This function will implement the slice-compare intent

    Also removes the tuples that do not lie in the given date range.
    The arguments 'table, metric,dimension,slices_compare_column,
    summary_operator' are not optional, so they are passed as it is,
    'date_range', 'slices' will be passed in kwargs.
    If some the optional args are None(not passed),
    it is assumed that we don't have to apply them.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which grouping will be done.
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            'compare batsman A and B according to total_runs'
             dimension is 'batsman'. we group by dimensions.
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
        slice_compare_column: Type-list of string
            first element denotes the column name by which we will do comparision.
            rest elements will the value belongs to that column by which we
            will compare the slices.
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done

    Returns:
        The function will return the `table(a pandas dataframe object)`
        after applying the intent on the
        given `table(a pandas dataframe object)``

    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     date_format)

    table = aspects.slice_table(table, slices)

    required_columns = dimensions.copy()
    required_columns.append(metric)
    table = aspects.crop_other_columns(table, required_columns)

    required_table_for_one = aspects.slice_table(table.copy(), [(slice_compare_column[0], 
                                                               Filters.EQUAL_TO, 
                                                               slice_compare_column[1])])
    
    required_table_for_all = table.copy()
    required_table_for_all[slice_compare_column[0]] = '*'

    updated_table = pandas.concat([required_table_for_all, required_table_for_one])

    result_table = aspects.group_by(updated_table, dimensions, summary_operator)

    return result_table