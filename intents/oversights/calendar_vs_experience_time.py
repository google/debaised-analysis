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
This module contains the calendar vs experience time series debaising.
The oversight occurs in the slice compare intent when date range is used
and both the slices are not consistent & differs in experience time.
"""
import pandas, datetime
from util import aspects, enums
from util.enums import SummaryOperators, Filters, Oversights
from util import constants 

def calendar_vs_experience_time(table, metric, all_dimensions, slice_compare_column, 
                            slice1, slice2, summary_operator, **kwargs):
    """This function will implement the calendar vs experience in time series debaising

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we will do 
            grouping, summary operator is applied on metric. Metric 
            could a column containing strings, if we are applying count 
            operator on it.
        dimensions: Type-list of str or None
            It is the name of column we want.
            In query:'compare batsman A and B according to total_runs',
             dimension is 'batsman'. we group by dimensions.
        all_dimension: Type-list of str
            It contains list of all dimensions
        slice_compare_column: Type-string
            name of the slice-compare column.
        slice1: Type-string
            the first value of comparision
        slice2: Type-string
            the second value of comparision
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in 
            the format Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done

    Returns:
        return the suggestion dictionary if the oversight is detected.
        Keys in the dictionary are 'oversight', 'suggestion', 'confidence_score'
    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    # calendar vs experience in time series suggestion will not apply
    # if no date range is passed or grouping using dimensions is done
    if date_range is None or dimensions is not None:
        return

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, date_format)
    
    slice_list = []
    if slices is not None:
        slice_list = slices.copy()
    slice_list.append((slice_compare_column, Filters.IN, [slice1, slice2]))

    table = aspects.slice_table(table, slice_list)

    # date columns for slice 1 and slice 2
    date_column_1 = []
    date_column_2 = []

    num_rows = table.shape[0]

    for row in range(num_rows):
        if table.loc[row, slice_compare_column] == slice1:
            date_column_1.append(table.loc[row, date_column_name])
        if table.loc[row, slice_compare_column] == slice2:
            date_column_2.append(table.loc[row, date_column_name])
    
    # converting string dates to datetime objects
    date_column_1 = [datetime.datetime.strptime(date, date_format) for date in date_column_1]
    date_column_2 = [datetime.datetime.strptime(date, date_format) for date in date_column_2]


    date_column_1.sort()
    date_column_2.sort()

    if len(date_column_1) == 0 or len(date_column_2) == 0:
    	return

    if date_column_1[0] > date_column_2[0]:
    	swap(date_column_1, date_column_2)

    num_less = 0
    num_total = 0

    for date in date_column_1:
    	if date < date_column_2[0]:
    		num_less += 1
    	num_total += 1

    parameter = num_less / num_total

    if parameter > constants.CALENDAR_VS_EXPERIENCE_TIME_THRESHOLD:
    	suggestion = {}
    	suggestion['oversight'] = enums.Oversights.CALENDAR_VS_EXPERIENCE_IN_TIME_SERIES
    	suggestion['confidence_score'] = parameter
    	suggestion['suggestion'] = 'The entries in the date range mentioned are not consistent for both the slices'
    	return suggestion 
