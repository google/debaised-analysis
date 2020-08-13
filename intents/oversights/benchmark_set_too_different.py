 
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

"""This module detects the cases of Benchmark set too different
   oversight in slice-compare intent.
It can give the columns name which might affect the user's results and 
user's might not be aware of it. It can also given the list of rows on
which the disimilarity might have appeared.
"""

import pandas
from util import aspects, constants
from util.enums import SummaryOperators, Filters, Oversights

def benchmark_set_too_different(table, metric, all_metric, slice_compare_column, 
                                slice1, summary_operator, **kwargs):
    """This function can give the benchmark set too different oversight.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we will do grouping,
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'compare batsman A and B according to total_runs',
             dimension is 'batsman'. we group by dimensions.
        all_metric: Type-list of str
            It contains list of all metrics
        slice_compare_column: Type-list of string
            first element denotes the column name by which we will do comparision.
            rest elements will the value belongs to that column by which we
            will compare the slices.
        summary_operator: Type-summary_operators enum members
            It denotes the summary operator, after grouping by dimensions.
            ex. SummaryOperators.MAX, SummaryOperators.SUM

    Note-summary_operator is always applied on metric column passed,
         and only when grouping is done

    Returns:
        return a list of dictionary in which every dictionary represent
               a oversight for some column.

    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    day_first = kwargs.get('day_first', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, 
                                     day_first)

    table = aspects.slice_table(table, slices)

    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(slice_compare_column)
    required_columns = required_columns + all_metric

    table = aspects.crop_other_columns(table, required_columns)

    """ required_table_for_one is a table which has data for the 
        single variable given by the user by which we shall do 
        comparision"""
    required_table_for_one = aspects.slice_table(table, [(slice_compare_column, 
                                                 Filters.EQUAL_TO, slice1)])

    """ required_table_for_all is a table which has all the data which was in
        the initial table but with the comparision column as '*' because we
        have to compare single value with the whole table"""
    required_table_for_all = table.copy()
    required_table_for_all[slice_compare_column] = '*'

    updated_table = pandas.concat([required_table_for_one, required_table_for_all])
    updated_table = updated_table.reset_index()
    
    grouping_columns = []
    if dimensions is not None:
        grouping_columns = dimensions.copy()
    grouping_columns.append(slice_compare_column)
    
    result_table = aspects.group_by(updated_table, grouping_columns, summary_operator)['table']

    other_metrics = all_metric.copy()
    other_metrics.remove(metric)

    columns_order = grouping_columns.copy()
    columns_order.append(metric)
    columns_order = columns_order + other_metrics

    """ We have done the reordering of columns so that all the dimension
        should appear first followed by the metric given by the user and
        and then rest of the columns."""
    result_table = result_table[columns_order]

    num_rows = result_table.shape[0]
    num_columns = result_table.shape[1]
    dimensions_len = 0
    if dimensions is not None:
        dimensions_len = len(dimensions)

    result_table_matrix = result_table.values.tolist()

    suggestion = []

    # We have to iterate through all metric which was not involved 
    # in the computation initially.
    for column_i in range(dimensions_len + 2, num_columns):
        # it can store the index of row on whcih the oversight might appear.
        column_i_suggestion_list = []
        row_i = 0
        while row_i < num_rows:
            if row_i == num_rows - 1 or result_table_matrix[row_i][:dimensions_len] != result_table_matrix[row_i + 1][:dimensions_len]:
                column_i_suggestion_list.append({'row':row_i + 1, 'confidence_score':100})
            else:
                if _calculate_relation(result_table_matrix[row_i][column_i], result_table_matrix[row_i + 1][column_i]) < constants.BSTD_DISIMILARITY_THRESHOLD:
                    row_i = row_i + 1
                elif _calculate_relation(result_table_matrix[row_i][dimensions_len + 1], result_table_matrix[row_i + 1][dimensions_len + 1]) < constants.BSTD_DISIMILARITY_THRESHOLD:
                    row_i = row_i + 1
                else:
                    column_i_suggestion_list.append({'row':row_i + 1, 'confidence_score':100})
                    column_i_suggestion_list.append({'row':row_i + 2, 'confidence_score':100})
                    row_i = row_i + 1
            row_i = row_i + 1

        if len(column_i_suggestion_list) > 0:
            """ for every suggestion we form a dictionary and 
                append it to the list of dictionary."""
            suggestion_i = {}
            suggestion_i['suggestion'] = slice1 + ' looks different from others on ' + metric + '. You might also want to look at ' + columns_order[column_i] +' since ' + slice1 + ' also looks different on this.'
            suggestion_i['oversight'] = Oversights.BENCHMARK_SET_TOO_DIFFERENT
            suggestion_i['is_row_level_suggestion'] = True
            suggestion_i['row_list'] = column_i_suggestion_list
            suggestion.append(suggestion_i)

    if len(suggestion) == 0:
        return None
    else:
        return suggestion

def _calculate_relation(val1, val2):
    """
    This function can find the similarity between two values
    """

    """
    Arg:
        val1: the first value for which we have to compute the similarity
        val2: the second value for which we have to compute the similarity

    Returns:
        return the similarity between both the arguments calculated by the
        formula
        similarity = |val1 - val2| / (|val1| + |val2|)
    """

    if (abs(val1) + abs(val2)) == 0:
        return 0
    result = abs(val1 - val2) / (abs(val1) + abs(val2))

    return result