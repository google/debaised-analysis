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
""" This module contains the correlation intent.
The correlation intent finds the correlation coefficient between 2
columns/metrics.
In statistics, correlation or dependence is any statistical relationship,
between two random variables or bivariate data. In the broadest sense
correlation is any statistical association, though it commonly refers
to the degree to which a pair of variables are linearly related.
Madlib :
    Type 1 : "Correlation between <column1> & <column2> where <filters> and
              <date-range>"
    Type 2 : "Correlation between <column1> & <column2> for each <grouping>
              where <filters> and <date-range>"

In Type 1 the result contains only 1 number as the result.
And in Type 2 the result is a table and a correlation coefficient for each
of the groupings.

Correlation value close to +1 means that the 2 variables move in the same
direction with respect to their means. 

Correlation value close to -1 means that the 2 variables move in the opposite
directions with respect to their means. 

Correlation value close to 0 means that the 2 columns are weakly correlated.
"""
from util import aspects, oversights_order, rank_oversights
import pandas

def correlation(table, metric1, metric2, **kwargs):
    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.
    Currently no oversight is implemented.

    This function calls the _correlation_result to get the results table
    for the correlation intent.
    
    Args :
        table: Type-pandas.dataframe
            It has the contents of the table in sheets
        metric1, metric2 : Type-strings
            The columns between which the correlation is to be found
        dimensions: Type-list of str
            It the list of columns according to which groups are formed
            If these are passed we calculate the correlation for each group
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes -https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
    Returns:
        The function will return both suggestions and the results in a tuple.
        (results, suggestions)
        results: Type - pandas dataframe, The results of the correlation intent
        suggestions: Type - List of strings, List of suggestions.
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions',None)

    result_table = _correlation_results(table, metric1, metric2,
                                         dimensions=dimensions,
                                         date_column_name=date_column_name,
                                         date_range=date_range,
                                         date_format=date_format,
                                         slices=slices)

    suggestions = []
    # ToDo (Onhold oversight) : Anscombe Quartet Error    
    
    order = oversights_order.ORDER_IN_CORRELATION

    suggestions = rank_oversights.rank_oversights(suggestions, order)

    return (result_table, suggestions)

def _correlation_results(table, metric1, metric2, **kwargs):
    """ This functions implements the correlation intent

    Uses the pandas corr() function to find the correlation coefficient.

    If grouping is not done the result will be a single number - the
        correlation coefficient.
    If grouping is done the result will be a table - the correlation
        coeffiecient for each group.

    There are 3 types of correlations:
        Standard correlation coefficient
        Kendall Tau correlation coefficient
        Spearman rank correlation

    Here the standard `Pearson correlation coefficient` is used.
    
    Args :
        table: Type-pandas.dataframe
            It has the contents of the table in sheets
        metric1, metric2 : Type-strings
            The columns between which the correlation is to be found
        dimensions: Type-list of str
            It the list of columns according to which groups are formed
            If these are passed we calculate the correlation for each group
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes -https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions',None)
    
    table = aspects.apply_date_range(table, date_range,date_column_name, date_format)
    
    table = aspects.slice_table(table, slices)

    correlation_col = 'correlation between "' + metric1 + '" , "' + metric2 + '"'

    if dimensions is None:
        correlation = table[metric1].corr(table[metric2])
        result_table = pandas.DataFrame([(correlation)], columns=[correlation_col])
        return result_table
    else:
        table = aspects.crop_other_columns(table, dimensions + [metric1, metric2])
        table = table.groupby(dimensions).corr().reset_index()
        table = aspects.crop_other_columns(table, dimensions + [metric1])
        table = table.rename(columns={metric1:correlation_col})
        table = table.groupby(dimensions).min()
        table = table.reset_index()

        return table
