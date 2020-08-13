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

"""This module implements the aspects
Aspects are the operations we perform while the the users intents are
being processed, most of them are common between all intents.
These are the functions that take the table, then perform some operations
on it and return the updated table.
Example in slicing - the rows that do not satisft the slicing condition
are dropped.
"""
from util import enums, date_module
import datetime , statistics
from oversights.mean_vs_median import mean_vs_median
from oversights.attribution_with_hidden_negative import attribution_with_hidden_negative

# Global Variables used by group_by and _mean to give oversights

# Row index of the groups in the result table
group_row_index = 1

# List of suggestions created by grouping , each suggestion being a dictionary defined by the oversight
suggestions = []


def apply_date_range(table, date_range, date_column_name, day_first, **kwargs):
    """This function removes the rows from from the table that
       are not in the date range(contains start date and end date) given.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        date_range: Type-tuple
            Tuple of start_date and end_date
            start_date & end_date are in a fixed format - '%Y-%m-%d'
        date_column_name: Type-str
            It is the name of column which contains date
        day_first: Type-str
            Day_first denotes that does day in the date occurs before month in the
            dates in the date column
            Example - '29-02-19', here day_first is true

    Returns:
        The updated table after aplying the condition, in pandas.dataframe type
    """
    if date_range is None:
        return table

    reset_index = kwargs.get('reset_index', True)
    
    num_rows = table.shape[0]

    for row in range(num_rows):
        row_date = date_module.str_to_datetime(table.loc[row, date_column_name],
                                               day_first)

        # format of start_date & end_date strings is always fixed
        start_date = datetime.datetime.strptime(date_range[0], '%Y-%m-%d')
        end_date = datetime.datetime.strptime(date_range[1], '%Y-%m-%d')

        if row_date < start_date or end_date < row_date:
            table = table.drop([row])

    # drop=True drops the new columnn named 'index' created in reset_index call
    if reset_index is True:
        table = table.reset_index(drop=True)
    return table

