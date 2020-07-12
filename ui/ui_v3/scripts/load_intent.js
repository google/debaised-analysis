// Functions for loading the selected page in sidebar

/**
 * onOpen trigger runs automatically when a user opens a spreadsheet
 * TODO - Once entire functionality is set up remove intent calls from add on menu
 * 
 * Add the launch option in add-on menu to run the add-on
 */
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem('Launch','launchHelper')
    .addSeparator()
    .addItem('Test Query','testFunction')
    .addSeparator()
    .addItem('Show','show')
    .addItem('Top-k','topK')
    .addItem('Trend','trend')
    .addSeparator()
    .addItem('Slice-Compare','sliceCompare')
    .addItem('Time-Compare','timeCompare')
    .addSeparator()
    .addItem('Growth','growth')
    .addToUi();
}

/**
 * onInstall trigger runs automatically when a user installs add-on
 * Add the add-on in add-on menu once user installs it
 */
function onInstall() {
  ui.alert('Installed');
  onOpen();
}

/**
 * Import css and javascript files content into the html file
 */
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

/**
 * Autodetect table range and call function to load the home page
 * Called when user selects launch from the add-on menu
 */
function launchHelper() {
  var userProperties = PropertiesService.getUserProperties();
  userProperties.deleteAllProperties();
  autoDetectTable();
  launch();
}

/**
 * Load the home page and send the detected table range
 */
function launch() {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var rangeString = userProperties.getProperty('rangeString');
  var headerRow = userProperties.getProperty('headerRow');
  var headerRange = userProperties.getProperty('headerRange');
  var autodetectedRange = [inputSheet, rangeString, headerRow, headerRange];
  
  // Highlight the selected table range
  var rangeTable = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet).getRange(rangeString);
  rangeTable.activate();

  var html = HtmlService
                .createTemplateFromFile('indexpage/html/index')
                .evaluate()
                .setTitle('Home Page');

  // Appending table range
  var autodetectedRangeDiv = '<div style="display: none;" id="autodetectedRange">' + autodetectedRange + '</div>';
  html.append(autodetectedRangeDiv);
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Run queries using their json (for testing purposes)
 */
function testFunction() {
  var html = HtmlService
              .createTemplateFromFile('test_query/json_input')
              .evaluate()
              .setTitle('Test Page');
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for show intent and send the column headers list
 */
function show() {
  var headers = getHeaders();
  var html = HtmlService
              .createTemplateFromFile('intents/show/show')
              .evaluate()
              .setTitle('Show');
  // Appending headers list
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for top-k intent and send the column headers list
 */
function topK() {
  var headers = getHeaders();
  var html = HtmlService
              .createTemplateFromFile('intents/top_k/topk')
              .evaluate()
              .setTitle('Top-K');
  // Appending headers list
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for slice-compare intent and send the column headers list
 */
function sliceCompare() {
  var headers = getHeaders();
  var html = HtmlService
              .createTemplateFromFile('intents/slice_compare/slicecompare')
              .evaluate()
              .setTitle('Slice-Compare');
  // Appending headers list
  var headersDiv = '<div style="display: none;" id="headers">' + headers + '</div>';
  html.append(headersDiv);
  SpreadsheetApp.getUi().showSidebar(html);
}

/**
 * Load page for trend intent - to be added
 */
function trend() {
  SpreadsheetApp.getUi().alert('trend intent');
}

/**
 * Load page for time-compare intent - to be added
 */
function timeCompare() {
  SpreadsheetApp.getUi().alert('time compare intent');
}

/**
 * Load page for growth intent - to be added
 */
function growth() {
  SpreadsheetApp.getUi().alert('growth intent');
}