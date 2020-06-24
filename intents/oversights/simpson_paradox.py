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

from util import aspects
from util.enums import SummaryOperators

def simpson_paradox(table, metric, dimensions, all_dimensions, 
						slice_compare_column, summary_operator):
	"""This function will implement the simpson's-paradox debaising

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
        all_dimension: Type-list of str
        	It contains list of all dimensions
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
        return a string with debiasing suggestion or empty string.

    """

	""" removing all metric column except the one by which we will 
			 								do group_by operation"""
	required_columns = all_dimensions.copy()
	required_columns.append(metric)
	table = aspects.crop_other_columns(table, required_columns)

	""" operational_dimensions will contain list of all dimension 
									except slice_compare_column"""
	operational_dimensions = all_dimensions.copy()
	operational_dimensions.remove(slice_compare_column[0])
	grouping_dimensions = dimensions.copy()

	# slice_compare_column should be the last value of the list
	grouping_dimensions.remove(slice_compare_column[0])
	grouping_dimensions.append(slice_compare_column[0])

	required_table = table.copy()
	required_columns = grouping_dimensions.copy()
	required_columns.append(metric)
	required_table = aspects.crop_other_columns(required_table,
											 required_columns)

	"""initial_result will store the dominent percentage of 
							initial groups given by user."""
	initial_result = check_dominent_percentage(required_table, 
										grouping_dimensions, 
										slice_compare_column, 
										summary_operator)
	simpson_paradox_columns = []
	max_difference = 75
	
	for column in operational_dimensions:
		new_grouping_dimensions = dimensions.copy()
		new_grouping_dimensions.remove(slice_compare_column[0])
		new_grouping_result = 0

		""" if column is already in grouping_dimensions then 
					we will remove it otherwise we will 
					add the column to grouping_dimensions"""
		if (column in grouping_dimensions):
			new_grouping_dimensions.remove(column)
			new_grouping_dimensions.append(slice_compare_column[0])

			required_table = table.copy()
			required_columns = new_grouping_dimensions.copy()
			required_columns.append(metric)
			required_table = aspects.crop_other_columns(required_table, 
														required_columns)

			new_grouping_result = check_dominent_percentage(required_table, 
											new_grouping_dimensions.copy(), 
											slice_compare_column, 
											summary_operator)
		else:
			new_grouping_dimensions.append(column)
			new_grouping_dimensions.append(slice_compare_column[0])

			required_table = table.copy()
			required_columns = new_grouping_dimensions.copy()
			required_columns.append(metric)
			required_table = aspects.crop_other_columns(required_table, 
														required_columns)

			new_grouping_result = check_dominent_percentage(required_table, 
													new_grouping_dimensions, 
													slice_compare_column, 
													summary_operator)

		if abs(new_grouping_result - initial_result) >= max_difference:
			max_difference = abs(new_grouping_result - initial_result)
			simpson_paradox_columns = new_grouping_dimensions
	if len(simpson_paradox_columns) > 0:
		suggestion = str(simpson_paradox_columns)
		suggestion = suggestion + ' these group of columns have different results than initial columns so you might also look for the given group of columns'
		return suggestion
	else:
		return ""

def check_dominent_percentage(table, dimensions, slice_compare_column, 
													summary_operator):
	"""This function can compare all the numbers of first and second 
		slice and return what ppperceeentage of nnnnumbers of first 
		slice if greater than the second slice.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the csv file
        dimensions: Type-list of str
            It is the name of column we want.
            In query:'compare batsman A and B according to total_runs', 
            dimension is 'batsman'. we group by dimensions.
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
        Percentage of value slices for which the first slice has higher
        value than second slice
    """

	table = aspects.group_by(table, dimensions, summary_operator)

	num_rows = table.shape[0]
	num_columns = table.shape[1]

	table_matrix = table.values.tolist()
	positive_count = 0
	total_count = 0
	row_i = 0

	while row_i < num_rows:
		difference = 0
		if row_i == num_rows - 1 or table_matrix[row_i][:(num_columns-2)] != table_matrix[row_i+1][:(num_columns-2)]:
			difference = 0
			if table_matrix[row_i][num_columns-2] == slice_compare_column[1]:
				difference = table_matrix[row_i][num_columns-1]
			else:
				difference = -table_matrix[row_i][num_columns-1]
		else:
			if table_matrix[row_i][num_columns-2] == slice_compare_column[1]:
				difference = table_matrix[row_i][num_columns-1] - table_matrix[row_i+1][num_columns-1]
			else:
				difference = table_matrix[row_i+1][num_columns-1] - table_matrix[row_i][num_columns-1]
			row_i = row_i + 1
		if difference > 0:
			positive_count = positive_count + 1

		total_count = total_count + 1
		row_i = row_i + 1

	return (positive_count / total_count) * 100
    
