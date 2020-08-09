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
""" This modile contains the weighted mean intent.
The weighted mean intent finds the mean of column weighted by another
column.
The weighted arithmetic mean is similar to an ordinary arithmetic mean
(the most common type of average), except that instead of each of the
data points contributing equally to the final average, some data points
contribute more than others. The notion of weighted mean plays a role in
descriptive statistics and also occurs in a more general form in several
other areas of mathematics.

If all the weights are equal, then the weighted mean is the same as the
arithmetic mean. While weighted means generally behave in a similar fashion
to arithmetic means, they do have a few counterintuitive properties, as
captured for instance in Simpson's paradox.

Madlib :
    Type 1 : "Mean of <column1> weighted by <column2> where <filters> and
              <date-range>"
    Type 2 : "Mean of <column1> weighted by <column2> for each <grouping>
              where <filters> and <date-range>"

In Type 1 the result contains only 1 number as the result.
And in Type 2 the result is a table and a correlation coefficient for each
of the groupings.
"""
from util import aspects
import pandas

def weighted_mean(table, metric, weight_col, **kwargs):
    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.
    Currently no oversight is implemented.

    This function calls the _weighted_mean_results to get the results table
    for the weighted mean intent.

    Args :
        table: Type-pandas.dataframe
            It has the contents of the table in sheets
        metric : Type-string
            The column whose mean is to be found
        weight_col : Type-strings
            The weight column which is multiplied as weights to metric column
        dimensions: Type-list of str
            It the list of columns according to which groups are formed
            If these are passed we calculate the weighted mean for each group
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

        results: Type -pandas dataframe, The results of the weighted mean intent

        suggestions: Type - List of dictionaries(suggestion structure), List of
            suggestions.
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    result_table = _weighted_mean_results(table, metric, weight_col,
                                          dimensions=dimensions,
                                          date_column_name=date_column_name,
                                          date_range=date_range,
                                          date_format=date_format,
                                          slices=slices)

    suggestions = []

    return (result_table, suggestions)

def _weighted_mean_results(table, metric, weight_col, **kwargs):
    """ This functions implements the weighted mean intent

    Formula used for calculating weighted mean -

    metric column = {a1, a2, ... ai}
    weight column = {w1, w2, ... wi}

    weight mean = _sum(ai * wi) / _sum(wi)

    In case if _sum(wi) is 0 NaN is returned

    When a list of dimensions is also passed weighted mean is calculated
    for each grouping

    Args :
        table: Type-pandas.dataframe
            It has the contents of the table in sheets
        metric : Type-string
            The column whose mean is to be found
        weight_col : Type-strings
            The weight column which is multiplied as weights to metric column
        dimensions: Type-list of str
            It the list of columns according to which groups are formed
            If these are passed we calculate the weighted mean for each group
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


    Returns : Type-pandas.dataframe, the result table of the intent
        containing a column containing weighed mean
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', 'yyyy-mm-dd')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.apply_date_range(table, date_range,date_column_name, date_format)

    table = aspects.slice_table(table, slices)

    weighted_mean_col = 'mean of ' + metric + ' weighted by ' + weight_col

    if dimensions is None:
        # calculating weighted mean from the table
        table[weighted_mean_col] = table[metric] * table[weight_col]
        weighted_mean = table[weighted_mean_col].sum() / table[weight_col].sum()

        # Inserting the weighted mean in a new result table
        tbale = pandas.DataFrame([(weighted_mean)], columns=[weighted_mean_col])

        return tbale
    else:
        table = aspects.crop_other_columns(table, dimensions + [metric, weight_col])

        # Creating new column containg the product of metric & weight_col(Weight column)
        table[weighted_mean_col] = table[metric] * table[weight_col]
        table = table.groupby(dimensions).sum()


        table[weighted_mean_col] /= table[weight_col]

        table = table.reset_index()

        # Now the table contains the weighted mean for each dimension
        table = aspects.crop_other_columns(table, dimensions + [weighted_mean_col])

        return table
