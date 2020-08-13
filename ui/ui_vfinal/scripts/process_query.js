// Functions for processing the query submitted by user

/**
 * Sends the query submitted by user to gcp and receives the output for it
 *
 * @param {string} intent - The name of intent for which user has submitted query
 * @param {?string} metric - The name of metric column 
 * @param {?string} summaryOperator - The operation to apply on metric column
 * @param {boolean} isAsc - The sort order of results in case of topk intent
 * @param {number} topKLimit - The number of results to fetch in case of topk intent
 * @param {Array} dimensions - The list of dimension columns
 *
 * @param {Object[]} slices - The list of slices 
 * @param {string} slices[].sliceCol - The name of slice column
 * @param {string} slices[].sliceOp - The name of slice operation applied 
 * @param {(number|string|boolean|Array)} slices[].sliceVal - The slice values for filtering
 *
 * @param {?Object} dateRange - The date range in which results are to be fetched
 * @param {string} dateRange.dateCol - The date column containing dates used for filtering results
 * @param {string} dateRange.dateStart - The start date (yyyy-mm-dd)
 * @param {string} dateRange.dateEnd - The end date (yyyy-mm-dd) 
 *
 * @param {?string} timeGranularity - The time granularity value selected by the user
 *
 * @param {?Object} comparisonValue - Values to be compared for slice-compare intent
 * @paran {string} comparisonValue.comparisonColumn - The comparison column which contains values to comapre
 * @param {string} comparisonValue.slice1 - The first value to be compared 
 * @param {string} comparisonValue.slice2 - The second value to be compared (can be *)
 *
 * @param {?Object} compareDateRange - Date ranges to be compared for time-compare intent
 * @paran {string} compareDateRange.dateCol - The date column which contains date ranges to comapre
 * @param {string} compareDateRange.dateStart1 - The start date of first date-range
 * @param {string} compareDateRange.dateEnd1 - The end date of first date-range
 * @param {string} compareDateRange.dateStart2 - The start date of second date-range
 * @param {string} compareDateRange.dateEnd2- The end date of second date-range
 *
 * @param {?Object} correlationMetrics - The metrics for correlation intent
 * @param {string} correlationMetrics.metric1 - The first metric used to apply correlation
 * @param {string} correlationMetrics.metric2 - The second metric used to apply correlation
 *
 * @param {Object} dateColumnsList - The object containing information about the date columns
 * @param {string} dateColumnsList.dateColumnName.type - The type of date column 
 * @param {boolean} dateColumnsList.dateColumnName.day_first - The format of date column
 * @param {string} dateColumnsList.dateColumnName.min_date - The minimum date in specified date column
 * @param {string} dateColumnsList.dateColumnName.max_date - The maximum date in specified date column
 *
 * @return {Object} queryResult - The results of the query submitted 
 * @return {string} queryResult.status - Indicates whether gcp function returned results successfully
 * @return {string} queryResult.jsonQuery - The json for the submitted query
 * @return {Array} queryResult.outputTable - The output table of the query submitted 
 * @return {Object[]} queryResult.suggestions - The list of suggestions related to the submitted query
 * @return {?Array} queryResult.filtersPassed - The list of true-false values to insert output as column on filtering
 * @return {?Array} queryResult.inTopK -  The list of true-false values to insert output as column in topk
 */
function evalQuery(
    intent, 
    metric, 
    summaryOperator, 
    isAsc, 
    topKLimit, 
    dimensions, 
    slices,
    dateRange, 
    timeGranularity, 
    comparisonValue, 
    compareDateRange, 
    correlationMetrics, 
    dateColumnInfo) {

  // Json object which contains values of aspects and table' data
  var jsonObj = {};
  
  /*
   * Set table key fot jsonObj
   * jsonObj.table is a 2d array containing the selected table's data
   */
  jsonObj.table = getTableData();

  jsonObj.intent = intent;

  var userProperties = PropertiesService.getUserProperties();
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');

  jsonObj.rangeA1Notation = rangeA1Notation;

  if(metric !== null) {
    jsonObj.metric = metric;
  }

  if(summaryOperator !== null) {
    jsonObj.summaryOperator =summaryOperator;
  }

  jsonObj.isAsc = isAsc;

  jsonObj.topKLimit = topKLimit;

  if(dimensions.length > 0)
    jsonObj.dimensions = dimensions;

  if(slices.length > 0)
    jsonObj.slices = slices;

  if(dateRange !== null) {
    jsonObj.dateRange = dateRange;
  }

  if(timeGranularity !== null) {
    jsonObj.timeGranularity = timeGranularity;
  }

  if(comparisonValue !== null) {
    jsonObj.comparisonValue = comparisonValue;
  }

  if(compareDateRange !== null) {
    jsonObj.compareDateRange = compareDateRange;
  }

  if(correlationMetrics !== null) {
    jsonObj.correlationMetrics = correlationMetrics;
  }
  
  jsonObj.dateColumns = dateColumnInfo;
  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperty('dateColumnsList', JSON.stringify(dateColumnInfo));

  // Calling GCP function to obtain the query results
  var queryResult = callGcpToGetQueryResult(JSON.stringify(jsonObj));
  Logger.log('queryResult received form gcp function', queryResult);
  return queryResult;
}

