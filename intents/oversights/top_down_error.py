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

"""
This module contains the top-down erro debaising.
The top_down_error module can give user result, according to which
column group of column top-down error exist for some perticular
slicing. It will check top-down error for all related groups and
suggest the user to do operation on those groups.
"""
import pandas
from util import aspects
from util.enums import SummaryOperators, Filters
from util import constants 
def top_down_error(table, metric, all_dimensions, slice_compare_column, 
                            slice1, slice2, summary_operator, **kwargs):
    """This function will implement the top down error debaising

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we will do 
            grouping, summary operator is applied on metric. Metric 
            could a column containing strings, if we are applying count 
            operator on it.
        dimensions: Type-list of str or None
            It is the name of column we want.
            In query:'compare batsman A and B according to total_runs',
             dimension is 'batsman'. we group by dimensions.
        all_dimension: Type-list of str
        	It contains list of all dimensions
        slice_compare_column: Type-string
            name of the slice-compare column.
        slice1: Type-string
            the first value of comparision
        slice2: Type-string
            the second value of comparision
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in 
            the format Format Codes
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
        return a list of dictionary where each dictionary represent
               a debiasing suggestion according to the new column.
    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    dimensions = kwargs.get('dimensions', None)

    table = aspects.apply_date_range(table, date_range,
                                     date_column_name, date_format)
    
    slice_list = []
    if slices is not None:
        slice_list = slices.copy()
    slice_list.append((slice_compare_column, Filters.IN, [slice1, slice2]))

    table = aspects.slice_table(table, slice_list)

    # removing all metric column except the one by which we do 
    # group_by operation
    required_columns = all_dimensions.copy()
    required_columns.append(metric)
    table = aspects.crop_other_columns(table, required_columns)

    # operational_dimensions contain list of all dimension except 
    # slice_compare_column
    operational_dimensions = all_dimensions.copy()
    operational_dimensions.remove(slice_compare_column)
    
    required_columns = []
    if dimensions is not None:
        required_columns = dimensions.copy()
    required_columns.append(slice_compare_column)
    required_columns.append(metric)

    query_table = aspects.crop_other_columns(table, required_columns)

    grouping_columns = []
    if dimensions is not None:
        grouping_columns = dimensions.copy()
    grouping_columns.append(slice_compare_column)

    # result_table is the result table requested by user.
    result_table = aspects.group_by(query_table,
                                            grouping_columns,
                                            summary_operator)
    # suggestions store the list of debiasing for this oversight.
    suggestions = []

    dimension_list = []
    if dimensions is not None:
        dimension_list = dimensions.copy()

    dimensions_len = len(dimension_list)
               
    for column in operational_dimensions:
        # we try to find the debiasing for every column which 
        # is not in the grouping list initially
        if column not in dimension_list:
            new_grouping_columns = dimension_list.copy()
            new_grouping_columns.append(column)
            new_grouping_columns.append(slice_compare_column)

            new_required_columns = new_grouping_columns.copy()
            new_required_columns.append(metric)
            new_cropped_table = aspects.crop_other_columns(table, 
                                            new_required_columns)

            # result table after adding the new column in the grouping list.
            new_result_table = aspects.group_by(new_cropped_table,
                                                new_grouping_columns,
                                                summary_operator)

            # it will return the debiasing suggestion after comparing the
            # initial result table and new result table.
            new_suggestion =  _check_top_down_error(result_table,
                                                      new_result_table, 
                                                      column, slice1,
                                                      dimensions_len)
            if new_suggestion != None:
                suggestions.append(new_suggestion)
    return suggestions
              
def _check_top_down_error(result_table, new_result_table, new_added_column,
                                                    slice1, dimensions_len):
    """
    Args:
        result_table: Type-pandas.dataframe
            It has the contents of the csv file
        new_result_table: Type-pandas.dataframe
            It has the contents of the csv file
        new_added_column: Type-string
            The new column added in the initial grouping column.
        slice1: Type-string
            the first slice by which we do comparision.
        dimensions_len: Type-integer
            size of the initial gfrouping dimensions.

    Returns:
        return a dictionary where each dictionary represent a debiasing 
               suggestion according to the new column.
    """
    num_rows = result_table.shape[0]
    new_num_rows = new_result_table.shape[0]

    # changing dataframe to list of list to do next set of operation
    table_matrix = result_table.values.tolist()
    new_table_matrix = new_result_table.values.tolist()

    row_i = 0
    new_row_i = 0

    suggestion_row_list = []

    # dominant percentage is the percentage of pairs where 
    # (first value - second value) is positive.
            
    while row_i < num_rows:
        if row_i == num_rows - 1 or table_matrix[row_i][:dimensions_len] != \
                                    table_matrix[row_i + 1][:dimensions_len]:
            while new_row_i < new_num_rows and \
                  table_matrix[row_i][:dimensions_len] == \
                  new_table_matrix[new_row_i][:dimensions_len]:
                new_row_i = new_row_i + 1
        else:
            new_max_correlation = 0
            while new_row_i < new_num_rows and \
                  table_matrix[row_i][:dimensions_len] == \
                  new_table_matrix[new_row_i][:dimensions_len]:
                if new_row_i == new_row_i - 1 or \
                new_table_matrix[new_row_i][:dimensions_len + 1] != \
                new_table_matrix[new_row_i + 1][:dimensions_len + 1]:
                    max_disimilarity = constants.TOP_DOWN_ERROR_DISSIMILARITY_THRESHOLD
                else:
                    correlation = _calculate_relation(
                        new_table_matrix[new_row_i][dimensions_len + 2], 
                        new_table_matrix[new_row_i + 1][dimensions_len + 2])
                    new_max_correlation = max(correlation, new_max_correlation)
                    new_row_i = new_row_i + 1
                new_row_i = new_row_i + 1
               
            correlation = _calculate_relation(
                          table_matrix[row_i][dimensions_len + 1], 
                          table_matrix[row_i + 1][dimensions_len + 1])

            if new_max_correlation >= \
            constants.TOP_DOWN_ERROR_DISSIMILARITY_THRESHOLD and \
            correlation <= constants.TOP_DOWN_ERROR_SIMILARITY_THRESHOLD:
                suggestion_row_list.append(row_i)
                suggestion_row_list.append(row_i + 1)
            row_i = row_i + 1

        row_i = row_i + 1

    if len(suggestion_row_list) == 0:
        return
    else:
        new_suggestion = {}
        new_suggestion['suggestion'] = 'both the value is almost same in \
some grouping but different if we add ' + new_added_column + ' in initial grouping.'
        new_suggestion['oversight_name'] = 'top-down error'
        new_suggestion['is_row_level_suggestion'] = True
        new_suggestion['row_list'] = suggestion_row_list
        return new_suggestion

def _calculate_relation(val1, val2):
    """
    This function can find the similarity between two values

    Arg:
        val1: the first value for which we have to compute the similarity
        val2: the second value for which we have to compute the similarity

    Returns:
        return the similarity between both the arguments calculated by the
        formula
        similarity = |val1 - val2| / (|val1| + |val2|)
    """

    if abs(val1) + abs(val2) == 0:
        return 0
    result = abs(val1 - val2) / (abs(val1) + abs(val2))

    return result
