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

from mean_vs_median import mean_vs_median
import statistics

def test_1():
	"""
	Situation : One of the entry of data contains a number with an extra 0 in it
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_1.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """{'suggestion': 'Median is very different from the Mean', 'oversight_name': 'Mean vs Median', 'is_row_level_suggestion': True, 'confidence_score': 5.315150951994627}"""

	assert(str(suggestion) == expected_suggestion)

def test_2():
	"""
	Situation : Values having some high peaks above the median and some low peaks
	below the median due to which mean balances to be around median
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_2.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = 'None'

	assert(str(suggestion) == expected_suggestion)

def test_3():
	"""
	Situation : A lot of initial values are very small values
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_3.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """None"""

	assert(str(suggestion) == expected_suggestion)	

def test_4():
	"""
	Situation : There are only 2 data points present
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_4.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = 'None'

	assert(str(suggestion) == expected_suggestion)		
    
def test_5():
	"""
	Situation : Symmetrical data which includes negative numbers also
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_5.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = 'None'

	assert(str(suggestion) == expected_suggestion)	

def test_6():
	"""
	Situation : Values having negative numbers which are large in absolute value
	The skewness in this situation should be negative
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_6.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """None"""

	assert(str(suggestion) == expected_suggestion)	

def test_7():
	"""
	Situation : Values containing a large number of 0s in between which impacts the
	mean value but not the median value
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_7.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """None"""

	assert(str(suggestion) == expected_suggestion)	

def test_8():
	"""
	Situation : Values represeting a exponential set of values
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_8.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """{'suggestion': 'Median is very different from the Mean', 'oversight_name': 'Mean vs Median', 'is_row_level_suggestion': True, 'confidence_score': 3.779277130195112}"""

	assert(str(suggestion) == expected_suggestion)	

def test_9():
	"""
	Situation : Clustering example of data , with first initial values having 
	low value and rest of the values being high
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_9.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = """None"""

	assert(str(suggestion) == expected_suggestion)		

def test_10():
	"""
	Situation : All values being 0 , this situation check if there is any zero
	division errors
	"""
	test_file = open("data/data_for_test_mean_vs_median/test_10.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = mean_vs_median(values)
	print(suggestion)
	print("Mean: " + str(statistics.mean(values)) + " Median: " + str(statistics.median(values)))
	expected_suggestion = 'None'

	assert(str(suggestion) == expected_suggestion)		

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

print(test_9.__doc__)
test_9()

print(test_10.__doc__)
test_10()