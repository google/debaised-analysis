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

"""This module will return the list for inserting columns of filter
and top-k

The functions use Sheets formula to form filters and top-k. Specifically
they make use of the QUERY formula that Sheets provide.
There are 2 types of columns that are inserts 
(1) Show column - This is the filter column which should have True if
                  the row passed the filters/slices and date range
(2) Top-k column - Row should have True if it is in the top-k values

"""

from util import aspects , enums

def insert_as_column_show(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, **kwargs):
    """
    This function is called by main.py to insert the show column
    It returns a list of strings , 1 for each row , representing the required
    sheets formula that needs to be inserted.

    0 indexing is followed
    
    Args : 
        table : Type-Pandas dataframe
            Contents of the sheets
        cheader_to_clabel : Type-Dictionary
            short for column_header_to_column_label , represents
            the corresponding column label which is given by sheets
            to the respective column headers
        row_start_label : Type-int
            sheet label(1-indexed) of the first row of table
            Note : This row_start_label doesn't contain the header row
                   it is specifically the starting row of the data
        row_end_label : Type-int
            sheet label(1-indexed) of the last row of table
        column_start_label : Type-str
            sheet label of the first column of table
        column_end_label : Type-str
            sheet label of the last column of table
        slices : Type-List of tuples
            Tuple represents the conditon to keep the row.
            (column_name, filter, value)
            column_name - is the value of the column that the
            condition is applied upon.
            filter - Filters enum members, ex. Filters.IN
            value - corresponding value required by the respective filter
        date_range: Type-tuple
            Tuple of start_date and end_date
        date_column_name: Type-str
            It is the name of column which contains date
        date_format: Type-str
            It is required by datetime.strp_time to parse the date in the format
            Format Codes
            https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior

    Returns :
        List of strings, list[i] denotes that ith row
        sheet formula
    """

    date_column_name = kwargs.get('date_column_name', 'date')
    date_range = kwargs.get('date_range', None)
    date_format = kwargs.get('date_format', '%Y-%m-%d')

    slices = kwargs.get('slices', None)

    list_of_formulas = []

    number_of_conditions = len(slices)

    for i in range(row_start_label, row_end_label + 1) :

        current_formula = '=NOT(ISNA(QUERY('

        # adding the row data range
        current_formula += str(column_start_label) + str(i) + ':' + str(column_end_label) + str(i)

        # adding comma before start of the SQL-like respective query
        current_formula += ', "'

        # starting the initial part of the SQL-like query
        current_formula += 'select ' + str(column_start_label) + ' where '

        condition_number = 0

        for condition in slices :
            # starting the condition in query with an open paranthesis
            current_formula += '('

            column_label_of_slice_condition = cheader_to_clabel[ condition[0] ]

            condition_value = condition[2]

            # if condition_value is a string , it will be enclosed by '' as Sheets needs to detect it as a string
            if isinstance(condition_value, str):
                condition_value = "'" + condition_value + "'" 

            if condition[1] == enums.Filters.EQUAL_TO :
                current_formula += (column_label_of_slice_condition) + "=" + str(condition_value)

            elif condition[1] == enums.Filters.NOT_EQUAL_TO :
                current_formula += (column_label_of_slice_condition) + "!=" + str(condition_value)
            
            elif condition[1] == enums.Filters.LESS_THAN :
                current_formula += (column_label_of_slice_condition) + "<" +  str(condition_value)
            
            elif condition[1] == enums.Filters.LESS_THAN_EQUAL_TO :
                current_formula += (column_label_of_slice_condition) + "<=" + str(condition_value)
            
            elif condition[1] == enums.Filters.GREATER_THAN :
                current_formula += (column_label_of_slice_condition) + ">" + str(condition_value)
            
            elif condition[1] == enums.Filters.GREATER_THAN_EQUAL_TO :
                current_formula += (column_label_of_slice_condition) + ">=" + str(condition_value) 
            
            elif condition[1] == enums.Filters.IN :

                number_of_values = len(condition_value)
                value_number = 0

                for equal_to_value in condition_value :
                    # if equal_to_value is a string , it will be enclosed by '' as Sheets needs to detect it as a string
                    if isinstance(equal_to_value, str):
                        equal_to_value = "'" + equal_to_value + "'" 

                    # adding paranthesis to have correct precedence among "and" , "or" operators
                    current_formula += '('

                    current_formula += (column_label_of_slice_condition) + "=" + str(equal_to_value)

                    # closing "or" paranthesis
                    current_formula += ')'

                    # if it is not the last value then insert "or" in between
                    if value_number != number_of_values - 1 : 
                        current_formula += ' or '

                    value_number += 1

            elif condition[1] == enums.Filters.NOT_IN :

                number_of_values = len(condition_value)
                value_number = 0

                for not_equal_to_value in condition_value :
                    # if not_equal_to_value is a string , it will be enclosed by '' as Sheets needs to detect it as a string
                    if isinstance(not_equal_to_value, str):
                        not_equal_to_value = "'" + not_equal_to_value + "'" 

                    # adding paranthesis to have correct precedence among "and" operators
                    current_formula += '('

                    current_formula += (column_label_of_slice_condition) + "!=" + "'" + str(not_equal_to_value) + "'"

                    # closing "and" paranthesis
                    current_formula += ')'

                    # if it is not the last value then insert "and" in between
                    if value_number != number_of_values - 1 :
                        current_formula += ' and '

                    value_number += 1



            # end the condition in query with a close paranthesis
            current_formula += ')'


            # if it is not the last condition then insert an "and" in between
            if condition_number != number_of_conditions - 1 :
                current_formula += ' and '

            condition_number += 1


        # Apply date_range filter condition
        if date_range is not None : 

            # if conditions other than date range are present then insert a "and"
            if number_of_conditions > 0:
                current_formula += ' and '

            # adding paranthesis to have correct precedence among "and" operators
            current_formula += '('

            date_column_label = cheader_to_clabel[ date_column_name ]

            current_formula += str(date_column_label) + " >= " + "date " + "'" + str(date_range[0]) + "'"

            current_formula += " and "

            current_formula +=  str(date_column_label) + " <= " + "date " + "'" + str(date_range[1]) + "'"
 
            # closing "and" paranthesis
            current_formula += ')'


        current_formula += '")))'

        list_of_formulas.append(current_formula)

    return list_of_formulas




