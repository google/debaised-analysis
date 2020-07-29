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

"""This module contains the show intent.
The show intent finds and displays the table which is needed by the user ,
doing the required cropping based on date range , slicing (removing rows
that do not follow the conditions) , groupy by. 
Some of the operations are optional.
"""

from util import aspects

def show(table,**kwargs):
    """This function will implement the show intent

    Firstly removes the tuples that do not lie in the given date range.
    Then applies slicing and groupby operations.
    The argument 'table' is not optional , hence passed as it is.
    Rest of the arguments are optional , hence passed in kwargs
    If the summary_operator is not None , it groups by dimensions.
    If some of the optional args are None (not passed),
    it is assumed that we don't have to apply them.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column on which
            summary operator is applied in case of grouping. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'show all batsman', dimension is 'batsman'.
            When summary_operator is not None, we group by dimensions.
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
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    summary_operator = kwargs.get('summary_operator', None)

    metric = kwargs.get('metric',None)

    dimensions = kwargs.get('dimensions',None)

    table = aspects.apply_date_range(table, date_range,date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
    	required_columns = dimensions.copy()
    # metric is optional in show	
    if metric is not None:
        required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    # When there is no dimension to group by but a summary_operator exists ,
    # we assume that user wants to apply the summary operator on whole data
    if( (dimensions is None) and (summary_operator is not None) ):
        # We add temporary column of 'Summary Operator' by which we can groupby
        # to obtain the final result
        add_temporary_column_of_summary_operator(table,summary_operator)

        dimensions = []

        # To groupby 'Summary Operator' column inserted
        dimensions.append('Summary Operator')

    table = aspects.group_by(table, dimensions, summary_operator)

    return table




def add_temporary_column_of_summary_operator(table,summary_operator):
    """This function adds a new column of summary operator

    Whenever Show intent is applied on the whole data we 
    will add a temporary column which represent the summary operator
    and then apply grouping on the whole data which will give the 
    intended result.

    Example : 
    INPUT                      OUTPUT

        Marks                   Summary Operator   Marks 
    0   10                  0   MEAN                10
    1   20                  1   MEAN                20
    2   30                  2   MEAN                30

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

        
    Returns:
        The function will return the `table(a pandas dataframe object)`
        after adding the temporary column of summary operator
    """

    number_of_rows = len(table.index)

    summary_operator_column = [ summary_operator.name ] * number_of_rows

    table[ 'Summary Operator' ] = summary_operator_column

    return table 