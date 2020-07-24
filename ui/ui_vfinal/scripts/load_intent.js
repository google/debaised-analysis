// Functions for loading the selected page in sidebar

/**
 * onOpen trigger runs automatically when a user opens a spreadsheet
 * Add the launch option in add-on menu to run the add-on
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem('Launch','launchHelper')
    .addToUi();
}

/**
 * onInstall trigger runs automatically when a user installs add-on
 * Add the debiased analysis add-on in add-ons menu once user installs it
 */
function onInstall() {
 onOpen();
}

/**
 * Import css and javascript files content into the html file
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * Precompute table range and call the function to load the home page
 * Called when user selects launch from the add-on menu
 */
function launchHelper() {
  var userProperties = PropertiesService.getUserProperties();
  userProperties.deleteAllProperties();
  userProperties.setProperty('sameCellFormatting', 'false');
  userProperties.setProperty('dateColumnsList',JSON.stringify({}));
  preComputeTableRange();
  launch();
}

/**
 * Find the table range containing the range previously selected by user and 
 * call the function to load the home page
 * Called when user selects back option from the intent page
 */
function reloadHomePage() {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var sheetDataRange = sheet.getDataRange();
  var range = sheet.getRange(rangeA1Notation);

  // Getting start and end row, start and end column of the previous selected range by user
  var endRow = range.getLastRow();
  var startRow = range.getRow();
  var endCol = range.getLastColumn();
  var startCol = range.getColumn();
  var maxRows = sheetDataRange.getLastRow();
  var maxCols = sheetDataRange.getLastColumn();

  // Detecting the table containing the previous range selected by user
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
  userProperties.setProperty('entireTableRange',entireTableRange.getA1Notation());
  launch();
}

/**
 * Load the home page and send the detected table range
 */
function launch() {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var headerRow = userProperties.getProperty('headerRow');
  var headerRange = userProperties.getProperty('headerRange');
  var entireTableRange = userProperties.getProperty('entireTableRange');
  var autodetectedRange = [ 
    inputSheet, 
    rangeA1Notation,
    headerRow,
    headerRange, 
    entireTableRange
  ];
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var range = sheet.getRange(rangeA1Notation);
  // If the detected range has only 1 row, set it as none
  if(range.getRow() === range.getLastRow()) {
    autodetectedRange = 'none';
  }
  // Else highlight the selected table range
  else {
    range.activate();
  }

  var html = HtmlService.createTemplateFromFile('indexpage/html/index');
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.homeSidebarTitle);

  // Appending table range
  var autodetectedRangeDiv = '<div style="display: none;" id="autodetectedRange">' + autodetectedRange + '</div>';
  html.append(autodetectedRangeDiv);

  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for show intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function show() {
  var html = HtmlService.createTemplateFromFile('intents/show/show');
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.show.sidebarTitle);
              
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">show</div>';
  html.append(intentDiv);
              
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div id="headers" style="display: none;">' + headers + '</div>';
  html.append(headersDiv);
  
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for top-k intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function topK() {
  var html = HtmlService.createTemplateFromFile('intents/top_k/topk')
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.topK.sidebarTitle);
                 
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">topk</div>';
  html.append(intentDiv);
  
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
    
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for slice-compare intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function sliceCompare() {
  var html = HtmlService.createTemplateFromFile('intents/slice_compare/slicecompare')
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.sliceCompare.sidebarTitle);
               
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">slice-compare</div>';
  html.append(intentDiv);
  
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
    
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for time-compare intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function timeCompare() {
  var html = HtmlService.createTemplateFromFile('intents/time_compare/timecompare')
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.timeCompare.sidebarTitle);
               
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">time-compare</div>';
  html.append(intentDiv);
  
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
    
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for trend intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function trend() {
  var html = HtmlService.createTemplateFromFile('intents/trend/trend')
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.trend.sidebarTitle);
                
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">trend</div>';
  html.append(intentDiv);
  
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
    
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for correlation intent
 * Send the intent name, column headers list and information about the detected date columns 
 */
function correlation() {
  var html = HtmlService.createTemplateFromFile('intents/correlation/correlation')
  html.addOntext = addOnText;
  html = html.evaluate().setTitle(addOnText.intents.correlation.sidebarTitle);
                
  // Appending intent name
  var intentDiv = '<div id="intent-name" style="display: none;">correlation</div>';
  html.append(intentDiv);
  
  // Appending headers list
  var headers = getHeaders();
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
    
  // Appending date columns list
  var userProperties = PropertiesService.getUserProperties();
  var dateColumnsList = userProperties.getProperty('dateColumnsList');
  var dateDiv = '<div id="date-columns-list" style="display: none;">' + dateColumnsList + '</div>';
  html.append(dateDiv);
  
  SpreadsheetApp.getUi().showSidebar(html);
}