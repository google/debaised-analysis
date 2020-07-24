// Tests for detecting date columns and their format

/**
 * Master test function for testing detected date
 */
function testDetectDateFunctions() {
  testDetectDate();
  testCallGcpToDetectDate();
}

/**
 * Test: detectDate(rangeString, headerRow, inputSheet, entireTableRange)
 */
function testDetectDate() {  
  // Call the function to test
  var generatedOutput = IntentsUi.detectDate('C3:I46', 3, 'Sheet1', 'C3:I46');
  var expectedOutput = {
    'OrderDate': {
      'min_date': {'day_first_false': '2019-01-06'}, 
      'type': 'CONSISTENT', 
      'day_first': false, 
      'max_date': {'day_first_false': '2020-12-21'}
    }
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'detectDate');
}

/**
 * Test: callGcpToDetectDate(table)
 */
function testCallGcpToDetectDate() {  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var range = sheet.getRange('C3:I46');
  var table = range.getDisplayValues();
  
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToDetectDate(table);
  var expectedOutput = {
    'OrderDate': {
      'min_date': {'day_first_false': '2019-01-06'}, 
      'type': 'CONSISTENT', 
      'day_first': false, 
      'max_date': {'day_first_false': '2020-12-21'}
    }
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToDetectDate');
}
