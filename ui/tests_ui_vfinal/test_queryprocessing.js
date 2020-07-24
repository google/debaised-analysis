// Tests for processing queries

/**
 * Master test function for testing the intent's queries
 */
function testQueryProcessingFunctions() {
  testEvalQueryShow();
  testEvalQueryTopK();
  testEvalQuerySliceCompare();
  testEvalQueryTimeCompare();
  testEvalQueryTrend();
  testEvalQueryCorrelation();
  testEvalQueryOnFailure();

  testGetTableData();

  testCallGcpToGetQueryResult_onSuccess();
  testCallGcpToGetQueryResult_onFailure();

  testCheckJsonValidity_isValid();
  testCheckJsonValidity_isInvalid();
}

/**
 * Test: evalQuery(
 *           intent, 
 *           metric, 
 *           summaryOperator, 
 *           isAsc, 
 *           topKLimit, 
 *           dimensions, 
 *           slices, 
 *           dateRange,
 *           timeGranularity, 
 *           comparisonValue, 
 *           compareDateRange, 
 *           correlationMetrics, 
 *           dateColumnInfo)
 */
 
var dateColumnsList = {
  'OrderDate': {
    'type': 'CONSISTENT', 
    'day_first': false, 
    'min_date': {'day_first_false': '2019-01-06'}, 
    'max_date': {'day_first_false': '2019-07-12'}
  }
}; 

/**
 * Test: evalQuery
 * SHOW
 * When gcp function executes successfully
 * Query: Show Sum of Units for Item from OrderDate 2019-01-06 to 2019-07-12
 */ 
function testEvalQueryShow() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);
  
  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('show', 
                        'Units', 
                        'Sum', 
                        false, 
                        10.0, 
                        ['Item'], 
                        [],
                        {'dateCol': 'OrderDate', 'dateStart': '2019-01-06', 'dateEnd': '2019-07-12'},
                        null, 
                        null, 
                        null,
                        null,
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryShow,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryShow');
}

/**
 * Test: evalQuery
 * TOP-K
 * When gcp function executes successfully
 * Query: Find the top-7 Rep with maximum Total where Units is Greater than 50
 */ 
function testEvalQueryTopK() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);
 
  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('topk', 
                        'Total', 
                        null, 
                        false, 
                        7.0, 
                        ['Rep'], 
                        [{'sliceCol': 'Units', 'sliceOp': 'Greater than', 'sliceVal': 50.0}],
                        null,
                        null, 
                        null, 
                        null,
                        null,
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryTopK,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryTopK');
}

/**
 * Test: evalQuery
 * SLICE COMPARE
 * When gcp function executes successfully
 * Query: Compare the Mean of Unit Cost for the Region East and West by Item
 */ 
function testEvalQuerySliceCompare() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);

  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('slice_compare', 
                        'Unit Cost', 
                        'Mean', 
                        false, 
                        10.0, 
                        ['Item'], 
                        [],
                        null,
                        null, 
                        {'comparisonColumn': 'Region', 'slice1': 'East', 'slice2': 'West'}, 
                        null,
                        null,
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQuerySliceCompare,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQuerySliceCompare');
}

/**
 * TIME COMPARE
 * Test: evalQuery 
 * When gcp function executes successfully
 * Query: Compare the Mean of Unit Cost for the OrderDate 
 * 2019-01-06 to 2019-03-15 and 2019-04-01 to 2019-07-12 by Region
 */ 
function testEvalQueryTimeCompare() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);

  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('time_compare', 
                        'Unit Cost', 
                        'Mean', 
                        false, 
                        10.0, 
                        ['Region'], 
                        [],
                        null,
                        null, 
                        null,
                        {'dateCol': 'OrderDate', 
                         'dateStart1': '2019-01-06', 
                         'dateEnd1': '2019-03-15', 
                         'dateStart2': '2019-04-01', 
                         'dateEnd2': '2019-07-12'}, 
                        null,
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryTimeCompare,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryTimeCompare');
}

/**
 * TREND
 * Test: evalQuery 
 * When gcp function executes successfully
 * Query: Monthly trend of Sum of Units where Item is In 
 * Binder, Pencil, Pen from OrderDate 2019-01-06 to 2019-07-12
 */ 
function testEvalQueryTrend() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);

  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('trend', 
                        'Units', 
                        'Sum', 
                        false, 
                        10.0, 
                        [], 
                        [{'sliceCol': 'Item', 'sliceOp': 'In', 'sliceVal': ['Binder', 'Pencil', 'Pen']}],
                        {'dateCol': 'OrderDate', 'dateStart': '2019-01-06', 'dateEnd': '2019-07-12'},
                        'Monthly', 
                        null, 
                        null,
                        null,
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryTrend,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryTrend');
}

/**
 * CORRELATION
 * Test: evalQuery 
 * When gcp function executes successfully
 * Query: Correlation between Unit Cost and Total for each Item
 */ 
