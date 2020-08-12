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
This module contains the function to rank oversights according to
the order passed.

The suggestions will be displayed in the same order in the UI.
"""

def rank_oversights(suggestions, order):
    """
    This module sorts the the list of suggestions according
    to the order passed.

    Args:
        suggestions : list of dicts
            Each dict represents one oversight's suggestion
            Also, each dict should have a key 'oversight'

        order : list of enums.Oversights
            The order in which suggestions are to be ranked

    Returns:
        suggestions : list of dicts
            Sorted according to order
    """
    sorted_suggestions = []

    for oversight in order:
    	for suggestion in suggestions:
    		if oversight == suggestion['oversight']:
    			sorted_suggestions.append(suggestion)

    # To ensure that each of the oversight is listed in order
    assert(len(suggestions) == len(sorted_suggestions))

    return sorted_suggestions
