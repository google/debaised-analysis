// Tests for error check fucntions on client-side javascript

/**
 * Master test function for testing the error checks 
 * written on cliend-side javacript
 */
function testErrorCheckFunctions() {
  testIsValidColumnName1();
  testIsValidColumnName2();
  
  testIsValidDateColumn1();
  testIsValidDateColumn2();
  
  testSliceValCompatible1();
  testSliceValCompatible2();
  
  testCheckRangeValidity1();
  testCheckRangeValidity2();
  
  testCheckHeaderValidity1();
  testCheckHeaderValidity2();
  
  testSetHeaderRange1();
  testSetHeaderRange2();
}

/**
 * List of columns headers and date columns
 */
var headers = ['OrderDate', 'Region', 'Rep', 'Item', 'Units', 'Unit Cost', 'Total'];
var dateColumnNames = ['OrderDate'];

/**
 * Test: isValidColumnName(column)
 * When column specified is one of the headers
 */
function testIsValidColumnName1() {
  // Call the function to test
  var generatedOutput = isValidColumnName('Item');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'isValidColumnName1');
}

/**
 * Test: isValidColumnName(column)
 * When column specified is not one of the headers
 */
function testIsValidColumnName2() {
  // Call the function to test
  var generatedOutput = isValidColumnName('Items');
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'isValidColumnName2');
}

/**
 * Check if the column specified is valid
 * (i.e is one of the table's column header)
 * @param {string} column The column to be checked for validity
 * @return {boolean} True indictes valid and false indicates invalid
 */
function isValidColumnName(column) {
  // Column entered is not considered valid if the index = -1
  var index = headers.indexOf(column);
  if(column === '' || index !== -1)
    return true;
  return false;
}

/**
 * Test: isValidDateColumn(dateColumnValue)
 * When column specified is one of the date columns
 */
function testIsValidDateColumn1() {
  // Call the function to test
  var generatedOutput = isValidDateColumn('OrderDate');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'isValidDateColumn1');
}

/**
 * Test: isValidDateColumn(dateColumnValue)
 * When column specified is not one of the date columns
 */
function testIsValidDateColumn2() {
  // Call the function to test
  var generatedOutput = isValidDateColumn('Rep');
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'isValidDateColumn2');
}

/**
 * Check if the date column specified is valid
 * (i.e is one of the table's date column)
 * @param {string} dateColumnValue The column to be checked for validity as a date column
 * @return {boolean} True indictes valid and false indicates invalid
 */
function isValidDateColumn(dateColumnValue) {
  // Date column entered is not considered valid if the index = -1
  var index = dateColumnNames.indexOf(dateColumnValue);
  if(dateColumnValue === '' || index !== -1)
    return true;
  return false;
}

/**
 * Test: sliceValCompatibleUtil(sliceValue,sliceOperation)
 * When slice values and slice operation are compatible
 */
function testSliceValCompatible1() {
  // Call the function to test
  var generatedOutput = sliceValCompatibleUtil([5.85], 'Less than');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'sliceValCompatible1');
}

/**
 * Test: sliceValCompatibleUtil(sliceValue,sliceOperation)
 * When slice values and slice operation are not compatible
 */
function testSliceValCompatible2() {
  // Call the function to test
  var generatedOutput = sliceValCompatibleUtil(['East', 'West'], 'Equal to');
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'sliceValCompatible2');
}

/**
* Find whether the slice operation and slice values entered are compatible
* @param {Array} sliceValue - The list of slice values entered
* @param {string} sliceOperation - The slice operation selected by user
* @return {boolean} True indicates compatible and false indicates incompatible
*/
function sliceValCompatibleUtil(sliceValue,sliceOperation) {
  if(sliceValue.length === 1 && sliceValue[0] === '')
    return true;
  
  // If slice operation is not (In,Not in),the length of sliceValue array 
  // should not be greater than 1 
  // For slice operations <, <=, >, >= : the slice value should be a number
  if(sliceOperation !== 'In' && sliceOperation !== 'Not in') {
    if(sliceValue.length > 1) {
      return false;
    }
    if(sliceOperation !== 'Equal to' &&  sliceOperation !== 'Not equal to') {
      if(isNaN(sliceValue[0])) {
        return false;
      }
    }
  }
  return true;
}

/**
 * Test: checkRangeValidity(a1Notation)
 * When the A1Notation given is valid
 */
function testCheckRangeValidity1() {
  // Call the function to test
  var generatedOutput = checkRangeValidity('C5:20');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkRangeValidity1');
}

/**
 * Test: checkRangeValidity(a1Notation)
 * When the A1Notation given is not valid
 */
function testCheckRangeValidity2() {
  // Call the function to test
  var generatedOutput = checkRangeValidity('C:20');
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkRangeValidity2');
}

/**
 * Check if the A1Notation of the range entered by user is valid
 * @param {string} a1Notation - The range entered by user
 * @return {boolean} - True indicates the range is valid and false indicates invalid
 */
