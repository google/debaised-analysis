// Functions for table range selection, getting list of headers and filter values from sheet

/**
 * Detect the table's range based on user's selected cells
 *
 * @return {Object} dataRange - The detected table range's details
 * @return {string} dateRange.inputSheet - The name of the sheet containing detected table
 * @return {string} dateRange.rangeString - The A1Notation of the range detected
 * @return {number} dateRange.headerRow - The header row number of the range detected
 * @return {string} dateRange.headerRange - The header range of the range detected
 */
function autoDetectTable() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getDataRange();
  var rangeActive = sheet.getActiveRange();

  // Getting start and end row, start and end column of the range preselected by user
  var rowEnd = rangeActive.getLastRow();
  var rowStart = rangeActive.getRow();
  var colEnd = rangeActive.getLastColumn();
  var colStart = rangeActive.getColumn();
  var maxRows = range.getLastRow();
  var maxCols = range.getLastColumn();
  
  Logger.log('Range of the selected cells');
  Logger.log(rowStart, rowEnd, colStart, colEnd, maxRows, maxCols);
  
  var dataRange;

  // If range selected by user has more than 2 rows and area > 5
  // detect the selected range as the table range
  if(rowEnd-rowStart>=2 && (rowEnd-rowStart+1)*(colEnd-colStart+1)>5) {
    dataRange = [rowStart, rowEnd, colStart, colEnd];
  }
  // Else detect the table containing the selected range
  else {
    dataRange =  selectTable(rowStart, rowEnd, colStart, colEnd, range.getValues(), maxRows, maxCols);
  }
    
  Logger.log('Range of the detected table');
  Logger.log(dataRange);

  // Find the detected range's a1Notation
  var rangeTable = sheet.getRange(dataRange[0], dataRange[2], dataRange[1]-dataRange[0]+1, dataRange[3]-dataRange[2]+1);
  var rangeString = rangeTable.getA1Notation();

  // Select the first row of the detected table as header row
  var headerRange = sheet.getRange(dataRange[0], dataRange[2], 1, dataRange[3]-dataRange[2]+1).getA1Notation();
  var headerRow = dataRange[0];

  // Storing details about the detected table
  var dataRange = {
   'inputSheet': sheet.getName(),
   'rangeString': rangeString,
   'headerRow': headerRow,
   'headerRange': headerRange
  };
  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperties(dataRange);
  
  return dataRange;
}

/**
 * Detects the table containing the specified range of cells
 *
 * @param {number} rowStart The start row of the specified range
 * @param {number} rowEnd The end row of the specified range
 * @param {number} colStart The start column of the specified range
 * @param {number} colEnd The end column of the specified range
 * @param {number} maxRows The last row of the sheet containing data
 * @param {number} maxCols The last column of the sheet containing data
 * @return {Array} The start row, end row, start column, end column of the detected table
 */
function selectTable(rowStart, rowEnd, colStart, colEnd, values, maxRows, maxCols) {
  /**
   * Flag is used to indicate if the detected range changes in current function call
   * Flag is set to true when the range changes
   * Flag set to false indicates the range did not change
   */
  var flag = false;
  
  for(var j = colStart; j <= colEnd && j <= maxCols; j++) {
    // check for blank values in up directorion
    for(var i = rowStart - 1; i >= 1 && i <= maxRows; i--) {
      if(values[i-1][j-1] === '') {
        break;
      }
      rowStart = i;
      flag=true;
    }
    // check for blank values in down directorion
    for(var i = rowEnd + 1; i <= maxRows; i++) {
      if(values[i-1][j-1] === '') {
        break;
      }
      rowEnd = i;
      flag=true;
    }
  }

  for(var i = rowStart; i <= rowEnd && i <= maxRows; i++) {
    // check for blank values in left directorion
    for(var j = colStart - 1; j >= 1 && j <= maxCols ; j--) {
      if(values[i-1][j-1] === '') {
        break;
      }
      colStart = j;
      flag=true;
    }
    // check for blank values in right directorion
    for(var j = colEnd + 1; j <= maxCols; j++) {
      if(values[i-1][j-1] === '') {
        break;
      }
      colEnd = j;
      flag=true;
    }
  }

  // If the detected range is altered the function is called again
  if(flag) {
    return selectTable(rowStart, rowEnd, colStart, colEnd, values, maxRows, maxCols);
  }
  // Else return the detected range from the function
  else {
    dataRange = [rowStart, rowEnd, colStart, colEnd];
    return dataRange;
  }
}

