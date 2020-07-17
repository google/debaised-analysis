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

"""This module detects the cases of regression to the mean in the top-k
intent.
Regression toward the mean is the phenomenon that arises if a random
variable is extreme on its first or first few measurements but closer
to the mean or average on further measurements.
If the top-k is queried for a time window in which the results look much
different from the previous window, or the next window of the same size, the
oversight suggestion is passed.
"""
import datetime
import math
from util import aspects, constants, time_window
from util.enums import *
import topk

def regression_to_mean(table, metric, dimensions, is_asc, k, **kwargs):
    """ This function gives suggestions if the regression to the
    mean oversight is detected in the top-k results.
    It checks the top-k results under the same slicingcondition
    in the previous window, and if those results differ a lot it
    returns the debiasing suggestion. It has 2 methods to check
    if the 2 results differ.
    1. Set intersection method.
        Checks if the sets formed by both the results differs a lot.
    2. Similartity in the ranks method.
        Checks if the ranks of the common items in both the
        results differ a lot.

    The cut-off in both the methods is fixed in the util/constants module

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

    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name'
    """
    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')
    slices = kwargs.get('slices', None)
    summary_operator = kwargs.get('summary_operator', None)

    # top-k in the given time window
    current_topk = topk.topk_results(table, metric, dimensions, is_asc, k,
                                     date_column_name=date_column_name,
                                     date_range=date_range,
                                     date_format=date_format, slices=slices,
                                     summary_operator=summary_operator)

    if date_range is None:
        return

    current_topk_set = _convert_to_set(current_topk, dimensions)

    # results of the other time interval may contain duplicates,
    # so setting the summary operator to MAX/MIN
    if summary_operator is None:
        if is_asc:
            summary_operator = SummaryOperators.MIN
        else:
            summary_operator = SummaryOperators.MAX

    # start & end dates of the previous time window
    previous_start, previous_end = time_window.previous(date_range[0],
                                                        date_range[1],
                                                        date_format)

    # top-k in previous window
    previous_topk = topk.topk_results(table, metric, dimensions, is_asc, k,
                                      slices=slices,
                                      summary_operator=summary_operator,
                                      date_column_name=date_column_name,
                                      date_format=date_format,
                                      date_range=(previous_start, previous_end))

    set_intersect_suggestions = _set_intersect(previous_topk,
                                              current_topk, dimensions)

    suggestion = {}
    suggestion['oversight_name'] = 'Regression to the mean'

    if set_intersect_suggestions is not None:
        suggestion['suggestion'] = set_intersect_suggestions
        return suggestion

    rank_vector_suggestion = _similarity_between_ranks(previous_topk,
                                                      current_topk, dimensions)

    if rank_vector_suggestion is not None:
        suggestion['suggestion'] = rank_vector_suggestion
        return suggestion

    return None

def _set_intersect(table1, table2, columns):
    """ This function suggests oversight if the size
    of intersection/size of union is less than a fixed value

    Args:
        table1, table2 : Type-pandas dataframe.
            The 2 top-k results that are to be compared.
        dimensions: Type-list
            It is the list of columns that we rank.
            Example - In query:'top 5 batsman according to runs',
            dimension is 'batsman'.
    Returns:
        A suggestion of type-str if the intersection between the 2
        results is less compared to their union. The cut-off is used
        is taken from util.constants
    """
    set1 = _convert_to_set(table1, columns)
    set2 = _convert_to_set(table2, columns)

    score = len(set1.intersection(set2))

    normalizing_factor = len(set1.union(set2))

    # handelling the 0/0 division case.
    if normalizing_factor != 0:
        score = score / normalizing_factor
    else:
        score = 0

    if score == 0:
        return 'None of the top-k in the given date range will be in the previous window\'s top-k'
    elif score <= constants.RTM_SET_INTERSECTION_CUT_OFF:
        return 'very few of the top-k in the given date range will be in the previous window\'s top-k'
    else:
        return None

def _similarity_between_ranks(table1, table2, dimensions):
    """ This function gives suggestions if the rank vector of the 2 passed
    results differ a lot. Uses the angle between the 2 vectors as a parameter.

    Args:
        table1, table2 : Type-pandas dataframe.
            The 2 top-k results that are to be compared.
        dimensions: Type-list
            It is the list of columns that we rank.
            Example - In query:'top 5 batsman according to runs',
            dimension is 'batsman'.
    Returns:
        A suggestion of type-str if the angle between the 2 vectors excedes a
        cutoff value, that is taken from util.constants
    """
    common_rows = _convert_to_set(table1, dimensions).intersection(_convert_to_set(table2, dimensions))

    rank_vector_1 = _rank_vector(table1, dimensions)
    rank_vector_2 = _rank_vector(table2, dimensions)

    angle = _angle_between_vectors(rank_vector_1, rank_vector_2, common_rows)

    if angle < constants.RTM_RANK_VECTOR_SIMILARITY_THRESHOLD:
        return None
    else:
        return 'The ranks of the top-k in the date range differs much from the previous window\'s top-k'

def _angle_between_vectors(vector_1, vector_2, common_rows):
    """ Calculates the angle in between the 2 rank vectors.
    Uses dot product to calculate the cosine of the angle, then math.acos to
    convert into angle.

    Args:
        vector_1, vector_2: Type-Dict
            The Angle is calculated in between these 2 vectors.
            The keys of the vector are the axis of the vector,
            and values are the length in that axis.
        common_rows: Type-list
            The rows which are to be taken into consideration while calculating the angle.
            The are the rows that are common in both the vector.
    Returns:
        The angle in between the 2 vectors in degree.
    """
    cross_product = 0
    magnitude1 = 0
    magnitude2 = 0

    for x in common_rows:
        cross_product = cross_product + vector_1[x]*vector_2[x]
        magnitude1 = magnitude1 + vector_1[x]*vector_1[x]
        magnitude2 = magnitude2 + vector_2[x]*vector_2[x]

    cosine_angle = cross_product / (math.sqrt(magnitude1 * magnitude2))

    angle = math.acos(cosine_angle)

    # angle in degrees
    angle = angle*180/math.pi

    return angle

def _rank_vector(table, columns):
    """ Calculates the rank vector of the table passed
    Applies a mathematical function to makes the ranks closer to each other.

    Args:
        table - Type-pandas.dataframe
            The table whose rank vector is to be calculated.
        columns - Type-List
            The columns whose rank is to be considered.

    Returns:
        A python dictionary which represent the rank vector.
        Keys are the row in form of tuple, and keys are log(2+rank)
    """
    # rows as keys & ranks as values
    rank_vector_dict = {}
    num_rows1 = table.shape[0]
    for row in range(num_rows1):
        list_row = []
        for col in columns:
            list_row.append(table.loc[row, col])
        # Using log because Ex- rank-999 & rank-1000 are more
        # similar compared to rank-1 and rank-2 -- may be changed
        rank_vector_dict[tuple(list_row)] = math.log(2+row)
    return rank_vector_dict

def _convert_to_set(table, columns):
    """ Converts the columns of the table which are in the
    list- columns into a set of tuples.

    First the other columns are dropped, then the columns are
    inseted into the a set as tuples and returned.

    Args:
        table - Type-pandas.dataframe
            The table that is to be converted into a python set

    Returns:
        The function will return a set containing the required colums
        of the table as tuples.
    """
    table = aspects.crop_other_columns(table, columns)
    result_set = set()
    num_rows = table.shape[0]
    for row in range(num_rows):
        list_row = []
        for col in columns:
            list_row.append(table.loc[row, col])
        result_set.add(tuple(list_row))
    return result_set
