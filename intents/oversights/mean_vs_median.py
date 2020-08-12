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

Mean vs Median is the oversight which arises whenever there is 
huge difference between the mean value and the median value of data.
If the summary_operator being used is mean on a data in which mean
differs a lot from median , the oversight suggestion is passed.
Here we use the SKEW function (also available as an inbuilt function in Google 
Sheets) as the parameter to detect the difference between mean and median.
"""
import sys
sys.path.append(".")

 
# for calculation standard deviation i.e pstdev() and mean i.e mean()
import statistics 

from util import constants, enums
 
def mean_vs_median(values):
    """ This function gives suggestion if the mean_vs_median oversight
	is detected when summary_operator 'mean' is used.
	It checks the difference between the mean and median using the
	standard Skew function which can be interpreted as the normalized
	difference between mean and median. If this parameter has a large 
	absolute value then it returns the debiasing suggestion.

    The cut-off is fixed in the util/constants module

    Args:
    	values : Type-list of numbers could be floating points
    		It has the numbers for which the user finds the mean
    Returns:
        suggestion : dictonary with keys 'suggestion', 'oversight_name'
    """

    skew_value = _skew(values)

    if (skew_value >= constants.LOWER_BOUND_SIMILARITY_MEAN_VS_MEDIAN 
    	and skew_value <= constants.UPPER_BOUND_SIMILARITY_MEAN_VS_MEDIAN):
    		return None
    else:
    	suggestion = {}
    	suggestion['suggestion'] = 'Median is very different from the Mean'
    	suggestion['oversight'] = enums.Oversights.MEAN_VS_MEDIAN
    	return suggestion

def _skew(values):
	""" This function calculates the skew value of the list
	of values which represents the difference between the mean
	and median which also corresponds to the skewness.
	Using the following formula ,
	(1/((n-1)*(n-2)))*(sum over i { ((values[i]-mean(values))/(std_dev))**3) }
	n -> number of values
	std_dev -> standard deviation of all values
	For documentation of this function refer to SKEW function
	available in Google Sheets

    Args:
        values : Type-list of numbers could be floating points
    Returns:
        floating point number represeting the skew value of values
	"""

	std_dev = statistics.pstdev(values)
	mean = statistics.mean(values)

	size = len(values)

	# If there is no deviation we assume to not have any skewness
	if std_dev == 0:
		return 0

	# If there are <=2 entries we assume to not have any skewness
	if size <= 2:
		return 0

	# Summation of skewness of each element
	skew_value = 0
	for x in values:
		skew_of_x = (x - mean) / std_dev
		skew_of_x = (skew_of_x)**3
		skew_value += skew_of_x

	#Normalizing skewness with the size of data
	skew_value = (skew_value * size) / ((size - 1) * (size - 2))

	return skew_value