/**
 * Get the sheet's data of range selected by user
 * @return {Array} table - 2D array containing sheet's data for the selected range
 */
function getTableData() {
  var userProperties = PropertiesService.getUserProperties();
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var inputSheet = userProperties.getProperty('inputSheet');
  var entireTableRange = userProperties.getProperty('entireTableRange');
  var dateColumnsList = JSON.parse(userProperties.getProperty('dateColumnsList'));
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var range = sheet.getRange(rangeA1Notation);
  var entireTable = sheet.getRange(entireTableRange);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  
  // Getting the selected range's data
  var tableHeader = sheet.getRange(headerRow, entireTable.getColumn(), 1, entireTable.getWidth())
                         .getValues();
  var tableData = sheet.getRange(startDataRow, 
                                 entireTable.getColumn(), 
                                 range.getLastRow() - startDataRow +1, 
                                 entireTable.getWidth())
                       .getValues();
  var tableRawData = sheet.getRange(startDataRow, 
                                    entireTable.getColumn(), 
                                    range.getLastRow() - startDataRow +1, 
                                    entireTable.getWidth())
                          .getDisplayValues();
  var dateColumnNames = Object.keys(dateColumnsList);
  for(var i = 0; i < tableHeader[0].length; i++) {
    if(dateColumnNames.indexOf(tableHeader[0][i]) !== -1) {
      for(var j=0; j < tableData.length; j++) {
        tableData[j][i] = tableRawData[j][i];
      }
    }
  }
  
  var table = tableHeader.concat(tableData);
  return table;
}

/**
 * Call the gcp function and fetch results
 *
 * @param {string} inputJson - The json to be sent as input to gcp function
 * @return {Object} queryResult - The results of the query submitted 
 * @return {string} queryResult.status - Indicates whether gcp function returned results successfully
 * @return {string} queryResult.jsonQuery - The json for the submitted query
 * @return {Array} queryResult.outputTable - The output table of the query submitted 
 * @return {Object[]} queryResult.suggestions - The list of suggestions related to the submitted query
 * @return {?Array} queryResult.filtersPassed - The list of true-false values to insert output as column on filtering
 * @return {?Array} queryResult.inTopK -  The list of true-false values to insert output as column in topk
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
  var resultValid = true;
  var queryResult;

  // Code 200 indicates success
  if (responseCode === 200) {    
    var jsonVerify = checkJsonValidity(responseBody);
    resultValid = jsonVerify;
    if(jsonVerify) {
      var outputQuery = JSON.parse(responseBody); 
      if('outputTable' in outputQuery && 'suggestions' in outputQuery) {
        // Storing fields for insert as column
        var filtersPassed = null;
        var inTopK = null;
        if('slicing_passed_list' in outputQuery)
          filtersPassed = outputQuery['slicing_passed_list'];
        if('list_topk_indices' in outputQuery)
          inTopK = outputQuery['list_topk_indices'];
    
        // Storing the received results
        var resultObj = {
          'status': 'success',
          'jsonQuery': inputJson,
          'outputTable': outputQuery['outputTable'],
          'suggestions': outputQuery['suggestions'],
          'filtersPassed': filtersPassed,
          'inTopK': inTopK
        };
        queryResult = resultObj;
      }
      else {
        resultValid = false;
      }
    }
  } 
  else {
    resultValid = false;
  }
  
  // If there is error in the returned result, give error message to user
  if(!resultValid) {
    var resultObj = {
      'status': 'fail',
      'jsonQuery': inputJson,
      'outputTable': [[]],
      'suggestions': [],
      'filtersPassed': null,
      'inTopK': null
    };
    queryResult = resultObj;
  }
  return queryResult;
}

/**
 * Check the json's validity
 * @param {string} text- The json to be verified
 * @return {boolean} - True indicates valid json and false invalid
 */
function checkJsonValidity(text) { 
  if (typeof text !== 'string') { 
    return false; 
  } 
  try { 
    JSON.parse(text); 
    return true; 
  } 
  catch (error) { 
    return false; 
  } 
}  