# Copyright 2020 Google LLC

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# https://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/bin/bash
#
# Runs all the tests & stores the results in the array - list_logs
# Displays all the results at the end
# Whenever a new test_file.py is added it should be added here

# function to show errors
err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

# empty array initialized
list_logs=()

if ! python3 test_topk.py;
then
  # if this test fails echos the error and also stores in an array
  err "test_topk failed"
  list_logs+=("test_topk failed")
else
  # if this does not fails then just stores in the array
  list_logs+=("test_topk passed")
fi

if ! python3 test_correlation.py;
then
  # if this test fails echos the error and also stores in an array
  err "test_correlation failed"
  list_logs+=("test_correlation failed")
else
  # if this does not fails then just stores in the array
  list_logs+=("test_correlation passed")
fi

if ! python3 test_trend.py;
then
  err "test_trend failed"
  list_logs+=("test_trend failed")
else
  list_logs+=("test_trend passed")
fi


if ! python3 test_weighted_mean.py;
then
  err "test_weighted_mean failed"
  list_logs+=("test_weighted_mean failed")
else
  list_logs+=("test_weighted_mean passed")
fi

if ! python3 test_show.py;
then
  err "test_show failed"
  list_logs+=("test_show failed")
else
  list_logs+=("test_show passed")
fi

if ! python3 test_slice_compare.py;
then
  err "test_slice_compare failed"
  list_logs+=("test_slice_compare failed")
else
  list_logs+=("test_slice_compare passed")
fi

if ! python3 test_time_compare.py;
then
  err "test_time_compare failed"
  list_logs+=("test_time_compare failed")
else
  list_logs+=("test_time_compare passed")
fi

if ! python3 util/test_aspects.py;
then
  err "util/test_aspects failed"
  list_logs+=("util/test_aspects failed")
else
  list_logs+=("util/test_aspects passed")
fi

if ! python3 util/test_insert_as_column.py;
then
  err "util/test_insert_as_column failed"
  list_logs+=("util/test_insert_as_column failed")
else
  list_logs+=("util/test_insert_as_column passed")
fi


if ! python3 util/test_rank_oversights.py;
then
  err "util/test_rank_oversights failed"
  list_logs+=("util/test_rank_oversights failed")
else
  list_logs+=("util/test_rank_oversights passed")
fi

if ! python3 oversights/test_mean_vs_median.py;
then
  err "oversights/test_mean_vs_median failed"
  list_logs+=("oversights/test_mean_vs_median failed")
else
  list_logs+=("oversights/test_mean_vs_median passed")
fi

if ! python3 oversights/test_topk_vs_others.py;
then
  err "oversights/test_topk_vs_others failed"
  list_logs+=("oversights/test_topk_vs_others failed")
else
  list_logs+=("oversights/test_topk_vs_others passed")
fi

if ! python3 oversights/test_more_than_just_topk.py;
then
  err "oversights/test_more_than_just_topk failed"
  list_logs+=("oversights/test_more_than_just_topk failed")
else
  list_logs+=("oversights/test_more_than_just_topk passed")
fi

if ! python3 oversights/test_simpsons_paradox.py;
then
  err "oversights/test_simpsons_paradox failed"
  list_logs+=("oversights/test_simpsons_paradox failed")
else
  list_logs+=("oversights/test_simpsons_paradox passed")
fi

if ! python3 oversights/test_top_down_error.py;
then
  err "oversights/test_top_down_error failed"
  list_logs+=("oversights/test_top_down_error failed")
else
  list_logs+=("oversights/test_top_down_error passed")
fi

if ! python3 oversights/test_looking_at_tails.py;
then
  err "oversights/test_looking_at_tails failed"
  list_logs+=("oversights/test_looking_at_tails failed")
else
  list_logs+=("oversights/test_looking_at_tails passed")
fi

if ! python3 oversights/test_wrong_points.py;
then
  err "oversights/test_wrong_points failed"
  list_logs+=("oversights/test_wrong_points failed")
else
  list_logs+=("oversights/test_wrong_points passed")
fi

if ! python3 oversights/test_benchmark_set_too_different.py;
then
  err "oversights/test_benchmark_set_too_different failed"
  list_logs+=("oversights/test_benchmark_set_too_different failed")
else
  list_logs+=("oversights/test_benchmark_set_too_different passed")
fi

if ! python3 oversights/test_topk_when_less_than_k_present.py;
then
  err "oversights/test_topk_when_less_than_k_present failed"
  list_logs+=("oversights/test_topk_when_less_than_k_present failed")
else
  list_logs+=("oversights/test_topk_when_less_than_k_present passed")
fi

if ! python3 oversights/test_calendar_vs_experience_time.py;
then
  err "oversights/test_calendar_vs_experience_time failed"
  list_logs+=("oversights/test_calendar_vs_experience_time failed")
else
  list_logs+=("oversights/test_calendar_vs_experience_time passed")
fi

if ! python3 oversights/test_weighted_mean_with_different_weights.py;
then
  err "oversights/test_weighted_mean_with_different_weights failed"
  list_logs+=("oversights/test_weighted_mean_with_different_weights failed")
else
  list_logs+=("oversights/test_weighted_mean_with_different_weights passed")
fi

if ! python3 oversights/test_attribution_with_hidden_negative.py;
then
  err "oversights/test_attribution_with_hidden_negative failed"
  list_logs+=("oversights/test_attribution_with_hidden_negative failed")
else
  list_logs+=("oversights/test_attribution_with_hidden_negative passed")
fi

echo 'All tests completed '
echo 'Results -'


list_logs_length=${#list_logs[@]}

# Displaying all the results at the end
for ((i=0;i<list_logs_length;i++)); do
    echo "${list_logs[i]}"
done
