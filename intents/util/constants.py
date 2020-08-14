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
This module stores various constants that affect behavior of
intents / oversights
These may be changed to decrease the number of false positives.
"""

# cut-off of set intersection method in regression to the mean
RTM_SET_INTERSECTION_CUT_OFF = .7

# threshold of similarity in ranks method in regression to the mean
RTM_RANK_VECTOR_SIMILARITY_THRESHOLD = 30

# range of similarity between mean and median in skew method
LOWER_BOUND_SIMILARITY_MEAN_VS_MEDIAN = -2.5
UPPER_BOUND_SIMILARITY_MEAN_VS_MEDIAN = 2.5

# Cut-off of looking at the tails 
LOOKING_AT_THE_TAILS_FLOAT_THRESHOLD = .7 
# type is angle, as cosine similarity is used
LOOKING_AT_THE_TAILS_STRING_THRESHOLD = 20

# Threshold of abs(similarity) between any row and the kth row in
# more than just topk ddetection
# This is a very tight threshold to prevent same suggestion coming each time
MORE_THAN_JUST_TOPK_THRESHOLD = 0.001

# threshold value of simpson's-paradox.
SIMPSONS_PARADOX_DOMINANT_PERCENT_THRESHOLD = 75

# threshold of disimilarity of two values in benchmark set too different.
BSTD_DISIMILARITY_THRESHOLD = 0.20

# top-down error similarity threshold value
TOP_DOWN_ERROR_SIMILARITY_THRESHOLD = 0.05

# top-down error dissimilarity threshold value
TOP_DOWN_ERROR_DISSIMILARITY_THRESHOLD = 0.30

# Threshold of ratio between sum of top-k & sum of others
TOPK_VS_OTHERS_THRESHOLD = .7

# calendar vs experience in time series  threshold value
CALENDAR_VS_EXPERIENCE_TIME_THRESHOLD = .8

# Threshold of wrong points oversight
WRONG_POINTS_THRESHOLD = .45
