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

"""This module detects the cases of mean_vs_median whenever 
user uses the summary_operator as mean.
This module detects the cases of attribution with hidden negative
whenever user uses the summary_operator as proportion

Attribution with Hidden Negative is the oversight which arises whenever
there is a negative value present among the values on which proportion is
being applied. Therefore, if the summary_operator is proportion of <sum/count> 
and the values contains a negative value , the oversight is passed.

"""

def attribution_with_hidden_negative(values):
	""" This function gives suggestion if the attribution_with_hidden_negative
	oversight is detected when summary_operator is 'proportion of <sum/count>'  
	
	It checks if a negative value exists in values.

	Args:
		values: Type - anything that can be iterated over
    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name'
	"""

	negative_exists = False

	for value in values :
		if ( type(value) == int or type(value) == float ) and value < 0 :
			negative_exists = True

	if negative_exists :
		suggestion = {}
		suggestion['suggestion'] = 'There exists negative values among the values on which proportion is being applied'
		suggestion['oversight_name'] = 'Attribution to Hidden Negative'
		suggestion['is_row_level_suggestion'] = True
		suggestion['confidence_score'] = 1

		return suggestion
	else :
		return None