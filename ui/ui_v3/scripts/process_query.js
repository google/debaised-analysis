// Functions for processing the query submitted by user

/*
 * Json object which contains values of aspects and table' data
 * TODO - Change of key names for :
 *        rowRange as tableMetaData
 *        k as limit
 *        Add keys dynamically
 *        Change return structure of comparisonValue
 * (to be done on gcp end for working of add-on)
 */
var jsonObj = {
  'intent': 'null',
  'table': 'null',
  'rowRange': 'null',
  'metric': 'null',
  'dimensions': 'null',
  'summaryOperator': 'null',
  'isAsc': 'null',
  'k': 'null',
  'slices': 'null',
  'dateRange': 'null',
  'timeGranularity': 'null',
  'comparisonValue': 'null' 
};

/**
 * Sends the query submitted by user to gcp and receives the output for it
 *
 * @param {string} intent The name of intent for which user has submitted query
 * @param {string} metric The name of metric column 
 * @param {string} summaryOperator The operation to apply on metric column
 * @param {boolean} isAsc The sort order of results in case of topk intent
 * @param {number} k The number of results to fetch in case of topk intent
 * @param {Array} dimensions The list of dimension columns
 *
 * @param {Object[]} slices The list of slices 
 * @param {string} slices[].sliceCol The name of slice column
 * @param {string} slices[].sliceOp The name of slice operation applied 
 * @param {(number|string|Array)} slices[].sliceVal The slice values for filtering
 *
 * @param {Object} dateRange The date range in which results are to be fetched
 * @param {string} dateRange.dateCol The date column containing dates used for filtering results
 * @param {string} dateRange.dateStart The start date (yyyy-mm-dd)
 * @param {string} dateRange.dateEnd The end date (yyyy-mm-dd) 
 *
 * @param {string} timeGranularity The time granularity value selected by the user
 * @param {Array} comparisonValue The comparison column and 2 values in it (one can be *)
 *                                to be compared in case of slice-compare intent
 *
 * @return {Object} queryResult The results of the query submitted 
 * @return {string} queryResult.jsonQuery The json for the submitted query
 * @return {Array} queryResult.outputTable The output table of the query submitted 
 * @return {Object[]} queryResult.suggestions The list of suggestions related to the submitted query
 */
function evalQuery(intent,metric,summaryOperator,isAsc,k,dimensions,slices,
                   dateRange,timeGranularity,comparisonValue) {
  /*
   * Set table and rowRange of jsonObj
   * jsonObj.table is a 2d array consisting of sheet's data
   * jsonObj.rowRange is an object with 3 keys: header, rowStart, rowEnd
   */
  getTable();

  jsonObj.intent = intent;

  jsonObj.metric = metric;
  jsonObj.summaryOperator = summaryOperator;
  jsonObj.isAsc = isAsc;
  jsonObj.k = k;

  if(dimensions.length > 0)
    jsonObj.dimensions = dimensions;

  if(slices.length > 0)
    jsonObj.slices = slices;

  if(dateRange !== 'null') {
    dateRange.dateStart = new Date(dateRange.dateStart);
    dateRange.dateEnd = new Date(dateRange.dateEnd);
    jsonObj.dateRange=dateRange;
  }
    
  jsonObj.timeGranularity = timeGranularity;
  jsonObj.comparisonValue = comparisonValue;

  // Logging jsonObj in json format
  Logger.log('jsonObj in json format');
  Logger.log(JSON.stringify(jsonObj));
  var jsonQuery = JSON.stringify(jsonObj);
  
  // Calling GCP function to obtain the query results
  var outputQuery = callGcpToGetQueryResult(JSON.stringify(jsonObj));
  var outputTable = outputQuery['outputTable'];
  var suggestions = outputQuery['suggestions'];
  Logger.log('output table ',outputTable);
  Logger.log('suggestions ',suggestions);

  // Sending the results to client side function to display results to the user
  var queryResult = {
    'jsonQuery': jsonQuery,
    'outputTable': outputTable,
    'suggestions': suggestions
  };
  return queryResult;
}

