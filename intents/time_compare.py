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

from util import aspects
import pandas

def time_compare(table, metric, dimensions, all_dimensions, time_compare_column,
                                                    summary_operator, **kwargs):

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
        time_compare_column: Type-list of different data types
            first element denotes the column name by which we will do comparision.
            second and third element are a tuple of start and end date range.
            last element is date_format in which the date of columns present.
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

    result_table = _time_compare_results(table, metric, dimensions, 
                                         time_compare_column, summary_operator, 
                                         date_column_name = date_column_name,
                                         date_range = date_range,
                                         date_format = date_format,
                                         slices = slices)
    return result_table

def _time_compare_results(table, metric, dimensions, time_compare_column,
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
        time_compare_column: Type-list of different data types
            first element denotes the column name by which we will do comparision.
            second and third element are a tuple of start and end date range.
            last element is date_format in which the date of columns present.
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
    date_format = kwargs.get('date_format', '%d/%m/%Y')

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     date_format)

    table = aspects.slice_table(table, slices)

    required_columns = dimensions.copy()
    required_columns.append(metric)

    required_table = aspects.crop_other_columns(table, required_columns)
    
    """ we shall have two list so that we can combine both the table and 
    after applying the groupby operation we can get the desired result."""
    table_slice1 = aspects.apply_date_range(required_table, 
                                            time_compare_column[1], 
                                            time_compare_column[0], 
                                            time_compare_column[3])
    table_slice1[time_compare_column[0]] = time_compare_column[1][0] + " - " + time_compare_column[1][1]

    table_slice2 = aspects.apply_date_range(required_table, 
                                            time_compare_column[2], 
                                            time_compare_column[0], 
                                            time_compare_column[3])
    table_slice2[time_compare_column[0]] = time_compare_column[2][0] + " - " + time_compare_column[2][1]

    # Pandas library to combine the tables.
    updated_table = pandas.concat([table_slice2, table_slice1])
    
    grouping_columns = dimensions.copy()
    grouping_columns.remove(time_compare_column[0])
    grouping_columns.append(time_compare_column[0])

    result_table = aspects.group_by(updated_table, grouping_columns, 
                                                   summary_operator)

    return result_table
