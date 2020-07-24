// Functions for date detection: getting the list of date columns, their type and formats

/**
 * Set the user property: dateColumnsList to the value given
 *
 * @param {Object} dateColumnsList - The object containing information about the date columns
 * @param {string} dateColumnsList.dateColumnName.type - The type of date column 
 *                                                       (consistent/inconsistent/ambiguous)
 * @param {boolean} dateColumnsList.dateColumnName.day_first - The format of date column
 * @param {string} dateColumnsList.dateColumnName.min_date - The minimum date in specified date column
 * @param {string} dateColumnsList.dateColumnName.max_date - The maximum date in specified date column
 */
function setDateColumnsList(dateColumnsList) {
   var userProperties = PropertiesService.getUserProperties();
   userProperties.setProperty('dateColumnsList', JSON.stringify(dateColumnsList));
}

/**
 * Detect the date columns in the range selected by the user
 *
 * @param {string} rangeA1Notation -  The A1Notation of range selected by user
 * @param {number} headerRow -  The header row of range selected by user
 * @param {string} inputSheet - The name of the sheet containing selected range
 * @param {string} entireTableRange - The A1Notation of the table range containing the selected range
 *
 * @return {Object} dateColumnsList - The object containing information about the date columns
 * @return {string} dateColumnsList.dateColumnName.type - The type of date column 
 *                                                        (consistent/inconsistent/ambiguous)
 * @return {boolean} dateColumnsList.dateColumnName.day_first - The format of date column
 * @return {string} dateColumnsList.dateColumnName.min_date - The minimum date in specified date column
 * @return {string} dateColumnsList.dateColumnName.max_date - The maximum date in specified date column
 */
function detectDate(rangeA1Notation, headerRow, inputSheet, entireTableRange) {  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var range = sheet.getRange(rangeA1Notation);
  var entireTable = sheet.getRange(entireTableRange);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  
  // Getting the selected range's data
  var tableHeader = sheet.getRange(headerRow, entireTable.getColumn(), 1, entireTable.getWidth()).getDisplayValues();
  var tableData = sheet.getRange(startDataRow, 
                                 entireTable.getColumn(), 
                                 range.getLastRow() - startDataRow +1, 
                                 entireTable.getWidth())
                       .getDisplayValues();
  var table = tableHeader.concat(tableData);
  
  // Calling the gcp function to receive information about date columns in given data
  var dateColumnsList = callGcpToDetectDate(table);
  setDateColumnsList(dateColumnsList);
  return dateColumnsList;
}

/**
 * Sending the table's data and receiving results about the detected date columns in table
 *
 * @param {Array} table - 2D array containing sheet's data for the selected range
 *
 * @return {Object} dateColumnsList - The object containing information about the date columns
 * @return {string} dateColumnsList.dateColumnName.type - The type of date column 
 *                                                        (consistent/inconsistent/ambiguous)
 * @return {boolean} dateColumnsList.dateColumnName.day_first - The format of date column
 * @return {string} dateColumnsList.dateColumnName.min_date - The minimum date in specified date column
 * @return {string} dateColumnsList.dateColumnName.max_date - The maximum date in specified date column
 */
function callGcpToDetectDate(table) {
  // Make a POST request with a JSON payload
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : JSON.stringify(table),
    'muteHttpExceptions' : true
  };
    
  // Makes a request to fetch data from a URL
  var response= UrlFetchApp.fetch(
                  'https://us-central1-mocha-interns.cloudfunctions.net/detect_datetime',
                  options);
  
  var responseCode = response.getResponseCode()
  var responseBody = response.getContentText()
  var dateColumnsList = {};

  // Code 200 indicates success
  if (responseCode === 200) {
    if(checkJsonValidity(responseBody)) {
      dateColumnsList = JSON.parse(responseBody); 
    }
  }
  return dateColumnsList;
}