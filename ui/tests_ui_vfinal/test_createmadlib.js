// Tests for creating query from given json

/**
 * Master test function for testing the madlib query
 * created for all the 6 intents
 */
function testCreateQueryFunctions() {
  testCreateQueryFromJsonShow();
  testCreateQueryFromJsonTopK();
  testCreateQueryFromJsonSliceCompare();
  testCreateQueryFromJsonTimeCompare();
  testCreateQueryFromJsonTrend();
  testCreateQueryFromJsonCorrelation();
}

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: SHOW
 */
function testCreateQueryFromJsonShow() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQueryShow);
  var expectedOutput = 
    'Show Sum of Units for Item from OrderDate 2019-01-06 to 2019-07-12';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'createQueryFromJsonShow');
} 

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: TOP-K
 */
function testCreateQueryFromJsonTopK() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQueryTopK);
  var expectedOutput = 
    'Find the top-7 Rep with maximum Total where Units is Greater than 50';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'createQueryFromJsonTopK');
}

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: SLICE-COMPARE
 */
function testCreateQueryFromJsonSliceCompare() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQuerySliceCompare);
  var expectedOutput = 
    'Compare the Mean of Unit Cost for the Region East and West by Item';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'testCreateQueryFromJsonSliceCompare');
}

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: TIME-COMPARE
 */
function testCreateQueryFromJsonTimeCompare() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQueryTimeCompare);
  var expectedOutput = 
    'Compare the Mean of Unit Cost for the OrderDate 2019-01-06 to 2019-03-15' +
    ' and 2019-04-01 to 2019-07-12 by Region';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'testCreateQueryFromJsonTimeCompare');
}

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: TREND
 */
function testCreateQueryFromJsonTrend() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQueryTrend);
  var expectedOutput = 
    'Monthly trend of Sum of Units where Item is In Binder, Pencil, Pen' +
    ' from OrderDate 2019-01-06 to 2019-07-12';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'createQueryFromJsonTrend');
} 

/**
 * Test: createQueryFromJson(jsonQuery)
 * Creating query for: CORRELATION
 */
function testCreateQueryFromJsonCorrelation() {
  // Call the function to test
  var generatedOutput = createQueryFromJson(jsonQueryCorrelation);
  var expectedOutput = 
    'Correlation between Unit Cost and Total for each Item';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'createQueryFromJsonCorrelation');
}
 
/**
 * Create madlib for the query using the json received
 * @param {string} jsonQuery - The json of submitted query
 * @return {string} madlibQuery - The query constructed from the json
 * 
 * Client side js function of project <can't be called from script>
 */
