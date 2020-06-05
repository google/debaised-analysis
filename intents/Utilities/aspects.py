"""This module implements the aspects"""

import datetime

from Utilities.enumerations import SummaryOperators, Granularities

def apply_date_range(table, date_range, date_column_name, date_format):
    """This function removes the rows from from the table that
    are not in the date range(contains start date and end date) given.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Returns:
        The updated table after aplying the condition, in pandas.dataframe type
    """
    if date_range is None:
        return table
    num_rows = table.shape[0]
    for row in range(num_rows):
        row_date = datetime.datetime.strptime(table.loc[row, date_column_name], date_format)
        start_date = datetime.datetime.strptime(date_range[0], date_format)
        end_date = datetime.datetime.strptime(date_range[1], date_format)
        if row_date < start_date or end_date < row_date:
            table = table.drop([row])
    table = table.reset_index()
    table = table.drop(['index'], axis=1)
    return table

def slice_table(table, slices):
    """This function removes the rows from the table that do not satisfy the slicing condition.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        slices: Type-dictionary (will be changed)
            contains the key as column name and value as instance we want to slice

    Returns:
        The updated table after aplying the condition, in pandas.dataframe type
    """
    if slices is None:
        return table
    num_rows = table.shape[0]
    for row in range(num_rows):
        slice_match = True
        for key in slices:
            if table.loc[row, key] != slices[key]:
                slice_match = False
        if slice_match is not True:
            table = table.drop([row])

    #some indices get deleted after slicing
    table = table.reset_index()
    # droping the new columnn named 'index' created after reset_index call
    table = table.drop(['index'], axis=1)
    return table

def corp_other_columns(table, required_columns):
    """This function removes the columns that are not in required_columns list
       This would help getting rid of columns that are not to be displayed.
    Args:
        table: Type-pandas.dataframe
        required_columns: Type-list of str

    Returns:
        Returns the table as a dataframe obj after removing the rest of the columns.
    """

    current_columns = table.columns
    for column in current_columns:
        if column not in required_columns:
            table = table.drop([column], axis=1)

    return table

def count_distinct(values):
    """ This function returns the number of distinct entries in values.
    The values are inserted into a set and it's size is returned.

    Args:
        values: Type - anything that can be iterated over

    Returns:
        Count of distinct values.
    """
    distinct_set = set()
    for value in values:
        distinct_set.add(value)
    return len(distinct_set)

def group_by(table, dimensions, summary_operator):
    """Groups the column by the columns in dimensions
    Basically makes a map in which keys contain dimensions and values
    are evaluated after applying the summary operator.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        dimensions: Type-list
            It contains the names of columns according to which we group
        summary_operator: Type-SummaryOperators enum members
            It denotes the summary operator

    Returns:
        Returns the table as a dataframe obj after applying grouping
    """
    if summary_operator is None:
        return table
    if summary_operator == SummaryOperators.summation:
        table = table.groupby(dimensions).sum()

    if summary_operator == SummaryOperators.mean:
        table = table.groupby(dimensions).mean()

    if summary_operator == SummaryOperators.count:
        table = table.groupby(dimensions).count()

    if summary_operator == SummaryOperators.maximum:
        table = table.groupby(dimensions).max()

    if summary_operator == SummaryOperators.minimum:
        table = table.groupby(dimensions).min()

    if summary_operator == SummaryOperators.std:
        table = table.groupby(dimensions).std()

    if summary_operator == SummaryOperators.var:
        table = table.groupby(dimensions).var()

    if summary_operator == SummaryOperators.first:
        table = table.groupby(dimensions).first()

    if summary_operator == SummaryOperators.last:
        table = table.groupby(dimensions).last()

    if summary_operator == SummaryOperators.distinct:
        table = table.groupby(dimensions).agg(count_distinct)

    table = table.reset_index()

    return table

def granular_time(row_date, granularity):
    """ Sets the time such that all time thats difference is not > granularity have the same time.
        It represents the hour, day, month, year that the date lies in,
        in case of hourly, daily, monthly, annually respectively.
        In other words it agregates dates, in some range to one date so that grouping can be done.

    Exampll:
        If date is 2017-04-12 and granularity is Granularities.annually,
            so it will convert the date to 2017-01-01
        If date is 2017-04-12 and granularity is Granularities.monthly,
            so it will convert the date to 2017-04-01
        If date is 2017-04-12 and granularity is Granularities.daily,
            so it will convert the date to 2017-04-12

    Args:
        row_date: Type-datetime.datetime
        granularity: Type-Granularities enum member
            currently, only these are supported - Granularities.hourly, Granularities.daily,
            Granularities.monthly, Granularities.annually

    Returns:
       Returns the updated row_date
    """
    if granularity == Granularities.hourly:
        row_date = row_date.replace(second=0, minute=0)
    if granularity == Granularities.daily:
        row_date = row_date.replace(second=0, minute=0, hour=0)
    if granularity == Granularities.monthly:
        row_date = row_date.replace(second=0, minute=0, hour=0, day=1)
    if granularity == Granularities.annually:
        row_date = row_date.replace(second=0, minute=0, hour=0, day=1, month=1)

    return row_date
