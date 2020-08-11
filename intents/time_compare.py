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

"""This module contains the time-compare intent.
The time-compare intent can give the result so that user can easily
compare the data according to the way user want.
Also it supports some operations like cropping based on date range,
slicing(removing rows that do not follow the conditions), group by.
Some of the operations are optional.
"""

from util import aspects, oversights_order, rank_oversights
import pandas
from oversights.simpsons_paradox import simpsons_paradox
from oversights.top_down_error import top_down_error

def time_compare(table, metric, all_dimensions, time_compare_column, date_range1, 
                           date_range2, date_format, summary_operator, **kwargs):

    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.
    Some of the oversights considered in this intent are-
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
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
        time_compare_column: Type-string
            the column name by which we will do comparision.
        date_range1: Type-tuple of start_date and end_date
            first date range for which we have to do comparision
        date_range2: Type-tuple of start_date and end_date
            second date range for which we have to do comparision
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done
    Returns:
        The function will return both suggestions and the results in a tuple.
        (results, suggestions)
        results: Type - pandas dataframe, The results of the intended time-compare
        suggestions: Type - List of strings, List of suggestions.
    """

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    result_table = _time_compare_results(table, metric, 
                                         time_compare_column,
                                         date_range1, date_range2, 
                                         date_format, summary_operator,
                                         dimensions = dimensions, 
                                         slices = slices)

    table_slice1 = aspects.apply_date_range(table, date_range1,
                                            time_compare_column, 
                                            date_format)
    table_slice1[time_compare_column] = date_range1[0] + " - " + date_range1[1]
    
    table_slice2 = aspects.apply_date_range(table, date_range2,
                                            time_compare_column, 
                                            date_format)
    table_slice2[time_compare_column] = date_range2[0] + " - " + date_range2[1]

    oversights_detection_table = pandas.concat([table_slice2, table_slice1])
    oversights_detection_table = oversights_detection_table.reset_index(drop = True)

    suggestions = []

    simpsons_paradox_suggestion = simpsons_paradox(oversights_detection_table, 
                                                   metric, all_dimensions,
                                                   time_compare_column,
                                                   date_range1[0] + " - " + date_range1[1],
                                                   date_range2[0] + " - " + date_range2[1],
                                                   summary_operator,
                                                   dimensions = dimensions,
                                                   slices = slices)

    top_down_error_suggestion = top_down_error(oversights_detection_table,  
                                               metric, all_dimensions,
                                               time_compare_column,
                                               str(date_range1[0] + " - " + date_range1[1]),
                                               str(date_range2[0] + " - " + date_range2[1]),
                                               summary_operator,
                                               dimensions = dimensions,
                                               slices = slices)

    suggestions = simpsons_paradox_suggestion + top_down_error_suggestion
    
    order = oversights_order.ORDER_IN_TIME_COMPARE

    suggestions = rank_oversights.rank_oversights(suggestions, order)

    return (result_table, suggestions)

def _time_compare_results(table, metric, time_compare_column, 
                          date_range1, date_range2, date_format, 
                          summary_operator, **kwargs):

    """ This function returns the results according to the intent.
    Some of the oversights considered in this intent are-

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
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
        time_compare_column: Type-string
            the column name by which we will do comparision.
        date_range1: Type-tuple of start_date and end_date
            first date range for which we have to do comparision
        date_range2: Type-tuple of start_date and end_date
            second date range for which we have to do comparision
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done
    Returns:
        The function will return the results
        results: Type - pandas dataframe, The results of the intended time-compare
    """

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.slice_table(table, slices)

    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(time_compare_column)
    required_columns.append(metric)

    required_table = aspects.crop_other_columns(table, required_columns)
    
    # we shall have two list so that we can combine both the table and 
    # after applying the groupby operation we can get the desired result.
    table_slice1 = aspects.apply_date_range(required_table,  
                                            date_range1,
                                            time_compare_column,
                                            date_format)
    table_slice1[time_compare_column] = date_range1[0] + " - " + date_range1[1]

    table_slice2 = aspects.apply_date_range(required_table,  
                                            date_range2,
                                            time_compare_column,
                                            date_format)
    table_slice2[time_compare_column] = date_range2[0] + " - " + date_range2[1]

    # Pandas library to combine the tables.
    updated_table = pandas.concat([table_slice2, table_slice1])
    updated_table = updated_table.reset_index(drop = True)

    grouping_columns = []
    if dimensions is not None:
        grouping_columns = dimensions.copy()
    grouping_columns.append(time_compare_column)

    result_table = aspects.group_by(updated_table, grouping_columns, 
                                                   summary_operator)

    return result_table
