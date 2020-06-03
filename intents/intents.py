"""This module currently contains the signature/implementation of some intents"""

import aspects

import datetime

def top_k(table, metric, dimensions, is_asc, k, **kwargs):
    """This function will implement the top-k intent

    Sorts tuples in the order metric, after applying slice, groupby operations. Also removes the tuples that do not lie in the given date range.
    The arguments 'table, metric,dimension,sort_order, k' are not optional so they are passed as it is,
    rest of the arguments that are optional('date_range', 'slices') will be passed in kwargs.
    If the summary_operator is not None, it groups by dimensions.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort, and in the case when grouping has to be done, summary operator is applied on metric. metric could a column containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want. ex query : 'top 5 batsman according to runs' , here dimension is 'batsman', when summary_operator is not None, we group by dimensions.
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        k: Type-int
            It is the number of entries to be taken
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes - https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as instance we want to slice
        summary_operator: Type-str
            It denotes the summary operator, after grouping by dimensions.

    Note- summary_operator is always applied on metric column passed, and only when grouping is done

    Returns:
        The function will return the `table(a pandas dataframe object)` after applying the intent on the `given table(a pandas dataframe object)``

    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    summary_operator = kwargs.get('summary_operator', None)


    table = aspects.apply_date_range(table, date_range, date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    table = aspects.corp_other_dimensions(table, dimensions, metric)

    table = aspects.group_by(table, dimensions, summary_operator)

    table = table.sort_values(by=[metric], ascending=is_asc)

    # selecting only the top-k
    table = table.head(k)

    return table

def trend(table, metric, date_range, date_column_name, date_format, granularity, summary_operator, **kwargs):
    """This function will implement the trend intent

    Groups by time, then applies summary operator on the column-name=metric to compress the rows having similar date according to time granularity, 
        after applying slicing and date range.
    Only slices is optional, so it is passed using kwargs

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort, and in the case when grouping has to be done, summary operator is applied on metric. metric could a column containing strings, if we are applying count operator on it.
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes - https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as instance we want to slice
        summary_operator: Type-str
            It denotes the summary operator

    Returns:
        The function will return the `table(a pandas dataframe object)` after applying the intent on the `given table(a pandas dataframe object)``

    """

    slices = kwargs.get('slices', None)

    table = aspects.apply_date_range(table, date_range, date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    table = aspects.corp_other_dimensions(table, [date_column_name], metric)

    num_rows = table.shape[0]
    for row in range(num_rows):
        row_date = datetime.datetime.strptime(table.loc[row, date_column_name], date_format)
        row_date = aspects.granular_time(row_date, granularity)
        table.loc[row, date_column_name] = row_date.strftime(date_format)

    table = aspects.group_by(table, [date_column_name], summary_operator)

    table = table.sort_values(by=[date_column_name])

    return table