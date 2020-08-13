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

"""This module has some examples of function calls for queries from IPL dataset.
The query is mentiond in __doc__ of the function.
"""
import pandas
import trend
from util.enums import *

def test_1():
    """An example from the IPL dataset
    question : annual trend of avg win_by_runs over date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = trend.trend(table, 'win_by_runs', Granularities.ANNUALLY,
                                  SummaryOperators.MAX,
                                  date_range=('2008-05-08', '2010-04-12'),
                                  date_column_name='date',
                                  date_format='%Y-%m-%d')
    print(query_result)

    expected_result = """         date  win_by_runs
0  2008-01-01          105
1  2009-01-01           92
2  2010-01-01           98"""
    expected_suggestions = "[]"

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

print(test_1.__doc__)
test_1()

print("Test cases completed")