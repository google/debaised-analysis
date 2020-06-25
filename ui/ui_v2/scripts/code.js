
//onOpen trigger runs automatically when a user opens a spreadsheet
//TODO - once entire functionality is set up remove intent calls from add on menu
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem('Launch','launch')
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

//onInstall trigger runs automatically when a user installs add-on
function onInstall() {
  ui.alert('Installed');
  onOpen();
}

//function to import css and javascript files into the html file
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

// function to call the index/home page
function launch() {

  var userProperties = PropertiesService.getUserProperties();
  //delete user properties already present
  userProperties.deleteAllProperties();

  //function call to autodetect table
  autoDetectTable();

  Logger.log("auto detected values");
  Logger.log(userProperties.getProperties());

  //load page for index/home page
  var html = HtmlService
                .createTemplateFromFile('indexpage/html/index')
                .evaluate()
                .setTitle('Home Page');
  SpreadsheetApp.getUi().showSidebar(html);

}

//function to run queries using their json values
function testFunction() {

  var html = HtmlService
              .createTemplateFromFile('test/json_input')
              .evaluate()
              .setTitle('Test Page');
  SpreadsheetApp.getUi().showSidebar(html);

}

//function invoked on clicking show from add-on menu bar
function show() {

  var html = HtmlService
              .createTemplateFromFile('intents/html/show')
              .evaluate()
              .setTitle('Show');
  SpreadsheetApp.getUi().showSidebar(html);
}

//function invoked on clicking top-k from add-on menu bar
function topK() {
  
  Logger.log("topk script func");
  var html = HtmlService
              .createTemplateFromFile('intents/html/topk')
              .evaluate()
              .setTitle('Top-K');
  SpreadsheetApp.getUi().showSidebar(html);
}

function trend(){
  SpreadsheetApp.getUi().alert("trend intent");
}

function sliceCompare(){
  SpreadsheetApp.getUi().alert("slice-compare intent");
}

function timeCompare(){
  SpreadsheetApp.getUi().alert("time compare intent");
}

function Growth(){
  SpreadsheetApp.getUi().alert("growth intent");
}

//function to autodetermine table's range
function autoDetectTable() {

  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getDataRange();
  var rangeActive = sheet.getActiveRange();

  var rowEnd = rangeActive.getLastRow();
  var rowStart = rangeActive.getRow();
  var colEnd = rangeActive.getLastColumn();
  var colStart = rangeActive.getColumn();
  var maxRows = range.getLastRow();
  var maxCols = range.getLastColumn();

  Logger.log("Range of the selected cells");
  Logger.log(rowStart,rowEnd,colStart,colEnd);

  var dataRange =  selectTable(rowStart,rowEnd,colStart,colEnd,range.getValues(),maxRows,maxCols);
  Logger.log("Range of the detected table");
  Logger.log(dataRange);

  var rangeTable = sheet.getRange(dataRange[0],dataRange[2],dataRange[1]-dataRange[0]+1,dataRange[3]-dataRange[2]+1);
  var rangeString = rangeTable.getA1Notation();
  var headerRow = dataRange[0];
  //var headers = sheet.getRange(dataRange[0],dataRange[2],1,dataRange[3]-dataRange[2]+1).getValues();
  //headers = headers[0];

  var dataRange = {
   'rangeString': rangeString,
   'headerRow': headerRow
  }

  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperties(dataRange);

  Logger.log("Range String and Header Row detected in autoDetectTable()");
  Logger.log(userProperties.getProperties());
  
  //highlight the detected table
  rangeTable.activate();

}

// function that runs control-a logic on the selected cells
function selectTable(rowStart,rowEnd,colStart,colEnd,values,maxRows,maxCols) {
  
  var flag = false;

  for(var j = colStart; j <= colEnd && j <= maxCols; j++) {

    // check for blank values in up directorion
    for(var i = rowStart-1; i >= 1 && i <= maxRows; i--){
      if(values[i-1][j-1] == "")
        break;
      rowStart = i;
      flag=true;
    }
    // check for blank values in down directorion
    for(var i = rowEnd+1; i <= maxRows; i++){
      if(values[i-1][j-1] == "")
        break;
      rowEnd = i;
      flag=true;
    }

  }

  for(var i = rowStart; i <= rowEnd && i <= maxRows; i++) {

    // check for blank values in left directorion
    for(var j = colStart - 1; j >= 1 && j <= maxCols ; j--){
      if(values[i-1][j-1] == "")
        break;
      colStart = j;
      flag=true;
    }
    // check for blank values in right directorion
    for(var j = colEnd + 1; j <= maxCols; j++){
      if(values[i-1][j-1] == "")
        break;
      colEnd = j;
      flag=true;
    }

  }
  
  // if the selected range values are altered we call the function again
  // else we return from the function
  if(flag) {
    return selectTable(rowStart,rowEnd,colStart,colEnd,values,maxRows,maxCols);
  }
  else {
    dataRange = [rowStart,rowEnd,colStart,colEnd];
    return dataRange;
  }
  
}

// Function called by index/home page to fetch range and header
function prefillDataRange() {

  var userProperties = PropertiesService.getUserProperties();
  Logger.log("pre filled data range sent to index page");
  Logger.log(userProperties.getProperties());
  return (userProperties.getProperties());

}

//function to select the activated range from sheet
function getSelectedRange() {

  var sheet = SpreadsheetApp.getActiveSheet()
  var range = sheet.getActiveRange(); 

  var rangeString = range.getA1Notation(); 
  var headerRow = range.getRow();
  //var headers = sheet.getRange(headerRow,range.getColumn(),1,range.getWidth()).getValues();
   
  var dataRange = {
     'rangeString': rangeString,
     'headerRow': headerRow
  }
  
  Logger.log("Range selected by user");
  Logger.log(dataRange);

  return dataRange;
}

//function to highlight range selected by user and update range and header values
function highlightSelectedRange(rangeString,headerRow){

  var range = SpreadsheetApp.getActiveSheet().getRange(rangeString);
  range.activate();

  var userProperties = PropertiesService.getUserProperties();
  userProperties.setProperty('rangeString',rangeString);
  userProperties.setProperty('headerRow',headerRow);
  Logger.log("updated range");
  Logger.log(userProperties.getProperties());

}

//function to select filter values from sheet
function getFilterValues() {
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var values = range.getValues();
  return values;
}

//function to fetch column header names from header row
function getHeaders(){
  
  var userProperties = PropertiesService.getUserProperties();
  var rangeString = userProperties.getProperty('rangeString');
  var headerRow = Number(userProperties.getProperty('headerRow'));

  var sheet = SpreadsheetApp.getActiveSheet();
  var range = sheet.getRange(rangeString);

  var headers = sheet.getRange(headerRow,range.getColumn(),1,range.getWidth()).getValues();
  headers = headers[0];
  Logger.log("header row for table selected");
  Logger.log(headers);
  return headers;
}

