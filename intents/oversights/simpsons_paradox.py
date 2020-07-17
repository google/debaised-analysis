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
This module contains the simpson's paradox debaising.
The simpson_paradox module can give user result, according to which
column group of column simpson paradox exist for some perticular
slicing. It will check simpson's-paradox for all related groups and
suggest the user to do operation on those groups.
"""
import pandas
from util import aspects
from util.enums import SummaryOperators, Filters
from util import constants 

def simpsons_paradox(table, metric, all_dimensions, slice_compare_column, 
                            slice1, slice2, summary_operator, **kwargs):
    """This function will implement the simpson's-paradox debaising

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        metric: Type-string
            It is the name of the column according to which we will do grouping,
            summary operator is applied on metric. Metric could a column
            containing strings, if we are applying count operator on it.
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

    """removing all metric column except the one by which we will
       do group_by operation"""
    required_columns = all_dimensions.copy()
    required_columns.append(metric)
    table = aspects.crop_other_columns(table, required_columns)

    """operational_dimensions will contain list of all dimension
       except slice_compare_column"""
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

    # initial_result_table is the result table requested by user.
    initial_result_table = aspects.group_by(query_table,
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
            new_suggestion =  _check_simpsons_paradox(initial_result_table,
                                                      new_result_table, 
                                                      column, slice1,
                                                      dimensions_len)
            if new_suggestion != None:
                suggestions.append(new_suggestion)
    return suggestions

def _check_simpsons_paradox(initial_result_table, new_result_table, new_added_column,
                                                              slice1, dimensions_len):
    """
    Args:
        initial_result_table: Type-pandas.dataframe
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
    initial_num_rows = initial_result_table.shape[0]
    new_num_rows = new_result_table.shape[0]

    # changing dataframe to list of list to do next set of operation
    initial_table_matrix = initial_result_table.values.tolist()
    new_table_matrix = new_result_table.values.tolist()

    initial_row_i = 0
    new_row_i = 0

    suggestion_row_list = []

    """ dominant percentage is the percentage of pairs where 
        (first value - second value) is positive."""

    while initial_row_i < initial_num_rows:

        # check if it is the last row or there is only one slice for this group.
        if initial_row_i == initial_num_rows - 1 or initial_table_matrix[initial_row_i][:dimensions_len] != initial_table_matrix[initial_row_i + 1][:dimensions_len]:

            initial_difference = 0
            if initial_table_matrix[initial_row_i][dimensions_len] == slice1:
                initial_difference = initial_table_matrix[initial_row_i][dimensions_len + 1]
            else:
                initial_difference = -initial_table_matrix[initial_row_i][dimensions_len + 1]
            
            # it stores the dominent percent for the initial table
            initial_dominant_percent = 0
            if initial_difference > 0:
                initial_dominant_percent = 100

            positive_count = 0
            total_count = 0

            # while the group data is same for both the table it will continue in the loop
            while new_row_i < new_num_rows and initial_table_matrix[initial_row_i][:dimensions_len] == new_table_matrix[new_row_i][:dimensions_len] :
                new_difference = 0
                if new_table_matrix[new_row_i][dimensions_len + 1] == slice1:
                    new_difference = new_table_matrix[new_row_i][dimensions_len + 2]
                else:
                    new_difference = -new_table_matrix[new_row_i][dimensions_len + 2]
                
                if new_difference > 0:
                    positive_count = positive_count + 1
                total_count = total_count + 1

                new_row_i = new_row_i + 1

            new_dominant_percent = (positive_count / total_count) * 100

            # Finally according to the difference between dominent percentage we shall
            # add the debiasing suggestion.
            if abs(initial_dominant_percent - new_dominant_percent) >= constants.SP_THRESHOLD:
                suggestion_row_list.append(initial_row_i)
        else:
            initial_difference = 0
            if initial_table_matrix[initial_row_i][dimensions_len] == slice1:
                initial_difference = initial_table_matrix[initial_row_i][dimensions_len + 1] - initial_table_matrix[initial_row_i + 1][dimensions_len + 1]
            else:
                initial_difference = initial_table_matrix[initial_row_i + 1][dimensions_len + 1] - initial_table_matrix[initial_row_i][dimensions_len + 1]
            
            # it stores the dominent percent for the initial table
            initial_dominant_percent = 0
            if initial_difference > 0:
                initial_dominant_percent = 100

            positive_count = 0
            total_count = 0

            # while the group data is same for both the table it will continue in the loop
            while new_row_i < new_num_rows and initial_table_matrix[initial_row_i][:dimensions_len] == new_table_matrix[new_row_i][:dimensions_len] :
                new_difference = 0

                if new_row_i == new_num_rows - 1 or new_table_matrix[new_row_i][:dimensions_len + 1] != new_table_matrix[new_row_i + 1][:dimensions_len + 1]:
                    if new_table_matrix[new_row_i][dimensions_len + 1] == slice1:
                        new_difference = new_table_matrix[new_row_i][dimensions_len + 2]
                    else:
                        new_difference = -new_table_matrix[new_row_i][dimensions_len + 2]
                else:
                    if new_table_matrix[new_row_i][dimensions_len + 1] == slice1:
                        new_difference = new_table_matrix[new_row_i][dimensions_len + 2] - new_table_matrix[new_row_i + 1][dimensions_len + 2]
                    else:
                        new_difference = new_table_matrix[new_row_i + 1][dimensions_len + 2] - new_table_matrix[new_row_i][dimensions_len + 2]
                    new_row_i = new_row_i + 1

                if new_difference > 0:
                    positive_count = positive_count + 1
                total_count = total_count + 1

                new_row_i = new_row_i + 1

            new_dominant_percent = (positive_count / total_count) * 100

            # Finally according to the difference between dominent percentage we shall
            # add the debiasing suggestion.
            if abs(initial_dominant_percent - new_dominant_percent) >= constants.SP_THRESHOLD:
                suggestion_row_list.append(initial_row_i)
                suggestion_row_list.append(initial_row_i + 1)

            initial_row_i = initial_row_i + 1;
        initial_row_i = initial_row_i + 1

    if len(suggestion_row_list) == 0:
        return None
    else:
        new_suggestion = {}
        new_suggestion['suggestion'] = 'the relation between slices might changed a lot if you will consider ' + new_added_column + ' in grouping.'
        new_suggestion['oversight_name'] = 'simpsons-paradox'
        new_suggestion['is_row_level_suggestion'] = True
        new_suggestion['row_list'] = suggestion_row_list
        return new_suggestion
            

        