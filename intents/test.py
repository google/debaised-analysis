"""This module has some examples of function calls for queries from IPL & spider dataset"""

import pandas

import intents

# to extract tables from the spider database
## made some changes to the evaluation module to return table as pandas dataframe
import spider_eval.evaluation


# # # # An example from the IPL dataset

# loading a csv file in data-frame
table = pandas.read_csv('matches.csv')

# example of trend query
# question : trend of avg win_by_runs over date range 2008-05-08 to 2017-04-12


# print(table)

query_result = intents.trend(table, 'win_by_runs', ('2008-05-08', '2010-04-12'), 'date', '%Y-%m-%d', 'annually', 'max')

print(query_result)

exit()


#example call to top-k for the query -
# 	top-15 city based on win_by_runs in season = 2017 in the date range 2008-05-08 to 2017-04-12

print(table.head())
print("question  - ", "top-15 city based on win_by_runs in season = 2017 in the date range 2008-05-08 to 2017-04-12")

query_result = intents.top_k(table, 'win_by_runs', 'city', False, 40, slices={'season' : 2017}, date_range=('2008-05-08', '2017-04-12'), date_column_name='date', date_format='%Y-%m-%d')

print(query_result)



#example call to top-k for the query -
# 	top 5 player_of_match based on avg(win_by_runs) in season 2017 in date range 2008-05-08 to 2017-04-12

print("question  -", "top 5 player_of_match based on avg(win_by_runs) in season 2017 in date range 2008-05-08 to 2017-04-12")

query_result = intents.top_k(table, 'win_by_runs', ['player_of_match'], False, 5, slices={'season' : 2017}, date_range=('2017-05-09', '2017-05-12'), date_column_name='date', date_format='%Y-%m-%d', summary_operator='average') 

print(query_result)




# # # : queries from the spider dataset



# # query : In which year were most departments established?

# spider_eval.evaluation.print_tables_in_db('department_management')

table = spider_eval.evaluation.get_table('department_management', 'department')

query_result = intents.top_k(table, 'Department_ID', ['Creation'], False, 1, slices=None, date_range=None, date_column_name='date', date_format='%Y-%m-%d', summary_operator='count') 

print("question - ", "In which year were most departments established?")
print(table.head())
print(query_result)




# query : What are the themes of farm competitions sorted by year in ascending order?

# spider_eval.evaluation.print_tables_in_db('farm')

table = spider_eval.evaluation.get_table('farm', 'farm_competition')

query_result = intents.top_k(table, 'Year', 'Theme', True, 10000, slices=None, date_range=None, date_column_name='date', date_format='%Y-%m-%d', group_columns=None, summary_operator=None) 

print("question - ", "What are the themes of farm competitions sorted by year in ascending order?")
print(table.head())
print(query_result)



# query : For each city list their names in decreasing order by their highest station latitude.

# spider_eval.evaluation.print_tables_in_db('bike_1')

table = spider_eval.evaluation.get_table('bike_1', 'station')

query_result = intents.top_k(table, 'lat', ['city'], False, 10000, slices=None, date_range=None, date_column_name='date', date_format='%Y-%m-%d', summary_operator='max') 

print("question - ", "For each city list their names in decreasing order by their highest station latitude.")
print(table.head())
print(query_result)



# query : What are the dates of publications in descending order of price?

# spider_eval.evaluation.print_tables_in_db('book_2')

table = spider_eval.evaluation.get_table('book_2', 'publication')

query_result = intents.top_k(table, 'Price', 'Publication_Date', False, 10000, slices=None, date_range=None, date_column_name='date', date_format='%Y-%m-%d') 

print("question - ", "What are the dates of publications in descending order of price?")
print(table.head())
print(query_result)




# query : What is the name and salary of all employees in order of salary?

# spider_eval.evaluation.print_tables_in_db('flight_1')

table = spider_eval.evaluation.get_table('flight_1', 'employee')

query_result = intents.top_k(table, 'salary', 'name', True, 10000, slices=None, date_range=None, date_column_name='date', date_format='%Y-%m-%d') 

print("question - ", "What is the name and salary of all employees in order of salary?")
print(table.head())
print(query_result)






