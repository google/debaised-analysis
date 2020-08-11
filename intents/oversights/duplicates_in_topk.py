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

"""This module detects if there are duplicates in the top-k results.
Having duplicates in the top-k results might create a bias in the user's
thinking. Also, chances are that user forgot to apply group by operation
due to which duplicates occur in the results.
"""
from util import aspects, enums

def duplicates_in_topk(topk_results, dimensions):
    """
    This functions checks if there are duplicate entries present in the
    results of the top-k.

    First, it insert the rows of the results in a set, & then checks if
    the size of the set matches with the size of the topk_results.

    Args:
        topk_results : Type-Pandas dataframe
            The results of the top_k intent
        dimensions : Type-list of str
            The column names in which we look for duplicates 
    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name'
    """
    topk_results_set = _convert_to_set(topk_results, dimensions)

    # Checking if the result table contains duplicates
    if len(topk_results_set) != topk_results.shape[0]:
    	suggestion = {}
    	suggestion['suggestion'] = 'The results has duplicates'
    	suggestion['oversight'] = enums.Oversights.DUPLICATES_IN_TOPK
    	return suggestion

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
