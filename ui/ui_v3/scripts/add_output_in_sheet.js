// Functions for adding output in sheet

/**
 * Add the output result in a new sheet
 *
 * @param {Array} outputTable The output table of the query submitted 
 */
function addOutputInNewSheet(outputTable) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var userProperties = PropertiesService.getUserProperties();

  var inputSheet = userProperties.getProperty('inputSheet'); 
  var mainSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var mainSheetId = mainSheet.getSheetId();

  // Inserting a new sheet
  ss.insertSheet();   
  var insertedSheet = SpreadsheetApp.getActiveSheet();
  var insertedSheetId = insertedSheet.getSheetId();

  // Add the output in new inserted sheet  
  var dataRange = insertedSheet.getRange(1,1,outputTable.length,outputTable[0].length);
  dataRange.setValues(outputTable);
  
  // Apply formatting to the output table inserted
  applyFormattingToOutputTable(outputTable,mainSheet,mainSheetId,insertedSheet,insertedSheetId);
}

/**
 * Applies formatting to output header and data 
 *
 * @param {Array} outputTable The output table of the query submitted 
 * @param {Sheet} mainSheet The sheet containing the input table
 * @param {number} mainSheetId The id of sheet containing input table
 * @param {Sheet} insertedSheet The sheet in which output table is inserted
 * @param {number} insertedSheetId The id of the sheet in which output table is inserted
 */
function applyFormattingToOutputTable(outputTable,mainSheet,mainSheetId,insertedSheet,insertedSheetId) {
  var userProperties = PropertiesService.getUserProperties();
  
  // Format output table header 
  var headerRange = userProperties.getProperty('headerRange');
  var cells = findCellFormatForARange(headerRange,mainSheet,mainSheetId);
  cells = cells[0]['values'];
  var outputHeader = outputTable[0];

  for(var i = 0; i < cells.length; i++) {
    var cellValue = cells[i]['userEnteredValue']['stringValue'];
    var colIndex = outputHeader.indexOf(cellValue);
    
    if( colIndex !== -1) {
      var range = insertedSheet.getRange(1,colIndex+1);
      var cellFormatting = cells[i]['userEnteredFormat'];
      applyFormatting(range, cellFormatting, insertedSheetId);
    }
  }
  
  // Format output table data
  var rangeString = userProperties.getProperty('rangeString');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var dataRange = mainSheet.getRange(rangeString);
  var startRow = dataRange.getRow();
  var dataRangeString = dataRange.getA1Notation();
  if(startRow === headerRow) {
    startRow++;
    dataRangeString = mainSheet.getRange(startRow,
                                   dataRange.getColumn(),
                                   dataRange.getHeight()-1,
                                   dataRange.getWidth())
                               .getA1Notation();
  }
  // Find formatting for each data cell
  var cellsData = findCellFormatForARange(dataRangeString,mainSheet,mainSheetId);
  
  // Flag variable is used to indicate if each cell has same formartting
  // True indicates same formatting for all cells and False indicates different formatting
  var flag = true;
  var commonDataFormatting = cellsData[0]['values'][0]['userEnteredFormat'];
  for(var i = 0; i < cellsData.length; i++) {
    var cellsDataRow = cellsData[i]['values'];
    for(var j = 0; j < cellsDataRow.length; j++) {
      var cellFormatting = cellsDataRow[j]['userEnteredFormat'];
      if(!objectCompare(commonDataFormatting,cellFormatting)) {
        flag = false;
        break;
      }
    }
    if(!flag) {
      break;
    }
  }
  
  // Apply formatting to table cells if all cells have same formatting
  if(flag) {
    range = insertedSheet.getRange(2,1,outputTable.length-1,outputTable[0].length);
    applyFormatting(range, commonDataFormatting, insertedSheetId);
  }
}

/**
 * Get formatting of the given range
 *
 * @param {string} a1Rrange The range for which formatting is to be fetched
 * @param {Sheet} mainSheet The sheet containing the input table
 * @param {number} mainSheetId The id of sheet containing input table
 */
