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
from oversights.simpsons_paradox import simpsons_paradox
from oversights.benchmark_set_too_different import benchmark_set_too_different
from oversights.top_down_error import top_down_error
from util.enums import SummaryOperators, Filters
import pandas

def slice_compare(table, metric, all_dimensions, all_metric,
                      slice_compare_column, slice1, slice2,
                               summary_operator, **kwargs):
    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.
    Also, if summary operator is applied, the name of metric column is
    renamed to "<summary operator> of metric".
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
        all_dimensions: Type-list of str
            It is the list of dimension columns in the initial table
        all_metric: Type-list of str
            It is the list of metric columns in the initial table
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        day_first: Type-str
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
    day_first = kwargs.get('day_first', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    if slice2 == "*":
        result_table = _slice_compare_results_for_all(table, metric,
                                                      slice_compare_column,
                                                      slice1, slice2, 
                                                      summary_operator,
                                                      slices = slices,
                                                      dimensions = dimensions,
                                                      date_column_name = date_column_name,
                                                      date_range = date_range, 
                                                      day_first = day_first)
        suggestions = []

        if summary_operator == SummaryOperators.MEAN or summary_operator == SummaryOperators.MEDIAN:
            suggestions = benchmark_set_too_different(table, metric, all_metric, 
                                                      slice_compare_column, slice1,
                                                      summary_operator,
                                                      slices = slices,
                                                      dimensions = dimensions,
                                                      date_column_name = date_column_name,
                                                      day_first = day_first,
                                                      date_range = date_range
                                                      )

        return (result_table, suggestions)

    result_table = _slice_compare_results(table, metric, slice_compare_column,
                                          slice1, slice2, summary_operator,
                                          slices = slices, dimensions = dimensions,
                                          date_column_name = date_column_name,
                                          date_range = date_range, 
                                          day_first = day_first)

    suggestions = []

    simpsons_paradox_suggestion = simpsons_paradox(table, metric, all_dimensions,
                                                   slice_compare_column, slice1,
                                                   slice2, summary_operator,
                                                   dimensions = dimensions,
                                                   date_column_name = date_column_name,
                                                   date_range = date_range, 
                                                   day_first = day_first,
                                                   slices = slices)

    top_down_error_suggestion = top_down_error(table, metric, all_dimensions,
                                               slice_compare_column, slice1,
                                               slice2, summary_operator,
                                               dimensions = dimensions,
                                               date_column_name = date_column_name,
                                               date_range = date_range, 
                                               day_first = day_first,
                                               slices = slices)
    suggestions = simpsons_paradox_suggestion + top_down_error_suggestion

    if summary_operator is not None:
        result_table = aspects.update_metric_column_name(result_table, summary_operator, metric)

    return (result_table, suggestions)

def _slice_compare_results(table, metric, slice_compare_column,
                           slice1, slice2, summary_operator, **kwargs):
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
        day_first: Type-str
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
    day_first = kwargs.get('day_first', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     day_first)

    if slices == None:
        slices = [(slice_compare_column, Filters.IN, [slice1, slice2])]
    else:
        slices.append((slice_compare_column, Filters.IN, [slice1, slice2]))
    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(slice_compare_column)
    required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    # slice_compare_column should be the last element of the group
    # so that groupby will show them together for every grouping
    grouping_columns = []
    if dimensions is not None:
        grouping_columns = dimensions.copy()
    grouping_columns.append(slice_compare_column)
    
    result_table = aspects.group_by(table, grouping_columns, summary_operator)

    return result_table

def _slice_compare_results_for_all(table, metric, slice_compare_column,
                                   slice1, slice2, summary_operator, **kwargs):
    
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
        day_first: Type-str
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
    day_first = kwargs.get('day_first', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     day_first)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(slice_compare_column)
    required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    required_table_for_one = aspects.slice_table(table, [(slice_compare_column, 
                                                   Filters.EQUAL_TO, slice1)])
    
    required_table_for_all = table.copy()
    required_table_for_all[slice_compare_column] = 'ALL'

    updated_table = pandas.concat([required_table_for_all, required_table_for_one])
    updated_table = updated_table.reset_index(drop = True)

    # collecting the colums on whcih we shall do grouping
    grouping_columns = []
    if dimensions is not None:
        grouping_columns = dimensions.copy()
    grouping_columns.append(slice_compare_column)
    
    result_table = aspects.group_by(updated_table, grouping_columns, summary_operator)

    return result_table
