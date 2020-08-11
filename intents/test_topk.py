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
TODO - assert the suggestions
"""
import pandas
import topk
from util import enums
import data.spider_eval.evaluation

def test_1():
    """An example from the IPL dataset
    question : top-15 city based on win_by_runs in season = 2017
               in the date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = topk.topk(table, 'win_by_runs', ['city'], False, 40,
    	                        slices=[('season', enums.Filters.EQUAL_TO, 2017)],
    	                        date_range=('2008-05-08', '2017-04-12'),
    	                        date_column_name='date',
    	                        date_format='%Y-%m-%d')
    print(query_result)
    expected_result = """        city  win_by_runs
0       Pune           97
1  Hyderabad           35
2  Bangalore           15
3       Pune            0
4     Rajkot            0
5     Indore            0
6  Hyderabad            0
7     Mumbai            0
8     Indore            0
9     Mumbai            0"""
    expected_suggestions = """[{'suggestion': 'The results has duplicates', 'oversight_name': 'Duplicates in top-k'}, {'suggestion': 'Instead of 40 only 10 rows are present in the results', 'oversight_name': 'TopK when less than k present'}]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_2():
    """An example from the IPL dataset
    question : top 5 player_of_match based on avg(win_by_runs)
               in season 2017 in date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = topk.topk(table, 'win_by_runs', ['player_of_match'], False,
    	                        5, slices=[('season', enums.Filters.EQUAL_TO, 2017)],
    	                        date_range=('2017-05-09', '2017-05-12'),
    	                        date_column_name='date',
                                date_format='%Y-%m-%d',
    	                        summary_operator=enums.SummaryOperators.MEAN)
    print(query_result)
    expected_result = """  player_of_match  MEAN of win_by_runs
0       MM Sharma                   14
1         KK Nair                    7
2         WP Saha                    7
3         SS Iyer                    0"""
    expected_suggestions = """[{'oversight_name': 'Regression to the mean', 'suggestion': "very few of the top-k in the given date range will be in the previous window's top-k"}, {'suggestion': 'Instead of 5 only 4 rows are present in the results', 'oversight_name': 'TopK when less than k present'}]"""

    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_3():
    """An example from the spider dataset
    question : In which year were most departments established?
    """
    table = data.spider_eval.evaluation.get_table('department_management',
    	                                             'department')
    query_result = topk.topk(table, 'Department_ID', ['Creation'], False, 1,
    	                        slices=None,
                                date_range=None,
    	                        date_column_name='date',
                                date_format='%Y-%m-%d',
    	                        summary_operator=enums.SummaryOperators.COUNT)
    print(query_result)
    expected_result = """  Creation  COUNT of Department_ID
0     1789                       2"""
    expected_suggestions = """[{'change_list': {'topKLimit': 14}, 'suggestion': 'The rows NOT in the top-k have a much larger sum over Department_ID than the rows in top-k', 'confidence_score': 0.15384615384615385}]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_4():
    """An example from the spider dataset
    question : What are the themes of farm competitions sorted by year in
               ascending order?
    """
    table = data.spider_eval.evaluation.get_table('farm', 'farm_competition')
    query_result = topk.topk(table, 'Year', ['Theme'], True, -1, slices=None,
    	                        date_range=None,
                                date_column_name='date',
    	                        date_format='%Y-%m-%d',
                                group_columns=None,
    	                        summary_operator=None)
    print(query_result)
    expected_result = """   Year                Theme
