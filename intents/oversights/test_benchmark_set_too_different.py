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

import sys  
sys.path.append(".")

import pandas

import benchmark_set_too_different
from util.enums import SummaryOperators
from util.enums import Filters

def test_1():
    """
        question :  compare average hour work per day of A and rest all interns.
     """
    table = pandas.read_csv('data/intern_performance.csv')
    query_result = benchmark_set_too_different.benchmark_set_too_different(table, 'avg_hour_of_work',
                                                   ['avg_hour_of_work', 'lines_of_code'], 'intern_name', 
                                                   'A', SummaryOperators.MEAN)
    print(query_result)

    expected_result = "[{'suggestion': 'A looks different from others on avg_hour_of_work. You might also want to look at lines_of_code since A also looks different on this.', 'oversight_name': 'Benchmark set too different', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}]"

    assert(str(query_result) == expected_result)

def test_2():
    """
        question :  compare average revenue by country for A vs all
     """
    table = pandas.read_csv('data/revenue_list.csv')
    query_result = benchmark_set_too_different.benchmark_set_too_different(table, 'current_year_revenue',
                                                   ['current_year_revenue', 'last_year_revenue'], 'company_name', 
                                                   'A', SummaryOperators.MEAN, dimensions = ['country_name'])
    print(query_result)

    expected_result = "[{'suggestion': 'A looks different from others on current_year_revenue. You might also want to look at last_year_revenue since A also looks different on this.', 'oversight_name': 'Benchmark set too different', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}, {'row': 3, 'confidence_score': 100}, {'row': 4, 'confidence_score': 100}, {'row': 7, 'confidence_score': 100}, {'row': 8, 'confidence_score': 100}]}]"

    assert(str(query_result) == expected_result)

def test_3():
    """
        question :  compare average revenue for A vs all
     """
    table = pandas.read_csv('data/revenue_list.csv')
    query_result = benchmark_set_too_different.benchmark_set_too_different(table, 'current_year_revenue',
                                                   ['current_year_revenue', 'last_year_revenue'],
                                                   'company_name', 'A', SummaryOperators.MEAN)
    print(query_result)

    expected_result = "[{'suggestion': 'A looks different from others on current_year_revenue. You might also want to look at last_year_revenue since A also looks different on this.', 'oversight_name': 'Benchmark set too different', 'is_row_level_suggestion': True, 'row_list': [{'row': 1, 'confidence_score': 100}, {'row': 2, 'confidence_score': 100}]}]"

    assert(str(query_result) == expected_result)

print("\n\ncompare average hour work per day of A and rest all interns.\n")
test_1()

print("\n\ncompare average revenue by country for A vs all\n")
test_2()

print("\n\ncompare average revenue for A vs all\n")
test_3()

print("\nTest cases completed")