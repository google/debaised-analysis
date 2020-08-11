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

"""This module contains the trend intent.
The trend intent shows the trend of the metric
over time, it combines rows that are in the same time interval, for ex
yearly trend OR monthly trend. It compresses the rows that lie in the 
same year in case for yearly trend an similarly for others.
Also it supports some operations like cropping based on date range, 
slicing(removing rows that do not follow the conditions), group by.
Some of the operations are optional.
"""

import datetime

from util import aspects, date_module, oversights_order, rank_oversights

def trend(table, metric, granularity, summary_operator, **kwargs):
    """This function will implement the trend intent

    Groups by time, then applies summary operator on the column-name=metric to
    compress the rows having similar date according to time granularity,
    after applying slicing and date range. If some the optional args are
    None(not passed), it is assumed that we don't have to apply them.
    Only slices and date range parameters(range, column_name, format)
    is optional, so it is passed using kwargs.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort, and in the
            case when grouping has to be done, summary operator is applied
            on metric. Metric could be a column containing strings,
            if we are applying count operator on it.
        date_range: Type-tuple
            Tuple of start_date and end_date, if it is null,
            represents that we don't need to crop
        date_column_name: Type-str
            It is the name of column which contains date
        day_first: Type-str
            Day_first denotes that does day in the date occurs before month in the
            dates in the date column
            Example - '29-02-19', here day_first is true
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as
            instance we want to slice
        summary_operator: Type-summary_operators enum member
            It denotes the summary operator
        granularity: Type-granularities enum member
            It denotes the granularity we need to apply to the dates.

    Returns:
        The function will return the `table(a pandas dataframe object)`
        after applying the intent on the given
        `table(a pandas dataframe object)`

    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    day_first = kwargs.get('day_first', False)

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, day_first)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = [date_column_name, metric]

    table = aspects.crop_other_columns(table, required_columns)

    num_rows = table.shape[0]
    for row in range(num_rows):
        row_date = date_module.str_to_datetime(table.loc[row, date_column_name],
                                               day_first)
        row_date = aspects.granular_time(row_date, granularity)
        table.loc[row, date_column_name] = row_date.strftime('%Y-%m-%d')

    table = aspects.group_by(table, [date_column_name], summary_operator)

    table = table.sort_values(by=[date_column_name])

    suggestions = []

    # add mean vs median suggestion

    order = oversights_order.ORDER_IN_TREND

    suggestions = rank_oversights.rank_oversights(suggestions, order)

    return table
