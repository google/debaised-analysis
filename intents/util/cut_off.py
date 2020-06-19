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
This module stores the cuttoff of different that are fixed while
execution of the code.
These may be changed to decrease the number of false positives.
"""
# cut-off of set intersection method in regression to the mean
RTM_SET_INTERSECTION = .7
# cut-off of similarity in ranks method in regression to the mean
RTM_RANK_VECTOR = 30
