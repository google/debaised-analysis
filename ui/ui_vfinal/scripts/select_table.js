// Functions for table range selection, getting list of headers and filter values from sheet

/**
 * Precompute the table's range based on user's selected cells
 *
 * @return {Object} dataRange - The detected table range's details
 * @return {string} dateRange.inputSheet - The name of the sheet containing detected table
 * @return {string} dateRange.rangeA1Notation - The A1Notation of the range detected
 * @return {number} dateRange.headerRow - The header row number of the range detected
 * @return {string} dateRange.headerRange - The header range of the range detected
 * @return {string} dateRange.entireTableRange - The A1Notation of the table range 
 *                                               containing the detected range
 */
function preComputeTableRange() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var sheetDataRange = sheet.getDataRange();
  var activeRange = sheet.getActiveRange();

  // Getting start and end row, start and end column of the range preselected by user
  var endRow = activeRange.getLastRow();
  var startRow = activeRange.getRow();
  var endCol = activeRange.getLastColumn();
  var startCol = activeRange.getColumn();
  var maxRows = sheetDataRange.getLastRow();
  var maxCols = sheetDataRange.getLastColumn();
  
  Logger.log('Range of the pre-selected cells');
  Logger.log(startRow, endRow, startCol, endCol, maxRows, maxCols);
  
  // Getting the detected table range
  var dataRange = {};
  var detectedTable = detectTableFromGivenRange(startRow, 
                                                endRow, 
                                                startCol, 
                                                endCol, 
                                                sheetDataRange.getValues(), 
                                                maxRows, 
                                                maxCols);
  var entireTableRange = sheet.getRange(detectedTable[0], 
                                        detectedTable[2], 
                                        detectedTable[1] - detectedTable[0] + 1, 
                                        detectedTable[3] - detectedTable[2] + 1);

  dataRange['inputSheet'] = sheet.getName();
  dataRange['entireTableRange'] = entireTableRange.getA1Notation();
  dataRange['headerRow'] = entireTableRange.getRow();

  // If range selected by user has more than 2 rows and area > 5 
  // consider the selected range as the table range
  if(endRow - startRow >= 2 && (endRow - startRow + 1) * (endCol - startCol + 1) > 5) {
    dataRange['rangeA1Notation'] = activeRange.getA1Notation();
    dataRange['headerRange'] = sheet.getRange(dataRange['headerRow'], 
                                              activeRange.getColumn(), 
                                              1, 
                                              activeRange.getWidth())
                                    .getA1Notation();
  }
  // Else consider the detected table as the table range
  else {
    dataRange['rangeA1Notation'] = entireTableRange.getA1Notation();
    dataRange['headerRange'] = sheet.getRange(dataRange['headerRow'], 
                                              entireTableRange.getColumn(), 
                                              1, 
                                              entireTableRange.getWidth())
                                    .getA1Notation();
  }
 
  Logger.log('Range of the detected table');
  Logger.log(dataRange);
    
  setUserProperties(dataRange['inputSheet'], 
                    dataRange['rangeA1Notation'],
                    dataRange['headerRow'],
                    dataRange['headerRange'],
                    dataRange['entireTableRange']);
  return dataRange;
}

/**
 * Detects the table containing the specified range of cells
 *
 * @param {number} startRow - The start row of the specified range
 * @param {number} endRow -  The end row of the specified range
 * @param {number} startCol -  The start column of the specified range
 * @param {number} endCol -  The end column of the specified range
 * @param {number} maxRows -  The last row of the sheet containing data
 * @param {number} maxCols -  The last column of the sheet containing data
 * @return {Array} - The start row, end row, start column, end column of the detected table
 */
