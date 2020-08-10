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
This module contains the tests for looking_at_tails.py
"""

from attribution_with_hidden_negative import attribution_with_hidden_negative

def test_1():
	"""
	Situation : All numbers being positive
	"""
	test_file = open("data/data_for_test_attribution_with_hidden_negative/test_1.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))
	
	suggestion = attribution_with_hidden_negative(values)
	print(suggestion)
	expected_suggestion = "None"

	assert(str(suggestion) == expected_suggestion)

def test_2():
	"""
	Situation : Some numbers are negative
	"""
	test_file = open("data/data_for_test_attribution_with_hidden_negative/test_2.txt", "r")
	values = test_file.read().split("\n")
	values = list(map(int, values))

	suggestion = attribution_with_hidden_negative(values)
	print(suggestion)
	expected_suggestion = """{'suggestion': 'There exists negative values among the values on which proportion is being applied', 'oversight_name': 'Attribution to Hidden Negative', 'is_row_level_suggestion': True, 'confidence_score': 1}"""

	assert(str(suggestion) == expected_suggestion)


print(test_1.__doc__)
test_1()
print(test_2.__doc__)
test_2()

print('Test cases completed')