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
This module implements the 'TopK when less than k present.

'TopK when less than k present' oversight arises when there are less than
k entries present in the result table of the top-k intent.

This oversight would be very useful in the case when the entire
table is not visible to the user & it is difficult for him to scroll.
"""

def topk_when_less_than_k_present(result_table, k):
    """
    This function returns the suggestion when the 'TopK when less than k present'
    oversight is detected.

    In the detection it is simply checked if the number of rows in the
    results is less than k or not.

    Args:
        result_table: Type-pandas DataFrame
            Is the result of the top-k intent
        k: Integer
            It is the number of entries to be taken
    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name'
    """
    num_rows = result_table.shape[0]

    if num_rows < k and k != -1:
    	suggestion = {}
    	suggestion['suggestion'] = 'Instead of {} only {} rows are present in the results'.format(k, num_rows)
    	suggestion['oversight_name'] = 'TopK when less than k present'
    	return suggestion