/**
 * Get the data of table selected by user and set keys: (rowRange and table) of jsonObj
 */
function getTable() {
  var userProperties = PropertiesService.getUserProperties();
  var rangeString = userProperties.getProperty('rangeString');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var inputSheet = userProperties.getProperty('inputSheet');
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var range = sheet.getRange(rangeString);

  var rowRangeObj = {
    'header': headerRow,
    'rowStart': range.getRow(),
    'rowEnd': range.getLastRow()
  };

  // If start row of data range and header row is same 
  // increment data range's start row by 1
  if(rowRangeObj.rowStart === rowRangeObj.header)
    rowRangeObj.rowStart = rowRangeObj.rowStart+1;

  // Set jsonObj.rowRange as object with 3 keys header, rowStart and rowEnd
  jsonObj.rowRange = rowRangeObj;

  // Selecting the entire table containing range selected by user 
  var dataRange = selectTable(range.getRow(),
                              range.getLastRow(),
                              range.getColumn(),
                              range.getLastColumn(),
                              sheet.getDataRange().getValues(),
                              sheet.getDataRange().getLastRow(),
                              sheet.getDataRange().getLastColumn());
  var table = sheet.getRange(dataRange[0],dataRange[2],dataRange[1]-dataRange[0]+1,dataRange[3]-dataRange[2]+1);

  // Set jsonObj.table as the table's contents
  jsonObj.table = table.getValues();
}

/**
 * Call the gcp function and fetch results
 *
 * @param {string} inputJson The json to be sent as input to gcp function
 * @return {Object} outputQuery The result of the query submitted 
 * @return {Array} outputQuery.outputTable The output table of the query submitted 
 * @return {Object[]} outputQuery.suggestions The list of suggestions related to the submitted query
 */
function callGcpToGetQueryResult(inputJson) {
  // Make a POST request with a JSON payload
  var options = {
    'method' : 'post',
    'contentType': 'application/json',
    'payload' : inputJson,
    'muteHttpExceptions' : true
  };
    
  // Makes a request to fetch data from a URL
  var response= UrlFetchApp.fetch(
                  'https://us-central1-mocha-interns.cloudfunctions.net/testfunction',
                  options);
  
  var responseCode = response.getResponseCode()
  var responseBody = response.getContentText()
  var outputQuery = {};

  // Code 200 indicates success
  if (responseCode === 200) {
    outputQuery = JSON.parse(responseBody); 
  } 
  // Else gcp function failed, give error message to user
  else {
    Logger.log(Utilities.formatString('Request failed. Expected 200, got %d: %s', responseCode, responseBody));
    outputQuery.outputTable = [['Your request failed']];
    outputQuery.suggestions = [];
  }
  return outputQuery;
}

/**
 * Sends the json for query to gcp and receives the output for it
 *
 * @param {string} jsonInput The json for the query to process
 * @return {Object} queryResult The results of the query submitted 
 * @return {string} queryResult.jsonQuery The json for the submitted query
 * @return {Array} queryResult.outputTable The output table of the query submitted 
 * @return {Object[]} queryResult.suggestions The list of suggestions related to the submitted query
 */
function callGcpToGetQueryResultUsingJson(jsonInput) {
  // Calling GCP function to obtain the query results
  var outputQuery = callGcpToGetQueryResult(jsonInput);
  var outputTable = outputQuery['outputTable'];
  var suggestions = outputQuery['suggestions'];
  Logger.log('output table ',outputTable);
  Logger.log('suggestions ',suggestions);

  // Sending the results to client side function to display results to the user
  var queryResult = {
    'jsonQuery': jsonInput,
    'outputTable': outputTable,
    'suggestions': suggestions
  };
  return queryResult;
}