/**
 * Get the table selected by the user
 *
 * @return {Object} dataRange - The selected table range's details
 * @return {string} dateRange.rangeString - The A1Notation of the range selected
 * @return {number} dateRange.headerRow - The header row number of the range selected
 * @return {string} dateRange.headerRange - The header range of the range selected
 */
function getSelectedRange() {
  var sheet = SpreadsheetApp.getActiveSheet()
  var range = sheet.getActiveRange(); 

  // Storing A1Notation of selected range
  // and selecting first row of selected range as header
  var rangeString = range.getA1Notation(); 
  var headerRow = range.getRow();
  var headerRange = sheet.getRange(range.getRow(), range.getColumn(), 1, range.getWidth()).getA1Notation();
   
  var dataRange = {
     'rangeString': rangeString,
     'headerRow': headerRow,
     'headerRange': headerRange
  };
 
  // Getting the previous selected range
  var userProperties = PropertiesService.getUserProperties();
  var preSelectedRangeString = userProperties.getProperty('rangeString');
  var preSelectedRange = sheet.getRange(preSelectedRangeString);
  
  // Start and end row, start and end column of the selected range
  var rowStartNew = range.getRow();
  var rowEndNew = range.getLastRow();
  var colStartNew = range.getColumn();
  var colEndNew = range.getLastColumn();
  
  // Start and end row, start and end column of the previous selected range
  var rowStartOld = preSelectedRange.getRow();
  var rowEndOld = preSelectedRange.getLastRow();
  var colStartOld = preSelectedRange.getColumn();
  var colEndOld = preSelectedRange.getLastColumn();
  
  // If the new selected range is subset of previous selected range 
  // use the previous selected header row
  if(rowStartNew >= rowStartOld && rowEndNew <= rowEndOld) {
    if(colStartNew >= colStartOld && colEndNew <= colEndOld) {
      dataRange.headerRow = userProperties.getProperty('headerRow');
      dataRange.headerRange = sheet.getRange(Number(dataRange.headerRow), range.getColumn(), 1, range.getWidth()).getA1Notation();
    }
  }
  
  //printing dataRange object
  Logger.log('Range selected by user');
  Logger.log(dataRange);

  return dataRange;
}

/**
 * Detect the entire table containing the range selected by user
 *
 * @param {string} rangeString The A1Notation of range selected by user
 * @return {Object} dataRange - The detected table range's details
 * @return {string} dateRange.rangeString - The A1Notation of the range detected
 * @return {number} dateRange.headerRow - The header row number of the range detected
 * @return {string} dateRange.headerRange - The header range of the range detected
 */
function selectEntireTableFromGivenRange(rangeString) {
  var userProperties = PropertiesService.getUserProperties();
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(userProperties.getProperty('inputSheet'));
  var range = sheet.getRange(rangeString);

  // Getting entire table containing the selected range
  var dataRange = selectTable(range.getRow(),
                              range.getLastRow(),
                              range.getColumn(),
                              range.getLastColumn(),
                              sheet.getDataRange().getValues(),
                              sheet.getDataRange().getLastRow(),
                              sheet.getDataRange().getLastColumn());

  var table = sheet.getRange(dataRange[0], dataRange[2], dataRange[1]-dataRange[0]+1, dataRange[3]-dataRange[2]+1);
  var dataRange = {
   'rangeString': table.getA1Notation(),
   'headerRow': dataRange[0],
   'headerRange': sheet.getRange(dataRange[0], dataRange[2], 1, dataRange[3]-dataRange[2]+1).getA1Notation()
  };
  return dataRange;
}