function createQueryFromJson(jsonQuery) {
  jsonQuery = JSON.parse(jsonQuery);
  
  // Storing name of intent
  var intent = jsonQuery['intent'];
  
  var filtersAndDate = '';
  // Adding slices
  if(jsonQuery.hasOwnProperty('slices')) {
    filtersAndDate += ' where ';
    for(var i = 0; i < jsonQuery.slices.length; i++) {
      filtersAndDate += jsonQuery.slices[i].sliceCol + ' is ';
      filtersAndDate += jsonQuery.slices[i].sliceOp + ' ';
      if(jsonQuery.slices[i].sliceOp === 'In' || jsonQuery.slices[i].sliceOp === 'Not in') {
        var sliceVal = jsonQuery.slices[i].sliceVal;
        filtersAndDate += sliceVal[0];
        for(var j = 1; j < sliceVal.length; j++) {
          filtersAndDate += ', ' + sliceVal[j];
        }
      }
      else {
        filtersAndDate += jsonQuery.slices[i].sliceVal;
      }
      filtersAndDate += ', ';
    }
    filtersAndDate = filtersAndDate.slice(0,filtersAndDate.length - 2);
  }
  // Adding date range
  if(jsonQuery.hasOwnProperty('dateRange')) {
    filtersAndDate += ' from ';
    filtersAndDate += jsonQuery.dateRange.dateCol + ' ';
    filtersAndDate += jsonQuery.dateRange.dateStart + ' to ' + jsonQuery.dateRange.dateEnd;
  }
  
  // Store madlib query created
  var madlibQuery = '';
  
  switch (intent) {
    case 'show': 
      madlibQuery += 'Show ';	
      
      // Adding metric and summary operation
      if(jsonQuery.hasOwnProperty('metric')) {
        if(jsonQuery.hasOwnProperty('summaryOperator')) {
          madlibQuery += jsonQuery.summaryOperator + ' of ';
        }
        madlibQuery += jsonQuery.metric;
      }
      if(jsonQuery.hasOwnProperty('metric') && jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += ' for ';
      }
      
      // Adding dimension
      if(jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += jsonQuery.dimensions[0];
        for(var i = 1; i < jsonQuery.dimensions.length; i++) {
          madlibQuery += ', ' + jsonQuery.dimensions[i];
        }
      }
      
      break;
      
    case 'topk': 
      madlibQuery += 'Find the ';
      
      // Adding limit(k)
      madlibQuery += 'top-' + jsonQuery.topKLimit + ' ';
      
      // Adding dimensions
      if(jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += jsonQuery.dimensions[0];
        for(var i = 1; i < jsonQuery.dimensions.length; i++) {
          madlibQuery += ', ' + jsonQuery.dimensions[i];
        }
      }
      
      // Adding sort order
      madlibQuery += ' with ';
      if(jsonQuery.isAsc) 
        madlibQuery += 'minimum ';
      else
        madlibQuery += 'maximum ';
      
      // Adding metric and summary operation
      if(jsonQuery.hasOwnProperty('metric')) {
        if(jsonQuery.hasOwnProperty('summaryOperator')) {
          madlibQuery += jsonQuery.summaryOperator + ' of ';
        }
        madlibQuery += jsonQuery.metric;
      }
      
      break;
      
    case 'slice_compare': 
      madlibQuery += 'Compare the ';
      
      // Adding metric and summary operation
      if(jsonQuery.hasOwnProperty('metric')) {
        if(jsonQuery.hasOwnProperty('summaryOperator')) {
          madlibQuery += jsonQuery.summaryOperator + ' of ';
        }
        madlibQuery += jsonQuery.metric;
      }
      
      // Adding comparison column and comparison values
      madlibQuery += ' for the ';
      madlibQuery += jsonQuery.comparisonValue.comparisonColumn + ' ';
      madlibQuery += jsonQuery.comparisonValue.slice1 + ' and ';
      var value2 = 'everything';
      if(jsonQuery.comparisonValue.slice2 !== '*') {
        value2 = jsonQuery.comparisonValue.slice2;
      }
      madlibQuery += value2;
      
      // Adding dimensions
      if(jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += ' by ';
        madlibQuery += jsonQuery.dimensions[0];
        for(var i = 1; i < jsonQuery.dimensions.length; i++) {
          madlibQuery += ', ' + jsonQuery.dimensions[i];
        }
      }
      
      break;
      
    case 'time_compare': 
      madlibQuery += 'Compare the ';
      
      // Adding metric and summary operation
      if(jsonQuery.hasOwnProperty('metric')) {
        if(jsonQuery.hasOwnProperty('summaryOperator')) {
          madlibQuery += jsonQuery.summaryOperator + ' of ';
        }
        madlibQuery += jsonQuery.metric;
      }
      
      // Adding comparison column and comparison values
      madlibQuery += ' for the ';
      madlibQuery += jsonQuery.compareDateRange.dateCol + ' ';
      madlibQuery += jsonQuery.compareDateRange.dateStart1 + ' to ' + jsonQuery.compareDateRange.dateEnd1;
      madlibQuery += ' and '
      madlibQuery += jsonQuery.compareDateRange.dateStart2 + ' to ' + jsonQuery.compareDateRange.dateEnd2;
      
      // Adding dimensions
      if(jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += ' by ';
        madlibQuery += jsonQuery.dimensions[0];
        for(var i = 1; i < jsonQuery.dimensions.length; i++) {
          madlibQuery += ', ' + jsonQuery.dimensions[i];
        }
      }
      
      break;
      
    case 'trend': 
      // Adding time granularity
      madlibQuery += jsonQuery.timeGranularity + ' trend of ';	
      
      // Adding metric and summary operation
      if(jsonQuery.hasOwnProperty('metric')) {
        if(jsonQuery.hasOwnProperty('summaryOperator')) {
          madlibQuery += jsonQuery.summaryOperator + ' of ';
        }
        madlibQuery += jsonQuery.metric;
      }
      
      break;
      
    case 'correlation': 
      madlibQuery += 'Correlation between '; 
      
      // Adding metrics for correlation
      if(jsonQuery.hasOwnProperty('correlationMetrics')) {
        madlibQuery += jsonQuery.correlationMetrics.metric1 + ' and ';
        madlibQuery += jsonQuery.correlationMetrics.metric2;
      }
      
      // Adding dimensions
      if(jsonQuery.hasOwnProperty('dimensions')) {
        madlibQuery += ' for each ';
        madlibQuery += jsonQuery.dimensions[0];
        for(var i = 1; i < jsonQuery.dimensions.length; i++) {
          madlibQuery += ', ' + jsonQuery.dimensions[i];
        }
      }
      
      break;
  }
  madlibQuery += filtersAndDate;
  
  // Returning the computed madlib query
  return madlibQuery;
}