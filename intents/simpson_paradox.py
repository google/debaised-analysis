""" 
	**Some improvement will be done in this code, all ideas for better implementation will be appreciated.
	1. commenting part will be done later. 
	2. Implementation part will be improved by using some python function.
	3. Variable name will be changed according to the need.
"""
from Utilities import aspects
from Utilities import enumerations
import pandas as pd

def check_simpson_paradox(table, dimension, slice_compare, summary_operator):
	slice_compare_column = list(slice_compare.keys())[0]
	dimension.append(slice_compare_column)
	slice_val_list = list(slice_compare.values())
	sliced_val = slice_val_list[0]
	sliced_val.sort()

	table = aspects.group_by(table, dimension, summary_operator)

	num_rows = table.shape[0]
	num_columns = table.shape[1]
	positive_count = 0
	negative_count = 0
	zero_count = 0
	total_count = 0
	row_i = 0

	while row_i < num_rows:
		if row_i == num_rows - 1:
			difference = 0
			if table.loc[row_i][num_columns - 2] == sliced_val[0]:
				difference = table.loc[row_i][num_columns - 1]
			else:
				difference = -table.loc[row_i][num_columns - 1]
			if difference < 0:
				negative_count = negative_count + 1
			elif difference > 0:
				positive_count = positive_count + 1
			else:
				zero_count = zero_count + 1
			total_count = total_count + 1
			break
		equality_check = True
		for column_i in range(num_columns-2):
			if table.loc[row_i][column_i] != table.loc[row_i+1][column_i]:
				equality_check = False
		if equality_check == True:
			difference = table.loc[row_i][num_columns - 1] - table.loc[row_i+1][num_columns - 1]
			if difference < 0:
				negative_count = negative_count + 1
			elif difference > 0:
				positive_count = positive_count + 1
			else:
				zero_count = zero_count + 1
			total_count = total_count + 1
			row_i = row_i + 1
		else:
			difference = 0
			if table.loc[row_i][num_columns - 2] == sliced_val[0]:
				difference = table.loc[row_i][num_columns - 1]
			else:
				difference = -table.loc[row_i][num_columns - 1]
			if difference < 0:
				negative_count = negative_count + 1;
			elif difference > 0:
				positive_count = positive_count + 1;
			else:
				zero_count = zero_count + 1;
			total_count = total_count + 1;
		row_i = row_i + 1
	return (positive_count/total_count)*100
    
def simpson_paradox(table, dimension, grouping, summary_operation_column, slice_compare, summary_operator):
	dimension.append(summary_operation_column)
	table = aspects.corp_other_columns(table, dimension)
	dimension.remove(summary_operation_column)

	slice_compare_column = list(slice_compare.keys())[0]
	dimension.remove(slice_compare_column)
	grouping.remove(slice_compare_column)
	temp_grouping = grouping.copy()

	temp_table = table.copy()
	initial_result = check_simpson_paradox(temp_table, temp_grouping, slice_compare, summary_operator)
	maximum_result = initial_result
	minimum_result = initial_result
	for column in dimension:
		temp_grouping = grouping.copy()
		temp_table = table.copy()
		if (column in grouping):
			temp_grouping.remove(column)
			temp_result = check_simpson_paradox(temp_table, temp_grouping, slice_compare, summary_operator)
			maximum_result = max(maximum_result, temp_result)
			minimum_result = min(minimum_result, temp_result)
	return [maximum_result, minimum_result, initial_result]

# please find the example bellow
df = pd.DataFrame({'team_name': ['MI','MI','CSK','CSK','MI','CSK','CSK','MI'], 
	'city_name': ['patna','patna', 'patna', 'darbhanga', 'darbhanga', 'darbhanga', 'delhi', 'bangalore'],
	'score': [1,2,3,4,4,5,6,7]})
enum_variable = enumerations.SummaryOperators
slices = {
	'team_name': ['MI','CSK']
}
print(df)

print(simpson_paradox(df, ['team_name', 'city_name'], ['team_name', 'city_name'], 'score', slices, enum_variable.summation))