function detectTableFromGivenRange(startRow, endRow, startCol, endCol, values, maxRows, maxCols) {
  /**
   * Flag is used to indicate if the detected range changes in current function call
   * Flag is set to true when the range changes and remains false when range does not change
   * Range is indicated by the startRow, endRow, startCol and endCol
   */
  var flag = false;
  
  for(var j = startCol; j <= endCol && j <= maxCols; j++) {
    // Check for blank values in the up directorion
    for(var i = startRow - 1; i >= 1 && i <= maxRows; i--) {
      if(values[i - 1][j - 1] === '') {
        break;
      }
      startRow = i;
      flag = true;
    }
    // Check for blank values in the down directorion
    for(var i = endRow + 1; i <= maxRows; i++) {
      if(values[i - 1][j - 1] === '') {
        break;
      }
      endRow = i;
      flag = true;
    }
  }

  for(var i = startRow; i <= endRow && i <= maxRows; i++) {
    // Check for blank values in the left directorion
    for(var j = startCol - 1; j >= 1 && j <= maxCols ; j--) {
      if(values[i - 1][j - 1] === '') {
        break;
      }
      startCol = j;
      flag = true;
    }
    // Check for blank values in the right directorion
    for(var j = endCol + 1; j <= maxCols; j++) {
      if(values[i - 1][j - 1] === '') {
        break;
      }
      endCol = j;
      flag = true;
    }
  }

  // If the detected range changes, the function is called again
  if(flag) {
    return detectTableFromGivenRange(startRow, endRow, startCol, endCol, values, maxRows, maxCols);
  }
  // Else return the detected range from the function
  else {
    dataRange = [startRow, endRow, startCol, endCol];
    return dataRange;
  }
}

/**
 * Get the table selected by the user
 *
 * @return {Object} dataRange - The selected table range's details
 * @return {string} dateRange.rangeA1Notation - The A1Notation of the range selected
 * @return {number} dateRange.headerRow - The header row number of the range selected
 * @return {string} dateRange.headerRange - The header range of the range selected
 */
function getSelectedRange() {
  var sheet = SpreadsheetApp.getActiveSheet()
  var range = sheet.getActiveRange(); 

  // Storing A1Notation of selected range and first row of selected range as header
  var rangeA1Notation = range.getA1Notation(); 
  var headerRow = range.getRow();
  var headerRange = sheet.getRange(range.getRow(), range.getColumn(), 1, range.getWidth()).getA1Notation();
   
  var dataRange = {
     'rangeA1Notation': rangeA1Notation,
     'headerRow': headerRow,
     'headerRange': headerRange
  };
 
  // Getting the previous selected range
  var userProperties = PropertiesService.getUserProperties();
  var preSelectedRangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var preSelectedRange = sheet.getRange(preSelectedRangeA1Notation);
  
  // Start and end row, start and end column of the selected range
  var startRowNew = range.getRow();
  var endRowNew = range.getLastRow();
  var startColNew = range.getColumn();
  var endColNew = range.getLastColumn();
  
  // Start and end row, start and end column of the previous selected range
  var startRowOld = preSelectedRange.getRow();
  var endRowOld = preSelectedRange.getLastRow();
  var startColOld = preSelectedRange.getColumn();
  var endColOld = preSelectedRange.getLastColumn();
  
  // If the new selected range is subset of previous selected range 
  // use the previous selected header row
  if(startRowNew >= startRowOld && endRowNew <= endRowOld) {
    if(startColNew >= startColOld && endColNew <= endColOld) {
      dataRange.headerRow = userProperties.getProperty('headerRow');
      dataRange.headerRange = sheet.getRange(Number(dataRange.headerRow), 
                                             range.getColumn(), 
                                             1, 
                                             range.getWidth())
                                   .getA1Notation();
    }
  }

  Logger.log('Range selected by user');
  Logger.log(dataRange);

  return dataRange;
}

/**
 * Select the entire table as specifed in range received
 *
 * @param {string} tableA1Notation -  The A1Notation of the table to select
 * @return {Object} dataRange - The object containing table range's details
 * @return {string} dateRange.rangeA1Notation - The A1Notation of the range selected
 * @return {number} dateRange.headerRow - The header row number of the range selected 
 * @return {string} dateRange.headerRange - The header range of the range selected
 */
function selectEntireTable(tableA1Notation) {  
  var sheet = SpreadsheetApp.getActiveSheet()
  var table = sheet.getRange(tableA1Notation);
  var dataRange = {
    'rangeA1Notation': tableA1Notation,
    'headerRow': table.getRow(),
    'headerRange': sheet.getRange(table.getRow(), 
                                  table.getColumn(), 
                                  1, 
                                  table.getWidth())
                        .getA1Notation()
  };
  return dataRange;
}

