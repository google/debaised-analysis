
//onOpen trigger runs automatically when a user opens a spreadsheet
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
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

//function invoked on clicking show from add-on menu bar
function show() {
  var html= HtmlService
              .createTemplateFromFile('html/intents/show')
              .evaluate()
              .setTitle('Show');
  SpreadsheetApp.getUi().showSidebar(html);
}

//function invoked on clicking top-k from add-on menu bar
function topK() {
  var html= HtmlService
              .createTemplateFromFile('html/intents/topk')
              .evaluate()
              .setTitle('Top-K');
  SpreadsheetApp.getUi().showSidebar(html);
}

//function to import css and javascript files into the html file
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

//function to select the activated range from sheet
function getSelectedRange() {
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var rangeString = range.getA1Notation(); 
  //selecting first row from the range selected as header row
  var headerRow = range.getLastRow() - range.getHeight()+1;
  var tableRange = [rangeString,headerRow];
  return tableRange;
}

//function to select filter values from sheet
function getFilterValues() {
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var values = range.getValues();
  return values;
}

//function to autodetermine table's range
function autoDetectTable() {
   var sheet = SpreadsheetApp.getActiveSheet();
   var range=sheet.getDataRange();
   var rangeString = range.getA1Notation();
   return rangeString;
}