function checkRangeValidity(a1Notation) {
  /**
  * Separate a1notation into 2 parts 
  * before ':' is start cell
  * after ':' is end cell (blank is case of no ':')
  */
  var index = a1Notation.indexOf(':');
  var startCell = '';
  var endCell = '';
  if(index != -1) {
    startCell = a1Notation.slice(0,index);
    endCell = a1Notation.slice(index+1);
  }
  else {
    startCell = a1Notation;
  }
  
  // If start cell is of the form: B5 - valid
  if(/(([a-zA-Z]+)([0-9]+))$/.test(startCell)) {
    // If end cell is of the form: D20 / D / 20 or there is no end cell, range is valid
    if(
      (/(([a-zA-Z]+)([0-9]*))$/.test(endCell)) || 
      (/(([0-9]+))$/.test(endCell)) || 
      (index === -1 && endCell === '')
    ) {
      return true;
    }
    return false;
  }
  
  // Else if start cell is of the form: B - valid
  else if(/(([a-zA-Z]+))$/.test(startCell)) {
    // If end cell is of the form: D20 / D, range is valid
    if(/(([a-zA-Z]+)([0-9]*))$/.test(endCell)) {
      return true;
    }
    return false;
  }
  
  // Else if start cell is of the form: 5 - valid
  else if(/(([0-9]+))$/.test(startCell)) {
    // If end cell is of the form: D20 / 20, range is valid
    if((/(([a-zA-Z]+)([0-9]+))$/.test(endCell)) || (/(([0-9]+))$/.test(endCell))) {
      return true;
    }
    return false;
  }
  
  // Else the range is not valid
  return false;
}
 
/**
 * Test: checkheaderValidity(headerRowValue)
 * When the header row given is valid
 */
function testCheckHeaderValidity1() {
  // Call the function to test
  var generatedOutput = checkHeaderValidity('3');
  var expectedOutput = true;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkHeaderValidity1');
} 

/**
 * Test: checkheaderValidity(headerRowValue)
 * When the header row given is not valid
 */
function testCheckHeaderValidity2() {
  // Call the function to test
  var generatedOutput = checkHeaderValidity('-3');
  var expectedOutput = false;
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'checkHeaderValidity2');
}  

/**
 * Check if the specified header row is valid
 * @param {string} headerRowValue The header row to be checked for validity
 * @return {boolean} True indictes valid and false indicates invalid 
 */
function checkHeaderValidity(headerRowValue) {
  // Header row is not considered valid if it less than equal to 0 or empty
  var headerRowInteger = parseInt(headerRowValue);
  if(headerRowValue === '' || headerRowInteger <=0) {
    return false;
  }
  else {
    return true;
  }
}

/**
 * Test: setHeaderRange(headerRow, dataRange)
 * When headerRow and dataRange are valid
 */
function testSetHeaderRange1() {
  // Call the function to test
  var generatedOutput = setHeaderRange('3', 'C5:F20');
  var expectedOutput = 'C3:F3';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setHeaderRange1');
} 

/**
 * Test: setHeaderRange(headerRow, dataRange)
 * When one of headerRow and dataRange is not valid
 */
function testSetHeaderRange2() {
  // Call the function to test
  var generatedOutput = setHeaderRange('3', '5:E');
  var expectedOutput = '';
  
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'setHeaderRange2');
} 
  
/**
 * Set header range using the specified data range and header row
 * @param {string} headerRow The headerRow selected by user
 * @param {string} dataRange The a1Notation of data range selected by user
 * @return {string} headerRange The header range constructed using given values
 */
function setHeaderRange(headerRow, dataRange) {
  var headerRange = '';

  // Header range is not set if range or header row is invalid
  if(!checkRangeValidity(dataRange) || !checkHeaderValidity(headerRow)) {
    return headerRange;
  }

  // Separate a1notation into 2 parts - one before ':' and second after ':'
  var index = dataRange.indexOf(':');
  var startCell = '';
  var endCell = '';
  if(index != -1) {
    startCell = dataRange.slice(0,index);
    endCell = dataRange.slice(index+1);
  }
  else {
    startCell = dataRange;
  }

  // Convert header row from string to number
  headerRow = parseInt(headerRow);
  
  // Start column for header range
  var startColumn = '';
  for(var i = 0; i < startCell.length; i++) {
    if(isNaN(startCell[i])) {
      startColumn += startCell[i];
    }
    else {
      break;
    }
  }
  
  // End column for header range
  var endColumn = '';
  for(var i = 0; i < endCell.length; i++) {
    if(isNaN(endCell[i])) {
      endColumn += endCell[i];
    }
    else {
      break;
    }
  }
  
  if(startColumn === '' && endColumn === '') {
    startColumn = 'A';
  }
  
  // Constructing the header range
  headerRange += startColumn + headerRow;
  if(endColumn !== startColumn && index !== -1) {
    headerRange += ':' + endColumn + headerRow;
  }
  return headerRange;
}