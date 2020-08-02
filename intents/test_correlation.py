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

"""This module has some tests to test the correlation module.
Tables(.csv files) used are in the places in the
data/data_for_test_correlation folder.
The query is mentiond in __doc__ of the function.
"""

import pandas
import correlation

def test_1():
    """
    Query : Find correlation between NA_Sales & EU_Sales
    Dataset Used - https://www.kaggle.com/gregorut/videogamesales
    Columns :
        Platform - Platform of the games release (i.e. PC,PS4, etc.)
        NA_Sales - Sales in North America (in millions)
        EU_Sales - Sales in Europe (in millions)
    """
    table = pandas.read_csv('data/data_for_test_correlation/vgsales.csv')
    
    result_table, suggestions = correlation.correlation(table, 'NA_Sales', 'EU_Sales')

    print(result_table)
    print(suggestions)

    expected_result_table = """   correlation between "NA_Sales" , "EU_Sales"
0                                     0.767727"""

    assert(expected_result_table == result_table.to_string())
    
    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))


def test_2():
    """
    Query : Find correlation between NA_Sales & EU_Sales for each platform
    Dataset Used - https://www.kaggle.com/gregorut/videogamesales
    Columns :
        Platform - Platform of the games release (i.e. PC,PS4, etc.)
        NA_Sales - Sales in North America (in millions)
        EU_Sales - Sales in Europe (in millions)
    """
    table = pandas.read_csv('data/data_for_test_correlation/vgsales.csv')
    
    result_table, suggestions = correlation.correlation(table, 'NA_Sales', 'EU_Sales',
                                                        dimensions=['Platform'])

    print(result_table)
    print(suggestions)

    expected_result_table = """   Platform  correlation between "NA_Sales" , "EU_Sales"
0      2600                                     0.996554
1       3DO                                          NaN
2       3DS                                     0.945838
3        DC                                     0.797678
4        DS                                     0.871312
5        GB                                     0.705745
6       GBA                                     0.925557
7        GC                                     0.938478
8       GEN                                     0.973297
9        GG                                          NaN
10      N64                                     0.919057
11      NES                                     0.735203
12       NG                                          NaN
13       PC                                     0.404835
14     PCFX                                          NaN
15       PS                                     0.811515
16      PS2                                     0.654672
17      PS3                                     0.813370
18      PS4                                     0.793474
19      PSP                                     0.701001
20      PSV                                     0.755251
21      SAT                                     0.999610
22      SCD                                     1.000000
23     SNES                                     0.988964
24     TG16                                          NaN
25       WS                                          NaN
26      Wii                                     0.971428
27     WiiU                                     0.959718
28     X360                                     0.854582
29       XB                                     0.831869
30     XOne                                     0.779913"""

    assert(expected_result_table == result_table.to_string())
    
    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))

def test_3():
    """
    Query : Find correlation between math score and reading score
    Dataset used - https://www.kaggle.com/spscientist/students-performance-in-exams
    Columns : race/ethnicity, math score, reading score 
    """
    table = pandas.read_csv('data/data_for_test_correlation/students_performance.csv')

    result_table, suggestions = correlation.correlation(table, 'math score', 'reading score')

    print(result_table.to_string())
    print(suggestions)

    expected_result_table = """   correlation between "math score" , "reading score"
0                                            0.81758 """

    assert(expected_result_table == result_table.to_string())

    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))

def test_4():
    """
    Query : Find correlation between math score and reading score for each race/ethnicity
    Dataset used - https://www.kaggle.com/spscientist/students-performance-in-exams
    Columns : race/ethnicity, math score, reading score 
    """
    table = pandas.read_csv('data/data_for_test_correlation/students_performance.csv')

    result_table, suggestions = correlation.correlation(table, 'math score', 'reading score',
    	                                                dimensions=['race/ethnicity'])

    print(result_table.to_string())
    print(suggestions)

    expected_result_table = """  race/ethnicity  correlation between "math score" , "reading score"
0        group A                                           0.816310 
1        group B                                           0.824536 
2        group C                                           0.810855 
3        group D                                           0.793180 
4        group E                                           0.859600 """

    assert(expected_result_table == result_table.to_string())

    expected_suggestions = """[]"""

    assert(expected_suggestions == str(suggestions))


print(test_1.__doc__)
test_1()

print(test_2.__doc__)
test_2()

print(test_3.__doc__)
test_3()

print(test_4.__doc__)
test_4()
