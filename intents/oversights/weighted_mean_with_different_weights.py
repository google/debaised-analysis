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
"""The module detects cases of Weighted mean with different weights
oversight when user uses the weighted mean intent & show intent when
summary operator used is mean.

Weighted mean with different weights oversight gives a debiasing
suggestion to use weighted mean intent with different weights.
The columns that it suggests to as weights are the column that
positive entries & all entries sum up to either 1 or 100.
The columns whose sum is 1 or 100 would be proportion/percentage
columns and will possibly be meaningfull when used as weights.
"""

def weighted_mean_with_different_weights(table, metric, **kwargs):
    """
    The function checks for Weighted mean with different weights in
    the user table.

    In the function each column in the initial table is iterated
    upon and if a column has all entries positive & sum of entries
    is either 1 or 100 & it is not equal to metric column & weight
    column, it is listed as possible weight columns.

    There is no cut-off for this oversight as there is no parameter
    involved.

    Args:
        table: Type-pandas.dataframe
            It has the contents of the table in sheets, without
            applying any operations
        metric: Type-String
            The column name whose mean/weighted mean is to be found.
        weight_col : Type-string (Optional)
            The weight column which is multiplied as weights to
            metric column when intent is weighted mean.


    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name',
                     'is_column_level_suggestion', 'col_list'.
    """

    weight_col = kwargs.get('weight_col', None)

    # Initializing list of possible weight columns
    possible_weight_columns = []

    for column in table.columns:
        if str(table[column].dtype) in ['float64', 'int64'] and\
            column not in [metric, weight_col] and\
            table[column].min() >= 0 and\
            table[column].sum() in [1, 100]:

            possible_weight_columns.append(column)

    # if there are possible weight columns return an oversight
    if possible_weight_columns:
    	suggestion = {}
    	suggestion['oversight_name'] = 'Weighted mean with different weights'
    	suggestion['suggestion'] = 'Consider using {columns} as the weights for computing weighted mean.'\
    	    .format(columns=str(possible_weight_columns))
    	suggestion['is_column_level_suggestion'] = True
    	suggestion['col_list'] = possible_weight_columns

    	return suggestion
    else:
    	return None