function findCellFormatForARange(a1Range,mainSheet,mainSheetId) {
  var sheetIndex = 0;
  var dataIndex = 0;
  var rowDataIndex = 0;
  
  var spreadSheetId = SpreadsheetApp.getActiveSpreadsheet().getId();
  var range = mainSheet.getRange(a1Range);
  
  var dataFilters = {
    'dataFilters': [
      {
        'gridRange': {
          'sheetId': mainSheetId,
          'startRowIndex': range.getRow()-1,
          'endRowIndex': range.getLastRow(),
          'startColumnIndex': range.getColumn()-1,
          'endColumnIndex': range.getLastColumn()
        }
      }
    ],
    'includeGridData': true
  };

  var sheet =  Sheets.Spreadsheets.getByDataFilter(dataFilters,spreadSheetId)['sheets'][sheetIndex];
  var cells = sheet['data'][dataIndex]['rowData'];
  return cells;
}

/**
 * Apply formatting to the given range
 *
 * @param {Range} range The range on which formatting has to be applied
 * @param {Object} cellFormatting The formatting to be applied
 * @param {number} insertedSheetId The id of the sheet in which output table is inserted
 */
function applyFormatting(range, cellFormatting, insertedSheetId) {
  var sheetId = SpreadsheetApp.getActiveSheet().getSheetId();
  var spreadSheetId = SpreadsheetApp.getActiveSpreadsheet().getId();

  var requestBody = {
    'requests': [
      {
        'repeatCell': {
          'range': {
            'sheetId': insertedSheetId,
            'startRowIndex': range.getRow()-1,
            'endRowIndex': range.getLastRow(),
            'startColumnIndex': range.getColumn()-1,
            'endColumnIndex': range.getLastColumn()
          },
          'cell': {
            'userEnteredFormat': cellFormatting
          },
          'fields': 'userEnteredFormat'
        }
      }
    ]
  }
  Sheets.Spreadsheets.batchUpdate(requestBody,spreadSheetId);
}

/**
 * Add the output result in a current sheet at selected location
 *
 * @param {string} outputCell The A1Notation of the output cell where output is to be inserted 
 * @param {Array} outputTable The output table of the query submitted 
 */
function addOutputInCurrentSheet(outputCell,outputTable) {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet); 
  var outputRange = sheet.getRange(outputCell);
  
  // Add the output in current sheet 
  var dataRange = sheet.getRange(outputRange.getRow(),
                                 outputRange.getColumn(),
                                 outputTable.length,
                                 outputTable[0].length);
  dataRange.setValues(outputTable);
  
//  //formatting output sheet's data
//  dataRange
//    .setFontFamily('Georgia')
//    .setFontSize('12')
//    .setBorder(true, true, true, true,true,null,null,SpreadsheetApp.BorderStyle.SOLID_MEDIUM);
// 
// //formatting output sheet's header
//  var headerRange = sheet.getRange(outputRange.getRow(), outputRange.getColumn(), 1, outputTable[0].length);
//  headerRange
//    .setFontWeight('bold')
//    .setFontColor('#ffffff')
//    .setBackgroundColor('#073763')
//    .setHorizontalAlignment('center');
  
}

/**
 * Compare 2 objects and check if they are equal
 * Used for comparing the cells formatting
 *
 * @param {Object} obj1 The first object to be compared
 * @param {Object} obj2 The second object to be compared
 * @return {boolean} true indictes the 2 objects are equal and false indicates unequal
 */
function objectCompare(obj1, obj2) {
  // Loop through properties in object 1
  for (var p in obj1) {
    // Check property exists on both objects
    if (obj1.hasOwnProperty(p) !== obj2.hasOwnProperty(p)) {
      return false;
    }

    switch (typeof (obj1[p])) {
      //Deep compare objects
      case 'object':
        if (!objectCompare(obj1[p], obj2[p])) {
          return false;
        }
        break;

      //Compare function code
      case 'function':
        if (typeof (obj2[p]) == 'undefined' || (p != 'compare' && obj1[p].toString() != obj2[p].toString())) {
          return false;
        }
        break;

      //Compare values
      default:
        if (obj1[p] != obj2[p]) {
          return false;
        }
    }
  }

  //Check object 2 for any extra properties
  for (var p in obj2) {
    if (typeof (obj1[p]) == 'undefined') {
      return false;
    }
  }
  return true;
};