0  2002               Aliens
1  2003             MTV Cube
2  2004      Valentine's Day
3  2005         MTV Asia Aid
4  2006          Codehunters
5  2013  Carnival M is back!"""
    expected_suggestions = """[]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_5():
    """An example from the spider dataset
    question : For each city list their names in decreasing order by their
               highest station latitude.
    """
    table = data.spider_eval.evaluation.get_table('bike_1', 'station')
    query_result = topk.topk(table, 'lat', ['city'], False, -1, slices=None,
    	                        date_range=None, date_column_name='date',
    	                        date_format='%Y-%m-%d',
    	                        summary_operator=enums.SummaryOperators.MAX)
    print(query_result)
    expected_result = """            city  MAX of lat
0  San Francisco   37.804770
1   Redwood City   37.491269
2      Palo Alto   37.448598
3  Mountain View   37.406940
4       San Jose   37.352601"""
    expected_suggestions = """[]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_6():
    """An example from the spider dataset
    question : What are the dates of publications in descending order of price?
    """
    table = data.spider_eval.evaluation.get_table('book_2', 'publication')
    query_result = topk.topk(table, 'Price', ['Publication_Date'], False, -1,
    	                        slices=None,
                                date_range=None,
    	                        date_column_name='date',
                                date_format='%Y-%m-%d')
    print(query_result)
    expected_result = """  Publication_Date       Price
0      August 2008  15000000.0
1       March 2008   6000000.0
2        June 2006   4100000.0
3     October 2005   3000000.0
4      August 2008   3000000.0
5       March 2007   2000000.0
6       April 2007   2000000.0"""
    expected_suggestions = """[{'suggestion': 'The results has duplicates', 'oversight_name': 'Duplicates in top-k'}]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_7():
    """An example from the spider dataset
    question : What is the name and salary of all employees in order of salary?
    """
    table = data.spider_eval.evaluation.get_table('flight_1', 'employee')
    query_result = topk.topk(table, 'salary', ['name'], True, -1, slices=None,
    	                        date_range=None,
                                date_column_name='date',
    	                        date_format='%Y-%m-%d')
    print(query_result)
    expected_result = """                name  salary
0        Milo Brooks      20
1        Donald King   18050
2    Richard Jackson   23980
3     Patricia Jones   24450
4        Linda Davis   27984
5   Elizabeth Taylor   32021
6      Haywood Kelly   32899
7       Chad Stewart   33546
8     David Anderson   43001
9     Barbara Wilson   43723
10      Robert Brown   44740
11    Michael Miller   48090
12     William Moore   48250
13   Jennifer Thomas   54921
14      William Ward   84476
15    Michael Miller   99890
16        Larry West  101745
17     William Jones  105743
18       Eric Cooper  114323
19       James Smith  120433
20      Dorthy Lewis  152013
21     John Williams  153972
22      Mary Johnson  178345
23       Karen Scott  205187
24        Mark Young  205187
25   Lawrence Sperry  212156
26   Angela Martinez  212156
27   Joseph Thompson  212156
28       Betty Adams  227489
29       Lisa Walker  256481
30     George Wright  289950"""
    expected_suggestions = """[{'suggestion': 'The results has duplicates', 'oversight_name': 'Duplicates in top-k'}]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

def test_8():
    """This query uses a manually created dataset - to test similarity between
    rank vectors question : Top-4 rating between 23/05/2010 to 25/05/2011
    """
    # in this database the ranks reverse if the previous window is considered
    table = pandas.read_csv('data/rating.csv')
    query_result = topk.topk(table, 'Rating', ['User Name'], True, 4,
                             slices=None,
                             date_range=('23/05/2010', '25/05/2011'),
                             date_column_name='date',
                             date_format='%d/%m/%Y')
    print(query_result)
    expected_result = """  User Name  Rating
0      Benq    3400
1     300iq    4300
2       cba    5200
3   tourist    6100"""
    expected_suggestions = """[{'oversight_name': 'Regression to the mean', 'suggestion': "The ranks of the top-k in the date range differs much from the previous window's top-k"}]"""
    assert(expected_result == query_result[0].to_string())
    assert(expected_suggestions == str(query_result[1]))

print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print(test_4.__doc__)
test_4()

print(test_5.__doc__)
test_5()

print(test_6.__doc__)
test_6()

print(test_7.__doc__)
test_7()

print(test_8.__doc__)
test_8()

print("Test cases completed")
