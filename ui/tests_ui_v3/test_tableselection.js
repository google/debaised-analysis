// Tests relared to data range selection

/**
 * Master test function for data range selection
 * Sheet1's data influences all tests
 */
function testTableSelectionFunctions() {
  testAutoDetectTable1();
  testAutoDetectTable2();
  
  testGetSelectedRange1();
  testGetSelectedRange2();
  
  testSelectEntireTableFromGivenRange();
  
  testSetSelectedRange1();
  testSetSelectedRange2();
  testSetSelectedRange3();
  testSetSelectedRange4();
     
  testGetHeaders();
  testGetSelectedCell();
  testGetFilterValues();
}

/**
 * Test: autoDetectTable()
 * When number of cells selected by user > Threshold (2 rows and area 5)
 */
function testAutoDetectTable1() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('B6:G12'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.autoDetectTable();
  var expectedOutput = {
   'inputSheet': 'Sheet1',
   'rangeString': 'B6:G12',
   'headerRow': 6,
   'headerRange': 'B6:G6'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'autoDetectTable1');
}

/**
 * Test: autoDetectTable()
 * When number of cells selected by user <= Threshold 
 */
function testAutoDetectTable2() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('C5:E6'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.autoDetectTable();
  var expectedOutput = {
   'inputSheet': 'Sheet1',
   'rangeString': 'A1:G44',
   'headerRow': 1,
   'headerRange': 'A1:G1'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'autoDetectTable2');
}

/**
 * Test: selectTable()
 */
function testSelectTable() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  var range = sheet.getRange('D7:F13');
  
  // Call the function to test
  var generatedOutput = 
    IntentsUi.selectTable(range.getRow(), 
                          range.getLastRow(), 
                          range.getColumn(), 
                          range.getLastColumn(), 
                          sheet.getDataRange().getValues(),
                          sheet.getDataRange().getLastRow(),
                          sheet.getDataRange().getLastColumn());
  var expectedOutput = [1, 44, 1, 7];
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'selectTable');
}

/**
 * Test: getSelectedRange()
 * When the range selected is not a subset of previous selected range
 */
function testGetSelectedRange1() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('A1:J50'));
  
  IntentsUi.setUserProperties(sheet, 'A1:G44', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getSelectedRange();
  var expectedOutput = {
     'rangeString': 'A1:J50',
     'headerRow': 1,
     'headerRange': 'A1:J1' 
  };
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'getSelectedRange1');
}

/**
 * Test: getSelectedRange()
 * When the range selected is a subset of previous selected range
 */
function testGetSelectedRange2() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('A10:G40'));
  
  IntentsUi.setUserProperties(sheet, 'A1:G44', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getSelectedRange();
  var expectedOutput = {
     'rangeString': 'A10:G40',
     'headerRow': 1,
     'headerRange': 'A1:G1' 
  };
  
  // Checking if generated output is same as expected output 
  assertEquals(expectedOutput, generatedOutput, 'getSelectedRange2');
  
}

/**
 * Test: selectEntireTableFromGivenRange(rangeString)
 */
function testSelectEntireTableFromGivenRange() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A1:G44', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = IntentsUi.selectEntireTableFromGivenRange('A10:G40');
  var expectedOutput = {
     'rangeString': 'A1:G44',
     'headerRow': 1,
     'headerRange': 'A1:G1' 
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'selectEntireTableFromGivenRange');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a header row in middle/end of the range selected
 */
function testSetSelectedRange1() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('A10:G44',15,'A15:G15');
  var expectedOutput = {
   'success': false,
   'errorIn': 'header-row',
   'errorMessage': 'Please select a header above the range selected'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange1');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a header row not in first/second row of the table
 */
function testSetSelectedRange2() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('A10:G40',5,'A5:G5');
  var expectedOutput = {
   'success': false,
   'errorIn': 'header-row',
   'errorMessage': 'Please select a header present in first/second row of the table'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange2');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a range with less than 2 rows or 2 columns
 */
function testSetSelectedRange3() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('A10:G10',1,'A1:G1');
  var expectedOutput = {
   'success': false,
   'errorIn': 'range',
   'errorMessage': 'Please select a range with more than 2 rows and 2 columns'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange3');
}

/**
 * Test: setSelectedRange(rangeString, headerRow, headerRange)
 * When user selects a valid range
 */
function testSetSelectedRange4() {
  // Call the function to test
  var generatedOutput = IntentsUi.setSelectedRange('A10:G40',1,'A1:G1');
  var expectedOutput = {
   'success': true,
   'inputSheet': 'Sheet1',
   'rangeString': 'A10:G40',
   'headerRow': 1,
   'headerRange': 'A1:G1'
  };
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setSelectedRange4');
}

/**
 * Test: getHeaders()
 */
function testGetHeaders() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A1:G44', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = IntentsUi.getHeaders();
  var expectedOutput = sheet.getRange('A1:G1').getValues()[0];
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getHeaders');
}

/**
 * Test: getSelectedCell()
 */
function testGetSelectedCell() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('A50:C55'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.getSelectedCell();
  var expectedOutput = 'A50';
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getSelectedCell');
}

/**
 * Test: getFilterValues()
 */
function testGetFilterValues() {
  // Set active range in Sheet1
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  SpreadsheetApp.setActiveSheet(sheet);
  sheet.setActiveRange(sheet.getRange('C6:C10'));
  
  // Call the function to test
  var generatedOutput = IntentsUi.getFilterValues();
  var expectedOutput = sheet.getActiveRange().getValues();
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getFilterValues');
}