"""This module currently contains the signature/implementation of some intents"""

from Utilities import aspects

def slice_compare(table, metric, dimension, slices, summary_operator, **kwargs):
    """This function will implement the slice-compare intent

    Sorts tuples in the order metric, after applying slice, groupby operations.
    Also removes the tuples that do not lie in the given date range.
    The arguments 'table, metric,dimension, slices, summary_operator' are not optional so they are passed as it is,
    rest of the arguments that are optional('date_range') will be passed in kwargs.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort,
            and in the case when grouping has to be done,
            summary operator is applied on metric.
            Metric could a column containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            ex query : 'top 5 batsman according to runs', here dimension is 'batsman'.
            When summary_operator is not None, we group by dimensions.
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as instance we want to slice
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.

    Note- summary_operator is always applied on metric column passed, and only when grouping is done

    Returns:
        The function will return the `table(a pandas dataframe object)`
        after applying the intent on the `given table(a pandas dataframe object)``

    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')


    table = aspects.apply_date_range(table, date_range, date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(metric)

    table = aspects.corp_other_columns(table, required_columns)

    table = aspects.group_by(table, dimensions, summary_operator)

    return table
