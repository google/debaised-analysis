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
	This module has some examples of function calls for queries from
	small part of innings dataset. The query is also mentioned.
"""

import pandas

import slice_compare
from util.enums import SummaryOperators

def test_1():
    """
    	An example from the IPL dataset
    	question :  compare total runs of 'Mumbai indians' and 
    				'Chennai Super Kings'.
     """
    table = pandas.read_csv('data/ipl_innings.csv')
    query_result = slice_compare.slice_compare(table, 'total_runs', ['batsman_team', 'season'], 
                dict({'batsman_team': ['Mumbai Indians', 'Chennai Super Kings']}),
                ['batsman_team', 'Mumbai Indians', 'Chennai Super Kings'],
                SummaryOperators.SUM)
    print(query_result)
print("compare total runs of 'Mumbai indians' and 'Chennai Super Kings'")
test_1()

print("Test cases completed")
