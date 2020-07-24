// Tests for selecting data range

/**
 * Master test function for testing the data range selected
 * Sheet1's data influences all tests
 */
function testTableSelectionFunctions() {
  testPreComputeTableRange_aboveThreshold();
  testPreComputeTableRange_underThreshold();
  
  testDetectTableFromGivenRange();
  
  testGetSelectedRange_isSubsetOfPrevious();
  testGetSelectedRange_isNotSubsetOfPrevious();
  
  testSelectEntireTable();
  
  testSetSelectedRange_headerInMiddleOfRange();
  testSetSelectedRange_headerNotAtTop();
  testSetSelectedRange_rangeTooSmall();
  testSetSelectedRange_validHeaderAndRange();
     
  testGetHeaders();
  testGetFilterValues();
}

/**
 * Test: preComputeTableRange()
 * When number of cells selected by user > Threshold (2 rows and area 5)
 */
function testPreComputeTableRange_aboveThreshold() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('D5:G10'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.preComputeTableRange();
  var expectedOutput = {
   'inputSheet': 'Sheet1',
   'entireTableRange': 'C3:I46',
   'rangeA1Notation': 'D5:G10',
   'headerRow': 3,
   'headerRange': 'D3:G3'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'preComputeTableRange_aboveThreshold');
}

/**
 * Test: preComputeTableRange()
 * When number of cells selected by user <= Threshold 
 */
function testPreComputeTableRange_underThreshold() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('C3'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.preComputeTableRange();
  var expectedOutput = {
   'inputSheet': 'Sheet1',
   'entireTableRange': 'C3:I46',
   'rangeA1Notation': 'C3:I46',
   'headerRow': 3,
   'headerRange': 'C3:I3'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'preComputeTableRange_underThreshold');
}

/**
 * Test: detectTableFromGivenRange()
 */
function testDetectTableFromGivenRange() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  var range = sheet.getRange('D7:F13');
  
  // Call the function to test
  var generatedOutput = 
    IntentsUi.detectTableFromGivenRange(range.getRow(), 
                                        range.getLastRow(), 
                                        range.getColumn(), 
                                        range.getLastColumn(), 
                                        sheet.getDataRange().getValues(),
                                        sheet.getDataRange().getLastRow(),
                                        sheet.getDataRange().getLastColumn());
  var expectedOutput = [3, 46, 3, 9];
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'detectTableFromGivenRange');
}

/**
 * Test: getSelectedRange()
 * When the range selected is a subset of previous selected range
 */
function testGetSelectedRange_isSubsetOfPrevious() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('D5:H15'));
  
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I46', 3, 'C3:I3','C3:I46');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getSelectedRange();
  var expectedOutput = {
     'rangeA1Notation': 'D5:H15',
     'headerRow': 3,
     'headerRange': 'D3:H3' 
  };
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'getSelectedRange_isSubsetOfPrevious');
}

/**
 * Test: getSelectedRange()
 * When the range selected is not a subset of previous selected range
 */
function testGetSelectedRange_isNotSubsetOfPrevious() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('A1:J50'));
  
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I46', 3, 'C3:I3','C3:I46');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getSelectedRange();
  var expectedOutput = {
     'rangeA1Notation': 'A1:J50',
     'headerRow': 1,
     'headerRange': 'A1:J1' 
  };
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'getSelectedRange_isNotSubsetOfPrevious');
}

/**
 * Test: selectEntireTable(tableA1Notation)
 */
function testSelectEntireTable() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  
  // Call the function to test
  var generatedOutput = IntentsUi.selectEntireTable('C3:I46');
  var expectedOutput = {
     'rangeA1Notation': 'C3:I46',
     'headerRow': 3,
     'headerRange': 'C3:I3' 
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'selectEntireTable');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a header row in middle/end of the range selected
 */
function testSetSelectedRange_headerInMiddleOfRange() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('C3:I46',5,'C5:I5');
  var expectedOutput = {
   'success': false,
   'errorIn': 'headerRow'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange_headerInMiddleOfRange');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a header row not in first/second row of the table
 */
function testSetSelectedRange_headerNotAtTop() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('C5:I46',5,'C5:I5');
  var expectedOutput = {
   'success': false,
   'errorIn': 'headerRow'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange__headerNotAtTop');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a range with only 1 row
 */
function testSetSelectedRange_rangeTooSmall() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('C3:I3',3,'C3:I3');
  var expectedOutput = {
   'success': false,
   'errorIn': 'range'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange_rangeTooSmall');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a valid range and header row
 */
function testSetSelectedRange_validHeaderAndRange() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('C5:I15',3,'C3:I3');
  var expectedOutput = {
   'success': true,
   'inputSheet': 'Sheet1',
   'entireTableRange': 'C3:I46',
   'rangeA1Notation': 'C5:I15',
   'headerRow': 3,
   'headerRange': 'C3:I3'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange_validHeaderAndRange');
}

/**
 * Test: getHeaders()
 */
function testGetHeaders() {
  // Setting user properties
  IntentsUi.setUserProperties('Sheet1', 'C3:I46', 3, 'C3:I3','C3:I46');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getHeaders();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var expectedOutput = sheet.getRange('C3:I3').getValues()[0];
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getHeaders');
}

/**
 * Test: getFilterValues()
 */
function testGetFilterValues() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('E7:E10'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.getFilterValues();
  var expectedOutput = sheet.getActiveRange().getValues();
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getFilterValues');
}