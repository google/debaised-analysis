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
LOWER_BOUND_SIMILARITY_MEAN_VS_MEDIAN = -0.3
UPPER_BOUND_SIMILARITY_MEAN_VS_MEDIAN = 0.3

# Cut-off of looking at the tails 
LOOKING_AT_THE_TAILS_FLOAT_THRESHOLD = .7 
# type is angle, as cosine similarity is used
LOOKING_AT_THE_TAILS_STRING_THRESHOLD = 20
