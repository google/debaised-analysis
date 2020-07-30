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

if ! python3 test_date_detection.py;
then
  # if this test fails echos the error and also stores in an array
  err "test_date_detection failed"
  list_logs+=("test_date_detection failed")
else
  # if this does not fails then just stores in the array
  list_logs+=("test_date_detection passed")
fi

if ! python3 util/test_min_max_date.py;
then
  err "util/test_min_max_date failed"
  list_logs+=("util/test_min_max_date failed")
else
  list_logs+=("util/test_min_max_date passed")
fi

echo 'All tests completed '
echo 'Results -'

list_logs_length=${#list_logs[@]}

# Displaying all the results at the end
for ((i=0;i<list_logs_length;i++)); do
    echo "${list_logs[i]}"
done