/**
 * Update the range selected by user if it doesn't contain any error
 * Give error message in case of any invalid input
 *
 * @param {string} rangeA1Notation -  The A1Notation of range selected by user
 * @param {number} headerRow -  The header row of range selected by user
 * @param {string} headerRange -  The header range for the range selected by user
 *
 * @return {Object} updatedRange - The updated range details in case of success 
 *                                 and error details in case of invalid input
 * @return {boolean} updatedRange.success - Indicates validity of the range selected by user
 * @return {string} updatedRange.errorIn - The field containing error: headerRow / range 
 * @return {string} updatedRange.inputSheet - The name of the sheet containing selected range
 * @return {string} updatedRange.rangeA1Notation - The A1Notation of the selected range 
 * @return {number} updatedRange.headerRow - The header row number of the selected range 
 * @return {string} updatedRange.headerRange - The header range of the selected range
 * @return {string} updatedRange.entireTableRange - The A1Notation of the table range 
 *                                                  containing the selected range
 */
function setSelectedRange(rangeA1Notation, headerRow, headerRange) {
  var inputSheet = SpreadsheetApp.getActiveSheet();
  var range = inputSheet.getRange(rangeA1Notation);

  // Getting entire table containing the selected range
  var entireTable = detectTableFromGivenRange(range.getRow(),
                                              range.getLastRow(),
                                              range.getColumn(),
                                              range.getLastColumn(),
                                              inputSheet.getDataRange().getValues(),
                                              inputSheet.getDataRange().getLastRow(),
                                              inputSheet.getDataRange().getLastColumn());
  
  var updatedRange = {};
  // If header is in middle of the selected range, give an error message
  if(range.getRow() < headerRow) {
    updatedRange['success'] = false;
    updatedRange['errorIn'] = 'headerRow';
  }
  // Else if header is not at top of the table, give an error message
  else if( entireTable[0] !== headerRow && entireTable[0]+1 !== headerRow) {
    updatedRange['success'] = false;
    updatedRange['errorIn'] = 'headerRow';
  }
  // Else if the range selected has only 1 row, give an error message
  else if(range.getHeight()<2) {
    updatedRange['success'] = false;
    updatedRange['errorIn'] = 'range';
  }
  // Else all inputs are valid
  else {
    updatedRange['success'] = true;
    range.activate();
    
    updatedRange['inputSheet'] = inputSheet.getName();
    updatedRange['rangeA1Notation'] = rangeA1Notation;
    updatedRange['headerRow'] = headerRow;
    updatedRange['headerRange'] = headerRange;
    updatedRange['entireTableRange'] = inputSheet.getRange(entireTable[0], 
                                                           entireTable[2], 
                                                           entireTable[1] - entireTable[0] + 1, 
                                                           entireTable[3] - entireTable[2] + 1)
                                                 .getA1Notation();
    setUserProperties(updatedRange['inputSheet'], 
                      updatedRange['rangeA1Notation'],
                      updatedRange['headerRow'],
                      updatedRange['headerRange'],
                      updatedRange['entireTableRange']);
  }
  return updatedRange;
}

/**
 * Finds the column header names in the header row of table selected
 *
 * @return {Array} - The list of column header names
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
 * Gets the values present in range selected by user to use them as filter values
 *
 * @return {Array} - The list of values present in selected range
 */
function getFilterValues() {
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var values = range.getValues();
  return values;
}

/**
 * Set user properties to the values given
 *
 * @param {string} inputSheet - The name of sheet in which user selects data
 * @param {string} rangeA1Notation - The A1Notation of range selected
 * @param {number} headerRow - The header row of range selected
 * @param {string} headerRange - The header range for the range selected
 * @param {string} entireTableRange - The A1Notation of the table range containing the range selected
 */
function setUserProperties(inputSheet, rangeA1Notation, headerRow, headerRange, entireTableRange) {
   var userProperties = PropertiesService.getUserProperties();
   userProperties.setProperty('inputSheet',inputSheet);
   userProperties.setProperty('rangeA1Notation',rangeA1Notation);
   userProperties.setProperty('headerRow',headerRow);
   userProperties.setProperty('headerRange',headerRange);
   userProperties.setProperty('entireTableRange',entireTableRange);
}