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
from IPL matches.csv
The query is mentiond in __doc__ of the function.
"""

import pandas

import show
from util.enums import *


def test_1():
    """An example from the IPL dataset 
    question : show all cities in season 2017 in the
                date range 2008-05-08 to 2017-04-12
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                dimensions=['city'],
                                slices=[('season', Filters.EQUAL_TO, 2017)],
                                date_range=('2008-05-08', '2017-04-12'),
                                date_column_name='date',
                                date_format='%Y-%m-%d')


    print(query_result);
    expected_result = """        city
0  Hyderabad
1       Pune
2     Rajkot
3     Indore
4  Bangalore
5  Hyderabad
6     Mumbai
7     Indore
8       Pune
9     Mumbai"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))



def test_2():
    """An example from the IPL dataset
    question :show player_of_match along with their average of win_by_runs
              in season 2017 in date range '2017-05-09' to '2017-05-12'
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                dimensions=['player_of_match'],
                                metric='win_by_runs' ,
                                slices=[('season', Filters.EQUAL_TO, 2017)],
                                date_range=('2017-05-09', '2017-05-12'),
                                date_column_name='date', date_format='%Y-%m-%d',
                                summary_operator=SummaryOperators.MEAN)
    print(query_result)
    expected_result = """  player_of_match  win_by_runs
0         KK Nair            7
1       MM Sharma           14
2         SS Iyer            0
3         WP Saha            7"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))


def test_3():
    """An example from the IPL dataset
    question :show all the distinct seasons available in IPL dataset
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                dimensions=['season'],
                                summary_operator=SummaryOperators.DISTINCT)
    print(query_result)
    expected_result = """   season
0    2008
1    2009
2    2010
3    2011
4    2012
5    2013
6    2014
7    2015
8    2016
9    2017"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))


def test_4():
    """An example from the IPL dataset
    question :show all matches where Royal Challengers Bangalore won the match in season 2008
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                slices=[('season', Filters.EQUAL_TO, 2008), ('winner', Filters.EQUAL_TO, 'Royal Challengers Bangalore')],
                                dimensions = ['team1','team2'],)
    print(query_result)
    expected_result = """                         team1                        team2
0               Mumbai Indians  Royal Challengers Bangalore
1              Deccan Chargers  Royal Challengers Bangalore
2  Royal Challengers Bangalore          Chennai Super Kings
3  Royal Challengers Bangalore              Deccan Chargers"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))
    

def test_5():
    """An example from the IPL dataset
    question :show all the umpire1 of season 2017 in date range '2017-05-09'to '2017-05-12'
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                dimensions=['umpire1'],
                                slices=[('season', Filters.EQUAL_TO, 2017)],
                                date_range=('2017-05-09', '2017-05-12'),
                                date_column_name='date', date_format='%Y-%m-%d',
                                summary_operator=SummaryOperators.DISTINCT)
    print(query_result)
    expected_result = """                 umpire1
0             A Deshmukh
1         A Nand Kishore
2  KN Ananthapadmanabhan
3               YC Barde"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))
    

def test_6():
    """An example from the IPL dataset
    question :show the toss_winners of season 2017
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                dimensions=['toss_winner'],
                                slices=[('season', Filters.EQUAL_TO, 2017)],)
    print(query_result)
    expected_result = """                    toss_winner
0   Royal Challengers Bangalore
1        Rising Pune Supergiant
2         Kolkata Knight Riders
3               Kings XI Punjab
4   Royal Challengers Bangalore
5           Sunrisers Hyderabad
6                Mumbai Indians
7   Royal Challengers Bangalore
8        Rising Pune Supergiant
9                Mumbai Indians
10        Kolkata Knight Riders
11               Mumbai Indians
12                Gujarat Lions
13          Sunrisers Hyderabad
14             Delhi Daredevils
15               Mumbai Indians
16  Royal Challengers Bangalore
17             Delhi Daredevils
18              Kings XI Punjab
19                Gujarat Lions
20          Sunrisers Hyderabad
21               Mumbai Indians
22                Gujarat Lions
23             Delhi Daredevils
24       Rising Pune Supergiant
25                Gujarat Lions
26  Royal Challengers Bangalore
27               Mumbai Indians
28        Kolkata Knight Riders
29                Gujarat Lions
30        Kolkata Knight Riders
31              Kings XI Punjab
32  Royal Challengers Bangalore
33                Gujarat Lions
34              Kings XI Punjab
35        Kolkata Knight Riders
36  Royal Challengers Bangalore
37       Rising Pune Supergiant
38             Delhi Daredevils
39       Rising Pune Supergiant
40             Delhi Daredevils
41  Royal Challengers Bangalore
42          Sunrisers Hyderabad
43             Delhi Daredevils
44        Kolkata Knight Riders
45                Gujarat Lions
46               Mumbai Indians
47        Kolkata Knight Riders
48             Delhi Daredevils
49               Mumbai Indians
50             Delhi Daredevils
51          Sunrisers Hyderabad
52        Kolkata Knight Riders
53       Rising Pune Supergiant
54  Royal Challengers Bangalore
55               Mumbai Indians
56        Kolkata Knight Riders
57               Mumbai Indians
58               Mumbai Indians"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))



def test_7():
    """An example from the IPL dataset
    question :show sum of win_by_runs
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                metric='win_by_runs' ,
                                date_column_name='date', date_format='%Y-%m-%d',
                                summary_operator=SummaryOperators.SUM)
    print(query_result)
    expected_result = """  Summary Operator  win_by_runs
0              SUM         8702"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
    assert(expected_suggestions == str(query_result[1]))

    

def test_8():
    """An example from the IPL dataset
    question :show mean of win_by_runs
              in season 2017 in date range '2017-05-09' to '2017-05-12'
    """
    table = pandas.read_csv('data/matches.csv')
    query_result = show.show(table,
                                metric='win_by_runs' ,
                                slices=[('season', Filters.EQUAL_TO, 2017)],
                                date_range=('2017-05-09', '2017-05-12'),
                                date_column_name='date', date_format='%Y-%m-%d',
                                summary_operator=SummaryOperators.MEAN)
    print(query_result)
    expected_result = """  Summary Operator  win_by_runs
0             MEAN            7"""
    assert(expected_result == query_result[0].to_string())
    expected_suggestions = "[]"
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