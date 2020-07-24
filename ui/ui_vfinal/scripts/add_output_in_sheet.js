// Functions for adding output in sheet with same formatting as input sheet

/**
 * Get formatting of the given range
 *
 * @param {string} a1Rrange - The range for which formatting is to be fetched
 * @param {Sheet} inputSheet - The sheet containing the input table
 * @param {number} inputSheetId - The id of sheet containing input table
 * @return {Object} cells - The information about each cells fetched from API 
 */
function findCellFormatForARange(a1Range, inputSheet, inputSheetId) {
  var sheetIndex = 0;
  var dataIndex = 0;
  
  var spreadSheetId = SpreadsheetApp.getActiveSpreadsheet().getId();
  var range = inputSheet.getRange(a1Range);
  var dataFilters = {
    'dataFilters': [
      {
        'gridRange': {
          'sheetId': inputSheetId,
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
 * @param {number} outputSheetId The id of the sheet in which output table is inserted
 */
function applyFormatting(range, cellFormatting, outputSheetId) {
  var spreadSheetId = SpreadsheetApp.getActiveSpreadsheet().getId();
  
  if(cellFormatting == null) {
    return;
  }
  if(cellFormatting.hasOwnProperty('numberFormat')) {
    delete cellFormatting.numberFormat;
  }
  var requestBody = {
    'requests': [
      {
        'repeatCell': {
          'range': {
            'sheetId': outputSheetId,
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
 * Compare 2 cellFormats  and check if they are equal
 *
 * @param {Object} cellFormat1 - The first object to be compared
 * @param {Object} cellFormat2 - The second object to be compared
 * @return {boolean} - True indictes the 2 formats are equal and false indicates unequal
 */
function compareFormatting(cellFormat1, cellFormat2) {
  if(cellFormat1 == null || cellFormat2 == null) {
    return false;
  }

  // Loop through properties in cellFormat1
  for (var p in cellFormat1) {
    // Check property exists in both objects
    if(p === 'numberFormat')
      continue;
    if (cellFormat1.hasOwnProperty(p) !== cellFormat2.hasOwnProperty(p)) {
      return false;
    }

    switch (typeof (cellFormat1[p])) {
      //Deep compare objects
      case 'object':
        if (!compareFormatting(cellFormat1[p], cellFormat2[p])) {
          return false;
        }
        break;

      //Compare function code
      case 'function':
        if (
          typeof (cellFormat2[p]) == 'undefined' || 
          (p != 'compare' && cellFormat1[p].toString() != cellFormat2[p].toString())
        ) {
          return false;
        }
        break;

      //Compare values
      default:
        if (cellFormat1[p] != cellFormat2[p]) {
          return false;
        }
    }
  }

  //Check cellFormat2 for any extra properties
  for (var p in cellFormat2) {
    if(p === 'numberFormat')
      continue;
    if (typeof (cellFormat1[p]) == 'undefined') {
      return false;
    }
  }
  return true;
};

/**
 * Check if all the cells in the range selected (except header row) have same formatting
 *
 * @param {string} inputSheet - The name of the sheet containing selected range
 * @param {string} rangeA1Notation -  The A1Notation of range selected by user
 * @param {number} headerRow -  The header row of range selected by user
 * @return {boolean} - True indictes all the cells have same formatting, false indicates different
 */
function checkTableCellsFormattingPattern(inputSheet, rangeA1Notation, headerRow) {
  var userProperties = PropertiesService.getUserProperties();
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet);
  var range = sheet.getRange(rangeA1Notation);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  var tableDataRange = sheet.getRange(startDataRow, 
                                      range.getColumn(), 
                                      range.getLastRow() - startDataRow +1, 
                                      range.getWidth())
                            .getA1Notation();
  var cellsData = findCellFormatForARange(tableDataRange,sheet,sheet.getSheetId());

  if(cellsData == null) {
    userProperties.setProperty('sameCellFormatting', false);
    return;
  }

  // Flag variable is used to indicate if each cell has same formartting
  // True indicates same formatting for all cells and False indicates different formatting
  var flag = true;
  var commonDataFormatting;
  if(cellsData[0].hasOwnProperty('values')) {
    if(cellsData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
      commonDataFormatting = cellsData[0]['values'][0]['userEnteredFormat'];
    }
    else {
      userProperties.setProperty('sameCellFormatting', false);
      return false;
    }
  } 
  else {
    userProperties.setProperty('sameCellFormatting', false);
    return false;
  }

  // Check if all cells have same formatting as the formatting of first table's cell
  for(var i = 0; i < cellsData.length; i++) {
    if(cellsData[i].hasOwnProperty('values')) {
      var cellsDataRow = cellsData[i]['values'];
      for(var j = 0; j < cellsDataRow.length; j++) {
        if(cellsDataRow[j].hasOwnProperty('userEnteredFormat')) {
          var cellFormatting = cellsDataRow[j]['userEnteredFormat'];
          if(!compareFormatting(commonDataFormatting,cellFormatting)) {
            flag = false;
            break;
          }
        }
        else {
          flag = false;
          break;
        }
      }
      if(!flag) {
        break;
      }  
    }
    else {
      flag = false;
      break;
    }
  }

  userProperties.setProperty('sameCellFormatting', flag);
  return flag;
}

/**
 * Check if all the header cells in the range selected have same formatting
 *
 * @param {string} headerRange - A1Notation of the header range 
 * @param {Sheet} inputSheet - The sheet containing the input table
 * @param {number} inputSheetId - The id of sheet containing input table
 * @return {boolean} - True indictes all the header cells have same formatting, false indicates different
 */
function checkSameHeaderFormatting(headerRange, inputSheet, inputSheetId) {
  var cells = findCellFormatForARange(headerRange, inputSheet, inputSheetId);
  if(cells != null) {
    if(cells[0].hasOwnProperty('values')) {
      cells = cells[0]['values'];
      var headerFormatting;
      if(cells[0].hasOwnProperty('userEnteredFormat')) {
        headerFormatting = cells[0]['userEnteredFormat'];
        for(var i = 0; i < cells.length; i++) {
          if(cells[i].hasOwnProperty('userEnteredFormat')) {
            var cellFormatting = cells[i]['userEnteredFormat'];
            if(!compareFormatting(headerFormatting,cellFormatting)) {
              return false;
            }
          }
          else {
            return false;
          }
        }
      }
      else {
        return false;
      }
    }
    else {
      return false;
    }
  }
  else {
    return false;
  }
  return true;
}

/**
 * Add the output result in a new sheet
 * @param {Array} outputTable - The output table of the query submitted 
 */
function addOutputInNewSheet(outputTable) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var userProperties = PropertiesService.getUserProperties();

  var inputSheetName = userProperties.getProperty('inputSheet'); 
  var inputSheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheetName);
  var inputSheetId = inputSheet.getSheetId();

  // Inserting a new sheet
  ss.insertSheet();
  var outputSheet = SpreadsheetApp.getActiveSheet();
  var outputSheetId = outputSheet.getSheetId();

  // Add the output in new inserted sheet  
  var dataRange = outputSheet.getRange(1, 1, outputTable.length, outputTable[0].length);
  dataRange.setValues(outputTable);
  
  // Apply formatting to the output table inserted
  applyFormattingInNewSheet(outputTable, inputSheet, inputSheetId, outputSheet, outputSheetId);
}

/**
 * Applies formatting to the output header and data inserted in new sheet
 *
 * @param {Array} outputTable - The output table of the query submitted 
 * @param {Sheet} inputSheet - The sheet containing the input table
 * @param {number} inputSheetId - The id of sheet containing input table
 * @param {Sheet} outputSheet - The sheet in which output table is inserted
 * @param {number} outputSheetId - The id of the sheet in which output table is inserted
 */
function applyFormattingInNewSheet(outputTable, inputSheet, inputSheetId, outputSheet, outputSheetId) {
  var userProperties = PropertiesService.getUserProperties();
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var headerRange = userProperties.getProperty('headerRange');
  var sameCellFormatting = userProperties.getProperty('sameCellFormatting');
  var range = inputSheet.getRange(rangeA1Notation);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  
  // Format output table header 
  if(checkSameHeaderFormatting(headerRange, inputSheet, inputSheetId)) {
    var headerStartCell = inputSheet.getRange(headerRow, range.getColumn()).getA1Notation();
    var cellsData = findCellFormatForARange(headerStartCell, inputSheet, inputSheetId);
    var headerFormatting;
    if(cellsData != null) {
      if(cellsData[0].hasOwnProperty('values')) {
        if(cellsData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          headerFormatting = cellsData[0]['values'][0]['userEnteredFormat'];
          var outputHeaderRange = outputSheet.getRange(1, 1, 1, outputTable[0].length);
          applyFormatting(outputHeaderRange, headerFormatting, outputSheetId);
        }
      }
    }
  }

  // Format output table data
  if(sameCellFormatting === 'true') {
    var startCell = inputSheet.getRange(startDataRow,range.getColumn()).getA1Notation();
    var cellData = findCellFormatForARange(startCell, inputSheet, inputSheetId);
    var commonDataFormatting;
    if(cellsData != null) {
      if(cellData[0].hasOwnProperty('values')) {
        if(cellData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          commonDataFormatting = cellData[0]['values'][0]['userEnteredFormat'];
          var formattingRange = outputSheet.getRange(2,1,outputTable.length-1,outputTable[0].length);
          applyFormatting(formattingRange, commonDataFormatting, outputSheetId);
        }
      } 
    }
  }
}

/**
 * Construct the slicing header of the column inserted in current sheet
 * @param {string} jsonQuery - The json of the submitted query to construct header
 */
function insertAsColumnHeader(jsonQuery) {
  var filterHeading = '';
  
  // Adding slice
  if(jsonQuery.hasOwnProperty('slices')) {
    filterHeading += ' where ';
    for(var i = 0; i < jsonQuery.slices.length; i++) {
      filterHeading += jsonQuery.slices[i].sliceCol + ' is ';
      filterHeading += jsonQuery.slices[i].sliceOp + ' ';
      if(jsonQuery.slices[i].sliceOp === 'In' || jsonQuery.slices[i].sliceOp === 'Not in') {
        var sliceVal = jsonQuery.slices[i].sliceVal;
        filterHeading += sliceVal[0];
        for(var j = 1; j < sliceVal.length; j++) {
          filterHeading += ', ' + sliceVal[j];
        }
      }
      else {
        filterHeading += jsonQuery.slices[i].sliceVal;
      }
      filterHeading += ', ';
    }
    filterHeading = filterHeading.slice(0,filterHeading.length - 2);
  }
  
  // Adding date range
  if(jsonQuery.hasOwnProperty('dateRange')) {
    filterHeading += ' from ';
    filterHeading += jsonQuery.dateRange.dateCol + ' ';
    filterHeading += jsonQuery.dateRange.dateStart + ' to ' + jsonQuery.dateRange.dateEnd;
  }
  return filterHeading;
}

/**
 * Add the column containing information about the entries passing filters
 *
 * @param {?Array} filtersPassed - The list of true-false values to insert output as column on filtering
 * @param {string} jsonQuery - Thejson of the submitted query to construct header of the inserted column
 * @param {number} insertAtColumn - The column at which we data is inserted
 * @param {string} lastTableRow - The last row of the table in which data is inserted
 */
function insertAsColumnSlicing(filtersPassed, jsonQuery, insertAtColumn, lastTableRow) {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var headerRange = userProperties.getProperty('headerRange');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var sameCellFormatting = userProperties.getProperty('sameCellFormatting');
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet); 
  var sheetId = sheet.getSheetId();
  var range = sheet.getRange(rangeA1Notation);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  jsonQuery = JSON.parse(jsonQuery);
  
  // Header: Setting header content and formatting
  var heading = 'Entries' + insertAsColumnHeader(jsonQuery);
  sheet.getRange(headerRow,insertAtColumn).setValue(heading);
  
  if(checkSameHeaderFormatting(headerRange, sheet, sheetId)) {
    var headerStartCell = sheet.getRange(headerRow, range.getColumn()).getA1Notation();
    var cellsData = findCellFormatForARange(headerStartCell, sheet, sheetId);
    var headerFormatting;
    if(cellsData != null) {
      if(cellsData[0].hasOwnProperty('values')) {
        if(cellsData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          headerFormatting = cellsData[0]['values'][0]['userEnteredFormat'];
          var headerCell = sheet.getRange(headerRow, insertAtColumn);
          applyFormatting(headerCell, headerFormatting, sheetId);
        }
      }
    }
  }
  
  // Data: Setting cells contents and formatting
  var filtersPassedValues = [];
  for(var i = 0; i < filtersPassed.length; i++) {
    filtersPassedValues.push([filtersPassed[i]]);
  }
  var dataRangeInserted = sheet.getRange(startDataRow, insertAtColumn, filtersPassedValues.length, 1);
  dataRangeInserted.setValues(filtersPassedValues);

  if(sameCellFormatting === 'true') {
    var startCell = sheet.getRange(startDataRow, range.getColumn()).getA1Notation();
    var cellData = findCellFormatForARange(startCell, sheet, sheetId);
    var commonDataFormatting;
    if(cellsData != null) {
      if(cellData[0].hasOwnProperty('values')) {
        if(cellData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          commonDataFormatting = cellData[0]['values'][0]['userEnteredFormat'];
          var formattingRange = sheet.getRange(headerRow+1, insertAtColumn, lastTableRow - headerRow);
          applyFormatting(formattingRange, commonDataFormatting, sheetId);
        }
      } 
    }
  }
}


/**
 * Add the column containing information about the entries that come under top-k
 *
 * @param {?Array} inTopK - The list of true-false values to insert output as column in top-k
 * @param {string} jsonQuery - Thejson of the submitted query to construct header of the inserted column
 * @param {number} insertAtColumn - The column at which we data is inserted
 * @param {string} lastTableRow - The last row of the table in which data is inserted
 */
function insertAsColumnTopK(inTopK, jsonQuery, insertAtColumn, lastTableRow) {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  var headerRange = userProperties.getProperty('headerRange');
  var headerRow = Number(userProperties.getProperty('headerRow'));
  var sameCellFormatting = userProperties.getProperty('sameCellFormatting');
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet); 
  var sheetId = sheet.getSheetId();
  var range = sheet.getRange(rangeA1Notation);
  var startDataRow = Math.max(range.getRow(),headerRow+1);
  jsonQuery = JSON.parse(jsonQuery);
  
  // Header: Setting header content and formatting
  var heading = 'Top-' + jsonQuery['topKLimit'] + ' entries with ';
  if(jsonQuery['isAsc'])
    heading += 'minimum ';
  else
    heading += 'maximum ';
  if(jsonQuery.hasOwnProperty('summaryOperator'))
    heading += jsonQuery['summaryOperation'] + ' of';
  heading += jsonQuery['metric'];
  heading += insertAsColumnHeader(jsonQuery);
  sheet.getRange(headerRow,insertAtColumn).setValue(heading);

  if(checkSameHeaderFormatting(headerRange, sheet, sheetId)) {
    var headerStartCell = sheet.getRange(headerRow, range.getColumn()).getA1Notation();
    var cellsData = findCellFormatForARange(headerStartCell, sheet, sheetId);
    var headerFormatting;
    if(cellsData != null) {
      if(cellsData[0].hasOwnProperty('values')) {
        if(cellsData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          headerFormatting = cellsData[0]['values'][0]['userEnteredFormat'];
          var headerCell = sheet.getRange(headerRow, insertAtColumn);
          applyFormatting(headerCell, headerFormatting, sheetId);
        }
      }
    }
  }
  
  // Data: Setting cells contents and formatting
  var inTopKValues = [];
  for(var i = 0; i < inTopK.length; i++) {
    inTopKValues.push([inTopK[i]]);
  }
  var dataRangeInserted = sheet.getRange(startDataRow, insertAtColumn, inTopKValues.length, 1);
  dataRangeInserted.setValues(inTopKValues);

  if(sameCellFormatting === 'true') {
    var startCell = sheet.getRange(startDataRow, range.getColumn()).getA1Notation();
    var cellData = findCellFormatForARange(startCell, sheet, sheetId);
    var commonDataFormatting;
    if(cellsData != null) {
      if(cellData[0].hasOwnProperty('values')) {
        if(cellData[0]['values'][0].hasOwnProperty('userEnteredFormat')) {
          commonDataFormatting = cellData[0]['values'][0]['userEnteredFormat'];
          var formattingRange = sheet.getRange(headerRow+1, insertAtColumn, lastTableRow - headerRow);
          applyFormatting(formattingRange, commonDataFormatting, sheetId);
        }
      }
    }
  } 
}

/**
 * Add the output result in a current sheet as column
 *
 * @param {?Array} filtersPassed - The list of true-false values to insert output as column on filtering
 * @param {?Array} inTopK - The list of true-false values to insert output as column in topk
 * @param {string} jsonQuery - Thejson of the submitted query to construct header of the inserted column
 */
function addOutputInCurrentSheet(filtersPassed, inTopK, jsonQuery) {
  var userProperties = PropertiesService.getUserProperties();
  var inputSheet = userProperties.getProperty('inputSheet');
  var rangeA1Notation = userProperties.getProperty('rangeA1Notation');
  
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(inputSheet); 
  var range = sheet.getRange(rangeA1Notation);
  
  var dataRange = detectTableFromGivenRange(range.getRow(),
                                            range.getLastRow(),
                                            range.getColumn(),
                                            range.getLastColumn(),
                                            sheet.getDataRange().getValues(),
                                            sheet.getDataRange().getLastRow(),
                                            sheet.getDataRange().getLastColumn());

  // Column number where we insert the data
  var column = dataRange[3]+1;
  if(filtersPassed !== null) {
    insertAsColumnSlicing(filtersPassed, jsonQuery, column, dataRange[1]);
    column++;
  }
  if(inTopK !== null) {
    insertAsColumnTopK(inTopK, jsonQuery, column, dataRange[1]);
  }
}
