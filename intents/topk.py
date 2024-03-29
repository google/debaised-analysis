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

"""This module contains the top-k intent.
The top-k intent sorts the table and returns the first/last k entries.
Also it supports some operations like cropping based on date range,
slicing(removing rows that do not follow the conditions), group by.
Some of the operations are optional.
"""

from oversights.regression_to_mean import regression_to_mean
from oversights.looking_at_tails import looking_at_tails
from oversights.duplicates_in_topk import duplicates_in_topk
from oversights.more_than_just_topk import more_than_just_topk
from oversights.topk_when_less_than_k_present import topk_when_less_than_k_present
from oversights.topk_vs_others import topk_vs_others
from util.enums import *
from util import aspects, oversights_order, rank_oversights

def topk(table, metric, dimensions, is_asc, k, **kwargs):
    """ This function returns both the results according to the intent
    as well as the debiasing suggestions.

    Also, if summary operator is applied, the name of metric column is
    renamed to "<summary operator> of metric".

    Oversights that may be detected in top-k
    1. Regression to the mean
    2. Looking at tails to find causes
    3. Duplicates in top-k
    4. More than just top-k
    5. Top-k vs others
    6. Top-k when less than k present

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort,
            and in the case when grouping has to be done,
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'top 5 batsman according to runs', dimension is 'batsman'.
            When summary_operator is not None, we group by dimensions.
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        k: Type-int
            It is the number of entries to be taken
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        day_first: Type-str
            Day_first denotes that does day in the date occurs before month in the
            dates in the date column
            Example - '29-02-19', here day_first is true
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
        The function will return both suggestions and the results in a tuple.
        (results, suggestions)

        results: Type -pandas dataframe, The results of the weighted mean intent

        suggestions: Type - List of dictionaries(suggestion structure), List of
            suggestions.
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    day_first = kwargs.get('day_first', False)

    slices = kwargs.get('slices', None)

    summary_operator = kwargs.get('summary_operator', None)

    result_tuple = topk_results(table, metric, dimensions, is_asc, k,
                                date_column_name=date_column_name,
                                date_range=date_range, day_first=day_first,
                                slices=slices,
                                summary_operator=summary_operator)

    result_table = result_tuple[0]

    suggestions = result_tuple[1]

    duplicates_in_topk_suggestion = duplicates_in_topk(result_table, dimensions)

    if duplicates_in_topk_suggestion is not None:
        suggestions.append(duplicates_in_topk_suggestion)
    
    else:
        # Check for RMT suggestion only when no duplicates present.
        rmt_suggestion = regression_to_mean(table, metric, dimensions, is_asc, k,
                                            date_column_name=date_column_name,
                                            date_range=date_range,
                                            day_first=day_first, slices=slices,
                                            summary_operator=summary_operator)

        if rmt_suggestion is not None:
            suggestions.append(rmt_suggestion)

    results_without_k_condition = topk_results(table, metric, dimensions, is_asc, -1,
                                               date_column_name=date_column_name,
                                               date_range=date_range, day_first=day_first,
                                               slices=slices,
                                               summary_operator=summary_operator)[0]

    more_than_just_topk_suggestion = more_than_just_topk(results_without_k_condition, k, metric)

    if more_than_just_topk_suggestion is not None:
        suggestions.append(more_than_just_topk_suggestion)

    topk_vs_others_suggestion = topk_vs_others(results_without_k_condition, k, metric)

    if topk_vs_others_suggestion is not None:
        suggestions.append(topk_vs_others_suggestion)

    looking_at_tails_suggestion = looking_at_tails(results_without_k_condition, k, metric)

    if looking_at_tails_suggestion is not None:
        suggestions.append(looking_at_tails_suggestion)

    topk_when_less_than_k_present_suggestion = topk_when_less_than_k_present(result_table, k)

    if topk_when_less_than_k_present_suggestion is not None:
        suggestions.append(topk_when_less_than_k_present_suggestion)

    order = oversights_order.ORDER_IN_TOPK
    suggestions = rank_oversights.rank_oversights(suggestions, order)

    if summary_operator is not None:
        result_table = aspects.update_metric_column_name(result_table, summary_operator, metric)

    return (result_table, suggestions)

def topk_results(table, metric, dimensions, is_asc, k, **kwargs):
    """This function will implement the top-k intent

    Sorts tuples in the order metric, after applying slice, groupby operations.
    Also removes the tuples that do not lie in the given date range.
    The arguments 'table, metric,dimension,sort_order, k' are not optional,
    so they are passed as it is, rest of the arguments that are
    optional('date_range', 'slices') will be passed in kwargs.
    If the summary_operator is not None, it groups by dimensions.
    If some the optional args are None(not passed),
    it is assumed that we don't have to apply them.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we sort,
            and in the case when grouping has to be done,
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'top 5 batsman according to runs', dimension is 'batsman'.
            When summary_operator is not None, we group by dimensions.
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        k: Type-int
            It is the number of entries to be taken. Also k = -1 means taking
            all entries
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        day_first: Type-str
            Day_first denotes that does day in the date occurs before month in the
            dates in the date column
            Example - '29-02-19', here day_first is true
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
        The function will return both suggestions and the results in a tuple.
        (results, suggestions)
        results: Type - pandas dataframe, The results of the intended top-k
        suggestions: Type - List of strings, List of suggestions.

    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    day_first = kwargs.get('day_first', False)

    slices = kwargs.get('slices', None)

    summary_operator = kwargs.get('summary_operator', None)


    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, day_first)

    table = aspects.slice_table(table, slices)

    # collecting the colums not to be removed
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(metric)

    table = aspects.crop_other_columns(table, required_columns)

    after_group_by = aspects.group_by(table, dimensions, summary_operator)

    table = after_group_by['table']

    suggestions = after_group_by['suggestions']

    # using a stable sort('mergesort') will help to preserve the order
    # if equal values of [metric] are present
    table = table.sort_values(by=[metric], ascending=is_asc, kind = 'mergesort')

    # reordering the index
    # drop=True drops the new columnn named 'index' created in reset_index call
    table = table.reset_index(drop=True)

    # selecting only the top-k
    if k != -1:
        table = table.head(k)

    return (table, suggestions)