function testEvalQueryCorrelation() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);

  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('correlation', 
                        null, 
                        null, 
                        false, 
                        10.0, 
                        ['Item'], 
                        [],
                        null,
                        null, 
                        null, 
                        null,
                        {'metric1': 'Unit Cost', 'metric2': 'Total'},
                        dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryCorrelation,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryCorrelation');
}

/**
 * Test: evalQuery
 * When gcp function fails
 */ 
function testEvalQueryOnFailure() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);
  
  // Call the function to test
  var receivedOutput = 
    IntentsUi.evalQuery('intent name', null, null, false, 10.0, [], [], {}, 
                        null, null, null, null, dateColumnsList);   
  var generatedOutput = {
    'status': receivedOutput.status,
    'outputTable':  receivedOutput.outputTable,
    'suggestions': receivedOutput.suggestions
  }                         
  var expectedOutput = {
    'status': 'fail',
    'outputTable': [[]],
    'suggestions': []
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryOnFailure');
}

/**
 * Test: getTable()
 */
function testGetTableData() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I15', 3, 'C3:I3', 'C3:I46');
  IntentsUi.setDateColumnsList(dateColumnsList);
  
  // Call the function to test
  var generatedOutput = IntentsUi.getTableData();
  var expectedOutput = [
    ['OrderDate', 'Region', 'Rep', 'Item', 'Units', 'Unit Cost', 'Total'], 
    ['1/6/2019', 'East', 'Jones', 'Pencil', 95.0, 1.99, 189.05], 
    ['1/23/2019', 'Central', 'Kivell', 'Binder', 50.0, 19.99, 999.4999999999999], 
    ['2/9/2019', 'Central', 'Jardine', 'Pencil', 36.0, 4.99, 179.64000000000001],
    ['2/26/2019', 'Central', 'Gill', 'Pen', 27.0, 19.99, 539.7299999999999],
    ['3/15/2019', 'West', 'Sorvino', 'Pencil', 56.0, 2.99, 167.44],
    ['4/1/2019', 'East', 'Jones', 'Pen', 60.0, 4.99, 299.40000000000003], 
    ['4/18/2019', 'Central', 'Andrews', 'Pencil', 75.0, 1.99, 149.25],
    ['5/5/2019', 'Central', 'Jardine', 'Pencil', 90.0, 4.99, 449.1],
    ['5/22/2019', 'West', 'Thompson', 'Pencil', 32.0, 1.99, 63.68],
    ['6/8/2019', 'East', 'Jones', 'Binder', 60.0, 8.99, 539.4],
    ['6/25/2019', 'Central', 'Morgan', 'Pencil', 90.0, 4.99, 449.1],
    ['7/12/2019', 'East', 'Howard', 'Binder', 29.0, 1.99, 57.71]
  ];

  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getTableData');
}

/**
 * Test: callGcpToGetQueryResult(inputJson)
 *
 * When gcp function executes successfully 
 * Query: Show Sum of Units for Item from OrderDate 2019-01-06 to 2019-07-12
 */
function testCallGcpToGetQueryResult_onSuccess() {
  // Call the function to test
  var receivedOutput = IntentsUi.callGcpToGetQueryResult(jsonQueryShow);    
  var generatedOutput = {
    'status': receivedOutput.status,
    'jsonQuery': receivedOutput.jsonQuery,
    'outputTableExist': ('outputTable' in receivedOutput),
    'suggestionsExist': ('suggestions' in receivedOutput)
  }                         
  var expectedOutput = {
    'status': 'success',
    'jsonQuery': jsonQueryShow,
    'outputTableExist': true,
    'suggestionsExist': true
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResult_onSuccess');
}

/**
 * Test: callGcpToGetQueryResult(inputJson)
 *
 * When gcp function fails
 */
function testCallGcpToGetQueryResult_onFailure() {
  // Call the function to test
  var receivedOutput = IntentsUi.callGcpToGetQueryResult({});    
  var generatedOutput = {
    'status': receivedOutput.status,
    'outputTable':  receivedOutput.outputTable,
    'suggestions': receivedOutput.suggestions
  }                         
  var expectedOutput = {
    'status': 'fail',
    'outputTable': [[]],
    'suggestions': []
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResult_onFailure');
}

/**
 * Test: checkJsonValidity(text)
 * When the json is valid
 */
function testCheckJsonValidity_isValid() {
  // Call the function to test
  var generatedOutput = IntentsUi.checkJsonValidity(jsonQueryShow);
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkJsonValidity_isValid');
} 

/**
 * Test: checkJsonValidity(text)
 * When the json is invalid
 */
function testCheckJsonValidity_isInvalid() {
  // Call the function to test
  var generatedOutput = IntentsUi.checkJsonValidity('{"dateCol":"OrderDate"}');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkJsonValidity__isInvalid');
} 