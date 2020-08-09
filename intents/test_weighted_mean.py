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

"""This module has some tests to test the weighted mean module.
Tables(.csv files) used are in the places in the
data/data_for_test_weighted_mean folder.
The query is mentiond in __doc__ of the function.
"""

import pandas
import weighted_mean

def test_1():
    """
    Query : Find mean of GDP weighted by population
    Dataset Used - hardcoded(values are artificial)
    Columns :
        Country, GDP, Population
    """
    table = pandas.DataFrame()
    table['Country'] = pandas.Series(['India', 'USA', 'Pakistan', 'China'])
    table['GDP'] = pandas.Series([1000, 3000, 100, 1500])
    # Population in billions
    table['Population'] = pandas.Series([1.34, 2.34, 10, 12.44])
    
    result_table, suggestions = weighted_mean.weighted_mean(table, 'GDP', 'Population')

    print(result_table)
    print(suggestions)

    expected_result_table = """   mean of GDP weighted by Population
0                         1072.741194"""

    assert(expected_result_table == result_table.to_string())
    
    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))


def test_2():
    """
    Query : Find mean of NA_Sales weighted by EU_Sales for each platform
    Dataset Used - https://www.kaggle.com/gregorut/videogamesales
    (The query does not makes much sense analytically)
    """
    table = pandas.read_csv('data/data_for_test_weighted_mean/vgsales.csv')
    
    result_table, suggestions = weighted_mean.weighted_mean(table, 'NA_Sales', 'EU_Sales',
                                                        dimensions=['Platform'])

    print(result_table)
    print(suggestions)

    expected_result_table = """   Platform  mean of NA_Sales weighted by EU_Sales
0      2600                               1.767898
1       3DO                                    NaN
2       3DS                               1.863717
3        DC                               0.979704
4        DS                               2.772966
5        GB                               6.555793
6       GBA                               1.246331
7        GC                               1.052674
8       GEN                               2.335670
9        GG                                    NaN
10      N64                               2.109861
11      NES                               8.463206
12       NG                                    NaN
13       PC                               0.494976
14     PCFX                                    NaN
15       PS                               1.181380
16      PS2                               1.144120
17      PS3                               1.387781
18      PS4                               1.305415
19      PSP                               0.557303
20      PSV                               0.215903
21      SAT                               0.263704
22      SCD                               1.000000
23     SNES                               4.625352
24     TG16                                    NaN
25       WS                                    NaN
26      Wii                               8.322429
27     WiiU                               1.080966
28     X360                               2.395338
29       XB                               0.825975
30     XOne                               1.222843"""

    assert(expected_result_table == result_table.to_string())
    
    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))

def test_3():
    """
    Query : For each state find average household_income weihted by
            members(number of members)
    Dataset used - Hardcoded
    Columns : state, household_income, members 
    """
    table = pandas.DataFrame()
    table['State'] = pandas.Series(['UP', 'MP', 'HP', 'UP', 'MP', 'HP'])
    table['household_income'] = pandas.Series([1000, 3000, 100, 1500, 3000, 100])
    # Number of members in the house
    table['members'] = pandas.Series([2, 3, 4, 2, 3, 5])


    result_table, suggestions = weighted_mean.weighted_mean(table, 'household_income',
                                                            'members',
                                                            dimensions=['State'])

    print(result_table.to_string())
    print(suggestions)

    expected_result_table = """  State  mean of household_income weighted by members
0    HP                                         100.0
1    MP                                        3000.0
2    UP                                        1250.0"""

    assert(expected_result_table == result_table.to_string())

    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))


print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print('Test cases completed')
