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
This module contains for each intent the order in which the oversight's
suggestions are to be displayed.

Oversights are ranked because in some intents multiple oversights
occur in a single query. Multiple oversights are shown to the user
one at a time. 

The basic principle used while deciding the particular orders -
usefulness of the suggestion to the user.
"""

from util import enums

ORDER_IN_TOPK = [enums.Oversights.DUPLICATES_IN_TOPK,
                 enums.Oversights.TOPK_WHEN_LESS_THAN_K_PRESENT,
                 enums.Oversights.MEAN_VS_MEDIAN,
                 enums.Oversights.MORE_THAN_JUST_TOPK,
                 enums.Oversights.REGRESSION_TO_THE_MEAN,
                 enums.Oversights.LOOKING_AT_TAILS_TO_FIND_CAUSES,
                 enums.Oversights.TOPK_VS_OTHERS,
                 enums.Oversights.ATTRIBUTION_WITH_HIDDEN_NEGATIVES
                ]

ORDER_IN_SHOW = [enums.Oversights.MEAN_VS_MEDIAN,
                 enums.Oversights.ATTRIBUTION_WITH_HIDDEN_NEGATIVES
                ]

ORDER_IN_SLICE_COMPARE = [enums.Oversights.MEAN_VS_MEDIAN,
                          enums.Oversights.TOP_DOWN_ERROR,
                          enums.Oversights.SIMPSONS_PARADOX,
                          enums.Oversights.BENCHMARK_SET_TOO_DIFFERENT
                         ]

ORDER_IN_TIME_COMPARE = [enums.Oversights.MEAN_VS_MEDIAN,
                         enums.Oversights.TOP_DOWN_ERROR,
                         enums.Oversights.SIMPSONS_PARADOX,
                        ]

ORDER_IN_TREND = [enums.Oversights.MEAN_VS_MEDIAN]

# There is no oversight related to correlation intent
# On hold oversight : Anscombe Quartet error
ORDER_IN_CORRELATION = []

# There is no oversight related to weighted mean intent
ORDER_IN_WEIGHTED_MEAN = []
