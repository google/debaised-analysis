// Tests for formatting table cells

/**
 * Master test function for testing the cells formatting
 * Sheet1's formatting influences all tests 
 */
function testDataFormattingFunctions() {
  testCheckTableCellsFormattingPattern1();
  testCheckTableCellsFormattingPattern2();
  
  testCheckSameHeaderFormatting1();
  testCheckSameHeaderFormatting2();
  
  testCompareFormatting1();
  testCompareFormatting2();
}

/**
 * Test: checkTableCellsFormattingPattern(inputSheet, rangeString, headerRow)
 * When formatting of all cells is same
 */
function testCheckTableCellsFormattingPattern1() {
  // Call the function to test
  var generatedOutput = IntentsUi.checkTableCellsFormattingPattern('Sheet1', 'C4:I15', 3);
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkTableCellsFormattingPattern1');
}

/**
 * Test: checkTableCellsFormattingPattern(inputSheet, rangeString, headerRow)
 * When formatting of all cells is different
 */
function testCheckTableCellsFormattingPattern2() {
  // Call the function to test
  var generatedOutput = IntentsUi.checkTableCellsFormattingPattern('Sheet1', 'C2:I15', 2);
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkTableCellsFormattingPattern2');
}

/**
 * Test: checkSameHeaderFormatting(headerRange, sheet, sheetId)
 * When formatting of all header cells is same
 */
function testCheckSameHeaderFormatting1() {
  // Call the function to test
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var generatedOutput = IntentsUi.checkSameHeaderFormatting('C3:I3', sheet, sheet.getSheetId());
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkSameHeaderFormatting1');
}

/**
 * Test: checkSameHeaderFormatting(headerRange, sheet, sheetId)
 * When formatting of all header cells is different
 */
function testCheckSameHeaderFormatting2() {
  // Call the function to test
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  var generatedOutput = IntentsUi.checkSameHeaderFormatting('A3:I3', sheet, sheet.getSheetId());
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkSameHeaderFormatting2');
}

/**
 * Test: compareFormatting(cellFormat1, cellFormat2)
 * When the 2 cell formats are same
 */
function testCompareFormatting1() {
  // Call the function to test
  var format1 = {
    'backgroundColorStyle': {
      'rgbColor': {
        'red': 1.0
      }
    }, 
    'backgroundColor': {
      'red': 1.0
    }, 
    'numberFormat': {
      'pattern': 'M/d/yyyy', 
      'type': 'DATE'
    }
  };
  var format2 = {
    'backgroundColor': {
      'red': 1.0
    }, 
    'backgroundColorStyle': {
      'rgbColor': {
        'red': 1.0
      }
    } 
  };
  var generatedOutput = IntentsUi.compareFormatting(format1, format2);
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'compareFormatting1');
}

/**
 * Test: compareFormatting(cellFormat1, cellFormat2)
 * When the 2 cell formats are different
 */
function testCompareFormatting2() {
  // Call the function to test
  var format1 = {
    'backgroundColorStyle': {
      'rgbColor': {
        'green': 1.0
      }
    }, 
    'backgroundColor': {
      'red': 1.0
    }, 
    'numberFormat': {
      'pattern': 'M/d/yyyy', 
      'type': 'DATE'
    }
  };
  var format2 = {
    'backgroundColor': {
      'red': 1.0
    }, 
    'backgroundColorStyle': {
      'rgbColor': {
        'red': 1.0
      }
    } 
  };
  var generatedOutput = IntentsUi.compareFormatting(format1, format2);
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'compareFormatting2');
}