def slice_table(table, slices,  **kwargs):
    """This function removes the rows from the table
       that do not satisfy the slicing condition.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        slices: Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. enums.Filters.IN
            list of supported operators -
                Equal to
                Not equal to
                Less than
                Less than equal to
                Greater than
                Greater than equal to
                In
                Not In
        reset_index: Bool
            True/False- to perform reset index or not
            Used only for generating the new column in insert_as_column

    Returns:
        The updated table after aplying the condition, in pandas.dataframe type
    """

    # initialized with True, so will not affect intents layer
    reset_index = kwargs.get('reset_index', True)

    if slices is None:
        return table

    num_rows = table.shape[0]

    # init a list that will contain index of rows to be dropped
    rows_to_be_dropped = []

    for row in range(num_rows):
        slice_match = True
        # checking if all condition in slices match
        for condition in slices:
            if condition[1] == enums.Filters.EQUAL_TO and not (
                    table.loc[row, condition[0]] == condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.NOT_EQUAL_TO and not (
                    table.loc[row, condition[0]] != condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.LESS_THAN and not (
                    table.loc[row, condition[0]] < condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.LESS_THAN_EQUAL_TO and not (
                    table.loc[row, condition[0]] <= condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.GREATER_THAN and not (
                    table.loc[row, condition[0]] > condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.GREATER_THAN_EQUAL_TO and not (
                    table.loc[row, condition[0]] >= condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.IN and not (
                    table.loc[row, condition[0]] in condition[2]):
                slice_match = False
            if condition[1] == enums.Filters.NOT_IN and not (
                    table.loc[row, condition[0]] not in condition[2]):
                slice_match = False

        # collecting row index if slice condition does not satisfy
        if slice_match is not True:
            rows_to_be_dropped.append(row)

    table = table.drop(rows_to_be_dropped)

    #some indices get deleted after slicing
    if reset_index is True:
        table = table.reset_index(drop=True)

    return table

def crop_other_columns(table, required_columns):
    """This function removes the columns that are not in required_columns list
       This would help getting rid of columns that are not to be displayed.
    Args:
        table: Type-pandas.dataframe
        required_columns: Type-list of str

    Returns:
        Returns the table as a dataframe obj after
        removing the rest of the columns.
    """

    current_columns = table.columns
    for column in current_columns:
        if column not in required_columns:
            table = table.drop([column], axis=1)

    return table

def _count_distinct(values):
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


def _mean(values):
    """ This function returns the average of values ,
    along with it the function also tests the existence of
    mean_vs_median oversight

    Args:
        values: Type - anything that can be iterated over

    Returns:
        Average of values

    Updates global variables,
        group_row_index always increases by 1
        suggestions is updated by the mean_vs_median suggestion if it exists    
    """

    global group_row_index , suggestions

    mean = statistics.mean(values)

    # to collect all numbers in values
    numbers = []

    for value in values :
        numbers.append(value)

    suggestion = mean_vs_median(numbers)

    if(suggestion is not None) :

        row_suggestion = {}
        row_suggestion['row'] = group_row_index
        row_suggestion['confidence_score'] = suggestion['confidence_score']

        # First mean_vs_median suggestion
        if len(suggestions) == 0:
            suggestion['row_list'] = []
            
            suggestion['row_list'].append(row_suggestion)
            suggestions.append(suggestion)
        
        else:
            #Updating the mean_vs_median suggestion
            suggestions[-1]['row_list'].append(row_suggestion)

    group_row_index += 1

    return mean

def _sum_for_propotion(values):
    """ This function returns the sum of values ,
    it is called separately to be able to check the 
    oversight of attribution with hidden negative

    Args:
        values: Type - anything that can be iterated over

    Returns:
        sum of values

    Updates global variables,
        group_row_index always increases by 1
        suggestions is updated by the attribution with hidden negative suggestion if it exists    
    """

    global group_row_index , suggestions

    # to collect all numbers in values
    numbers = []

    sum_of_values = 0

    for value in values :
        sum_of_values += value
        numbers.append(value)

    suggestion = attribution_with_hidden_negative(numbers)

    if(suggestion is not None) :

        row_suggestion = {}
        row_suggestion['row'] = group_row_index
        row_suggestion['confidence_score'] = suggestion['confidence_score']

        # First suggestion
        if len(suggestions) == 0:
            suggestion['row_list'] = []
            
            suggestion['row_list'].append(row_suggestion)
            suggestions.append(suggestion)
        
        else:
            #Updating the suggestion
            suggestions[-1]['row_list'].append(row_suggestion)

    group_row_index += 1

    return sum_of_values

def _count_for_propotion(values):
    """ This function returns the count of values ,
    it is called separately to be able to check the 
    oversight of attribution with hidden negative

    Args:
        values: Type - anything that can be iterated over

    Returns:
        sum of values

    Updates global variables,
        group_row_index always increases by 1
        suggestions is updated by the attribution with hidden negative suggestion if it exists    
    """

    global group_row_index , suggestions

    # to collect all numbers in values
    numbers = []

    count_of_values = 0

    for value in values :
        count_of_values += 1
        numbers.append(value)

    suggestion = attribution_with_hidden_negative(numbers)

    if(suggestion is not None) :

        row_suggestion = {}
        row_suggestion['row'] = group_row_index
        row_suggestion['confidence_score'] = suggestion['confidence_score']

        # First suggestion
        if len(suggestions) == 0:
            suggestion['row_list'] = []
            
            suggestion['row_list'].append(row_suggestion)
            suggestions.append(suggestion)
        
        else:
            #Updating the suggestion
            suggestions[-1]['row_list'].append(row_suggestion)

    group_row_index += 1

    return count_of_values


def group_by(table, dimensions, summary_operator, **kwargs):
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
        Returns a dictionary with the following (key,values) :
        'table' -> the table as a dataframe obj after applying grouping
        'suggestions' -> List of suggestions structure i.e debiasing suggestion 
    """

    global group_row_index , suggestions

    # Dictionary that will be returned
    result = {}
    result['table'] = table
    result['suggestions'] = []

    # defining the first row index as 1
    group_row_index = 1

    # starting with an empty list of suggestions
    suggestions = []

    if summary_operator is None:
        return result

    if summary_operator == enums.SummaryOperators.SUM:
        table = table.groupby(dimensions).sum()

    if summary_operator == enums.SummaryOperators.MEAN:
        table = table.groupby(dimensions).agg(_mean)

    if summary_operator == enums.SummaryOperators.MEDIAN:
        table = table.groupby(dimensions).median()

    if summary_operator == enums.SummaryOperators.COUNT:
        table = table.groupby(dimensions).count()

    if summary_operator == enums.SummaryOperators.MAX:
        table = table.groupby(dimensions).max()

    if summary_operator == enums.SummaryOperators.MIN:
        table = table.groupby(dimensions).min()

    if summary_operator == enums.SummaryOperators.STD:
        table = table.groupby(dimensions).std()

    if summary_operator == enums.SummaryOperators.VAR:
        table = table.groupby(dimensions).var()

    if summary_operator == enums.SummaryOperators.FIRST:
        table = table.groupby(dimensions).first()

    if summary_operator == enums.SummaryOperators.LAST:
        table = table.groupby(dimensions).last()

    if summary_operator == enums.SummaryOperators.DISTINCT:
        table = table.groupby(dimensions).agg(_count_distinct)
    
    if summary_operator == enums.SummaryOperators.PROPORTION_OF_SUM:
        table = table.groupby(dimensions).agg(_sum_for_propotion)
        for column in table.columns:
            if column not in dimensions:
                table[column] /= table[column].sum()

    if summary_operator == enums.SummaryOperators.PROPORTION_OF_COUNT:
        table = table.groupby(dimensions).agg(_count_for_propotion)
        for column in table.columns:
            if column not in dimensions:
                table[column] /= table[column].sum()

    table = table.reset_index()

    result['table'] = table
    result['suggestions'] = suggestions

    return result

def granular_time(row_date, granularity):
    """ Sets the time such that all time thats difference
        is not > granularity have the same time.
        It represents the hour, day, month, year that the date lies in,
        in case of HOURLY, DAILY, MONTHLY, ANNUALLY respectively.
        In other words it agregates dates,
        in some range to one date so that grouping can be done.

    Example:
        If date is 2017-04-12 and granularity is Granularities.ANNUALLY,
            so it will convert the date to 2017-01-01
        If date is 2017-04-12 and granularity is Granularities.MONTHLY,
            so it will convert the date to 2017-04-01
        If date is 2017-04-12 and granularity is Granularities.DAILY,
            so it will convert the date to 2017-04-12

    Args:
        row_date: Type-datetime.datetime
        granularity: Type-Granularities enum member
            currently, only these are supported-
            Granularities.HOURLY, Granularities.DAILY,
            Granularities.monthly, Granularities.ANNUALLY

    Returns:
       Returns the updated row_date
    """
    if granularity == enums.Granularities.HOURLY:
        row_date = row_date.replace(second=0, minute=0)
    if granularity == enums.Granularities.DAILY:
        row_date = row_date.replace(second=0, minute=0, hour=0)
    if granularity == enums.Granularities.MONTHLY:
        row_date = row_date.replace(second=0, minute=0, hour=0, day=1)
    if granularity == enums.Granularities.ANNUALLY:
        row_date = row_date.replace(second=0, minute=0, hour=0, day=1, month=1)

    return row_date