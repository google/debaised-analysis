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
# Runs all the tests & exits if any of the test fails
# Whenever a new test_file.py is added it should be added here

err() {
  echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

if ! python3 test_topk.py; then
  err "test_topk failed"
  exit 1
fi

if ! python3 test_trend.py; then
  err "test_trend failed"
  exit 1
fi

if ! python3 test_show.py; then
  err "test_show failed"
  exit 1
fi

if ! python3 test_slice_compare.py; then
  err "test_slice_compare failed"
  exit 1
fi

if ! python3 util/test_aspects.py; then
  err "util/test_aspects failed"
  exit 1
fi

if ! python3 oversights/test_mean_vs_median.py; then
  err "oversights/test_mean_vs_median failed"
  exit 1
fi

if ! python3 oversights/test_simpson_paradox.py; then
  err "oversights/test_simpson_paradox failed"
  exit 1
fi

echo 'All tests completed'
