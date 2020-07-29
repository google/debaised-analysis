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
This module will help in calling the main.py locally and debugging
if any error occurs.
This module has a RequestClass that mimics the flask.Request class.
(The argument that hello_world(Cloud endpoint that gets called by UI)
 takes is a flask.Request object containing the json sent.
)
Implementation-
    Then Creates an object of the RequestClass
    Reads the json object as a str from the obj.json file.
    Passes the json object to the hello_http function in the main.py
    Gets the date columns dictionary from the main.py module
    Prints all the date columns & also their type
Steps to Use:
    Copy the json object from the chrome console
    Pase the json object in /date_detection/obj.json
    Run the debug.py from /date_detection - python3 debug.py
"""
from main import hello_world
import pandas
import json

class RequestClass:
    """This class mimics the flask class, it has the get_json function
    that loads the json from the json file.
    Its object is passed to the hello_http in main.py.
    """
    args = None
    json_obj = ''
    def get_json(param, **kwargs):
        """
        Returns:
            The json object of the str in obj.json
        """
        silent = kwargs.get('silent', None)
        json_file = open("obj.json", "r")
        json_obj = json.loads(json_file.readline())
        return json_obj

obj = RequestClass()

result = hello_world(obj)

print(result)