/**
 * Update the range selected by user if it doesn't contain any error
 * Give error message in case of any invalid input
 *
 * @param {string} rangeString The A1Notation of range selected by user
 * @param {number} headerRow The header row of range selected by user
 * @param {string} headerRange The header range for the range selected by user
 *
 * @return {Object} updatedRangeObj - The updated range details in case of success 
 *                                    and error message in case of invalid input
 * @return {boolean} updatedRangeObj.succuss - Indicates validity of the range selected by user
 * @return {string} updatedRangeObj.errorIn - The field containing error: header-row/range 
 * @return {string} updatedRangeObj.errorMessage - The error message to display to user
 * @return {string} updatedRangeObj.inputSheet - The name of the sheet containing range
 * @return {string} updatedRangeObj.rangeString - The A1Notation of the range 
 * @return {number} updatedRangeObj.headerRow - The header row number of the range 
 * @return {string} updatedRangeObj.headerRange - The header range of the range
 */
function setSelectedRange(rangeString, headerRow, headerRange) {

  var inputSheet = SpreadsheetApp.getActiveSheet();
  var range = inputSheet.getRange(rangeString);

  // Getting entire table containing the selected range
  var entireTable = selectTable(range.getRow(),
                                range.getLastRow(),
                                range.getColumn(),
                                range.getLastColumn(),
                                inputSheet.getDataRange().getValues(),
                                inputSheet.getDataRange().getLastRow(),
                                inputSheet.getDataRange().getLastColumn());
  
  var updatedRangeObj = {};
  
  if(range.getRow() < headerRow) {
    //TODO - change the error message
    updatedRangeObj['success'] = false;
    updatedRangeObj['errorIn'] = 'header-row';
    updatedRangeObj['errorMessage'] = 'Please select a header above the range selected';
  }
  else if(entireTable[0] !== headerRow && entireTable[0]+1 !== headerRow) {
    //TODO - change the error message
    updatedRangeObj['success'] = false;
    updatedRangeObj['errorIn'] = 'header-row';
    updatedRangeObj['errorMessage'] = 'Please select a header present in first/second row of the table';
  }
  else if(range.getWidth()<2 || range.getHeight()<2) {
     //TODO - change the error message
    updatedRangeObj['success'] = false;
    updatedRangeObj['errorIn'] = 'range';
    updatedRangeObj['errorMessage'] = 'Please select a range with more than 2 rows and 2 columns';
  }
  // When all inputs are valid
  else {
    updatedRangeObj['success'] = true;
    range.activate();
    var userProperties = PropertiesService.getUserProperties();
    setUserProperties(inputSheet, rangeString, headerRow, headerRange);
    
    updatedRangeObj['inputSheet'] = userProperties.getProperty('inputSheet');
    updatedRangeObj['rangeString'] = userProperties.getProperty('rangeString');
    updatedRangeObj['headerRow'] = userProperties.getProperty('headerRow');
    updatedRangeObj['headerRange'] = userProperties.getProperty('headerRange');
  }
  return updatedRangeObj;
}

/**
 * Finds the column header names in the header row of table selected
 *
 * @return {Array} The list of column header names
 */
function getHeaders() {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet); 
  var headers = sheet.getRange(userProperties.getProperty('headerRange')).getValues();
  headers = headers[0];
  return headers;
}

/**
 * Selects the first cell of the range selected by user
 *
 * @return {string} The A1Notation of first cell of range selected
 */
function getSelectedCell() {
  var sheet = SpreadsheetApp.getActiveSheet()
  var range = sheet.getActiveRange(); 
  var cell = range.getCell(1, 1);
  var outputCell = cell.getA1Notation(); 
  return outputCell;
}

/**
 * Gets the values present in range selected by user to use them as filter values
 *
 * @return {Array} The list of values present in selected range
 */
function getFilterValues() {
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var values = range.getValues();
  return values;
}

/**
 * Set user properties to the values given
 *
 * @param {Sheet} inputSheet The sheet in which user selects data
 * @param {string} rangeString The A1Notation of range selected
 * @param {number} headerRow The header row of range selected
 * @param {string} headerRange The header range for the range selected
 */
function setUserProperties(inputSheet, rangeString, headerRow, headerRange) {
   var userProperties = PropertiesService.getUserProperties();
   userProperties.setProperty('inputSheet',inputSheet.getName());
   userProperties.setProperty('rangeString',rangeString);
   userProperties.setProperty('headerRow',headerRow);
   userProperties.setProperty('headerRange',headerRange);
}