def insert_as_column_topk_column(table, cheader_to_clabel, row_start_label, row_end_label, column_start_label, column_end_label, filter_column_label, metric, is_asc, k):
    """
    This function is called by main.py to insert the topk column
    It returns a list of strings , 1 for each row , representing the required
    sheets formula that needs to be inserted.

    0 indexing is followed
    
    Args : 
        table : Type-Pandas dataframe
            Contents of the sheets
        cheader_to_clabel : Type-Dictionary
            short for column_header_to_column_label , represents
            the corresponding column label which is given by sheets
            to the respective column headers
        row_start_label : Type-int
            sheet label(1-indexed) of the first row of table
            Note : This row_start_label doesn't contain the header row
            it is specifically the starting row of the data
        row_end_label : Type-int
            sheet label(1-indexed) of the last row of table
        column_start_label : Type-str
            sheet label of the first column of table
        column_end_label : Type-str
            sheet label of the last column of table
        filter_column_label : Type-str
            sheet label of the column in which topk column needs to be inserted
        metric : Type-str
            column name of the column on the basis of which top-k is decided
        is_asc: Type-Bool
            Denotes the sort order, True for ascending, False for Descending
        k : Type-int
            the k value of top-k intent        

    Returns :
        List of strings, list[i] denotes that ith row
        sheet formula
    """ 

    list_of_formulas = []

    metric_column_label = cheader_to_clabel[metric]

    for i in range(row_start_label, row_end_label + 1) :

        current_formula = '=NOT(ISNA(QUERY('

        # adding the row data range
        current_formula += str(column_start_label) + str(i) + ':' + str(filter_column_label) + str(i)

        # adding comma before start of the SQL-like respective query
        current_formula += ', "'

        # starting the initial part of the SQL-like query
        current_formula += 'select ' + str(column_start_label) + ' where '

        # adding the condition that it should pass all the filters
        current_formula += '(' + str(filter_column_label) + '=true' + ')'

        current_formula += ' and '

        # start of the top-k condition
        current_formula += '(' 

        # checking for the metric column
        current_formula += str(metric_column_label) + ' '

        # decing > or < on basis of ascending or descending query
        if is_asc :
            current_formula += '>= '
        else :
            current_formula += '<= '

        # the top-k condition
        current_formula += '"&large(filter(' + str(metric_column_label) + str(row_start_label) + ':' + str(metric_column_label) + str(row_end_label) + ','

        # applying the filter to only check topk for the values which pass filters and date range
        current_formula += str(filter_column_label) + str(row_start_label) + ':' + str(filter_column_label) + str(row_end_label) + '=TRUE' + ')'

        # closing the inside formula
        current_formula += ',' + str(k) + ')' + '&"'

        current_formula += ')"'

        # closing the outside formula
        current_formula += ')))'

        list_of_formulas.append(current_formula)

    return list_of_formulas