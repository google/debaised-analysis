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

"""This module has some examples of function calls for queries
from IPL & spider dataset.
The query is mentiond in __doc__ of the function.
"""

# to run the tests that use spider_eval dataset, download it from here -
# https://yale-lily.github.io/spider
# and replace the evaluation.py file to this -
# https://drive.google.com/file/d/1QSydM2VX2q1ERrZvrBNSFiaf5A3aO93i/\
# view?ts=5ee202e5

import pandas

import topk
from util.enumerations import *

# import data.spider_eval.evaluation

def test_1():
    """An example from the IPL dataset
    question : top-15 city based on win_by_runs in season = 2017
               in the date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = topk.topk(table, 'win_by_runs', ['city'], False, 40,
    	                        slices={'season' : 2017},
    	                        date_range=('2008-05-08', '2017-04-12'),
    	                        date_column_name='date',
    	                        date_format='%Y-%m-%d')
    print(query_result)

def test_2():
    """An example from the IPL dataset
    question : top 5 player_of_match based on avg(win_by_runs)
               in season 2017 in date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = topk.topk(table, 'win_by_runs', ['player_of_match'], False,
    	                        5, slices={'season' : 2017},
    	                        date_range=('2017-05-09', '2017-05-12'),
    	                        date_column_name='date', date_format='%Y-%m-%d',
    	                        summary_operator=SummaryOperators.MEAN)
    print(query_result)

def test_3():
    """An example from the spider dataset
    question : In which year were most departments established?
    """
    table = data.spider_eval.evaluation.get_table('department_management',
    	                                             'department')
    query_result = topk.topk(table, 'Department_ID', ['Creation'], False, 1,
    	                        slices=None, date_range=None,
    	                        date_column_name='date', date_format='%Y-%m-%d',
    	                        summary_operator=SummaryOperators.COUNT)
    print(query_result)

def test_4():
    """An example from the spider dataset
    question : What are the themes of farm competitions sorted by year in
               ascending order?
    """
    table = data.spider_eval.evaluation.get_table('farm', 'farm_competition')
    query_result = topk.topk(table, 'Year', ['Theme'], True, 10000, slices=None,
    	                        date_range=None, date_column_name='date',
    	                        date_format='%Y-%m-%d', group_columns=None,
    	                        summary_operator=None)
    print(query_result)

def test_5():
    """An example from the spider dataset
    question : For each city list their names in decreasing order by their
               highest station latitude.
    """
    table = data.spider_eval.evaluation.get_table('bike_1', 'station')
    query_result = topk.topk(table, 'lat', ['city'], False, 10000, slices=None,
    	                        date_range=None, date_column_name='date',
    	                        date_format='%Y-%m-%d',
    	                        summary_operator=SummaryOperators.MAX)
    print(query_result)

def test_6():
    """An example from the spider dataset
    question : What are the dates of publications in descending order of price?
    """
    table = data.spider_eval.evaluation.get_table('book_2', 'publication')
    query_result = topk.topk(table, 'Price', ['Publication_Date'], False, 10000,
    	                        slices=None, date_range=None,
    	                        date_column_name='date', date_format='%Y-%m-%d')
    print(query_result)

def test_7():
    """An example from the spider dataset
    question : What is the name and salary of all employees in order of salary?
    """
    table = data.spider_eval.evaluation.get_table('flight_1', 'employee')
    query_result = topk.topk(table, 'salary', ['name'], True, 1000, slices=None,
    	                        date_range=None, date_column_name='date',
    	                        date_format='%Y-%m-%d')
    print(query_result)

print(test_1.__doc__)
test_1()

print("Test cases completed")
