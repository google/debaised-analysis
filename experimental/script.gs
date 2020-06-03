
//onOpen trigger runs automatically when a user opens a spreadsheet
function onOpen(){
  var ui = SpreadsheetApp.getUi();
  ui.createAddonMenu()
    .addItem("Show","show")
    .addItem("Top-k","topK")
    .addItem("Trend","trend")
    .addSeparator()
    .addItem("Slice-Compare","sliceCompare")
    .addItem("Time-Compare","timeCompare")
    .addSeparator()
    .addItem("Growth","growth")
    .addToUi();
}

//onInstall trigger runs automatically when a user installs add-on
function onInstall(){
  ui.alert("Installed");
  onOpen();
}

//function invoked on clicking top-k from add-on menu bar
function topK(){
  var html = HtmlService.createTemplateFromFile('index').evaluate().setTitle("Top-K");
  SpreadsheetApp.getUi().showSidebar(html);
}

//function to import css.html and javascript.html file content into the index.html file
function include(filename) {
  return HtmlService.createHtmlOutputFromFile(filename).getContent();
}

//function to select the activated range from sheet
function getSelectedRange(){
  var range = SpreadsheetApp.getActiveSheet().getActiveRange(); 
  var rangeString = range.getA1Notation(); 
  return rangeString;
}

//funntion to find the index of a particular column in sheet
function colIndex(colName){
  var sheet=SpreadsheetApp.getActiveSheet();
  var data = sheet.getDataRange();
  //assuming header are on first row
  var headers=sheet.getRange(1,1,1,data.getLastColumn()).getValues();
  for(var i=0;i<headers[0].length;i++){
    if(headers[0][i]==colName){
      //return column number of the given column name
      return i+1;
    }
  }
  //return -1 indicating column name was not found
  return -1;
}