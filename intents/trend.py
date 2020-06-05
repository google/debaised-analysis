"""This module contains the trend intent."""

import datetime

from Utilities import aspects

def trend(table, metric, granularity, summary_operator, **kwargs):
    """This function will implement the trend intent

    Groups by time, then applies summary operator on the column-name=metric to
    compress the rows having similar date according to time granularity,
    after applying slicing and date range. If some the optional args are None(not passed),
    it is assumed that we don't have to apply them.
    Only slices and date range parameters(range, column_name, format) is optional,
    so it is passed using kwargs.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort, and in the case
            when grouping has to be done, summary operator is applied on metric.
            Metric could a column containing strings, if we are applying count operator on it.
        date_range: Type-tuple
            Tuple of start_date and end_date, if it is null, represents that we don't need to crop
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes-
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as instance we want to slice
        summary_operator: Type-summary_operators enum member
            It denotes the summary operator
        granularity: Type-granularities enum member
            It denotes the granularity we need to apply to the dates.

    Returns:
        The function will return the `table(a pandas dataframe object)`
        after applying the intent on the `given table(a pandas dataframe object)`

    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range, date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = [date_column_name, metric]

    table = aspects.corp_other_columns(table, required_columns)

    num_rows = table.shape[0]
    for row in range(num_rows):
        row_date = datetime.datetime.strptime(table.loc[row, date_column_name], date_format)
        row_date = aspects.granular_time(row_date, granularity)
        table.loc[row, date_column_name] = row_date.strftime(date_format)

    table = aspects.group_by(table, [date_column_name], summary_operator)

    table = table.sort_values(by=[date_column_name])

    return table
