// Tests relared to query processing

/**
 * Master test function for query processing
 */
function testQueryProcessingFunctions() {
  testEvalQueryShow();
  testEvalQueryTopK();
  testEvalQuerySliceCompare();

  testGetTable();

  testCallGcpToGetQueryResultShow();
  testCallGcpToGetQueryResultTopK(); 
  testCallGcpToGetQueryResultSliceCompare();

  testCallGcpToGetQueryResultUsingJsonShow();
  testCallGcpToGetQueryResultUsingJsonTopK(); 
  testCallGcpToGetQueryResultUsingJsonSliceCompare();
}

/**
 * Show intent
 * Query: Show Sum of Units for Item, Region where Region is In West,East
 */
var jsonQueryShow = 
  '{"intent":"show",' +
   '"table":[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
            '["2019-01-05T18:30:00.000Z","East","Jones","Pencil",95,1.99,189.05],' +
            '["2019-01-22T18:30:00.000Z","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
            '["2019-02-08T18:30:00.000Z","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
            '["2019-02-25T18:30:00.000Z","Central","Gill","Pen",27,19.99,539.7299999999999],' +
            '["2019-03-14T18:30:00.000Z","West","Sorvino","Pencil",56,2.99,167.44],' +
            '["2019-03-31T18:30:00.000Z","East","Jones","Binder",60,4.99,299.40000000000003],' +
            '["2019-04-17T18:30:00.000Z","Central","Andrews","Pencil",75,1.99,149.25],' +
            '["2019-05-04T18:30:00.000Z","Central","Jardine","Pencil",90,4.99,449.1],' +
            '["2019-05-21T18:30:00.000Z","West","Thompson","Pencil",32,1.99,63.68],' +
            '["2019-06-07T18:30:00.000Z","East","Jones","Binder",60,8.99,539.4],' +
            '["2019-06-24T18:30:00.000Z","Central","Morgan","Pencil",90,4.99,449.1],' +
            '["2019-07-11T18:30:00.000Z","East","Howard","Binder",29,1.99,57.71],' +
            '["2019-07-28T18:30:00.000Z","East","Parent","Binder",81,19.99,1619.1899999999998],' +
            '["2019-08-14T18:30:00.000Z","East","Jones","Pencil",35,4.99,174.65],' +
            '["2019-08-31T18:30:00.000Z","Central","Smith","Desk",2,125,250],' +
            '["2019-09-17T18:30:00.000Z","East","Jones","Pen Set",16,15.99,255.84],' +
            '["2019-10-04T18:30:00.000Z","Central","Morgan","Binder",28,8.99,251.72],' +
            '["2019-10-21T18:30:00.000Z","East","Jones","Pen",64,8.99,575.36],' +
            '["2019-11-07T18:30:00.000Z","East","Parent","Pen",15,19.99,299.84999999999997],' +
            '["2019-11-24T18:30:00.000Z","Central","Kivell","Pen Set",96,4.99,479.04],' +
            '["2019-12-11T18:30:00.000Z","Central","Smith","Pencil",67,1.29,86.43],' +
            '["2019-12-28T18:30:00.000Z","East","Parent","Pen Set",74,15.99,1183.26],' +
            '["2020-01-14T18:30:00.000Z","Central","Gill","Binder",46,8.99,413.54],' +
            '["2020-01-31T18:30:00.000Z","Central","Smith","Binder",87,15,1305],' +
            '["2020-02-17T18:30:00.000Z","East","Jones","Binder",4,4.99,19.96],' +
            '["2020-03-06T18:30:00.000Z","West","Sorvino","Binder",7,19.99,139.92999999999998],' +
            '["2020-03-23T18:30:00.000Z","Central","Jardine","Pen Set",50,4.99,249.5],' +
            '["2020-04-09T18:30:00.000Z","Central","Andrews","Pencil",66,1.99,131.34],' +
            '["2020-04-26T18:30:00.000Z","East","Howard","Pen",96,4.99,479.04],' +
            '["2020-05-13T18:30:00.000Z","Central","Gill","Pencil",53,1.29,68.37],' +
            '["2020-05-30T18:30:00.000Z","Central","Gill","Binder",80,8.99,719.2],' +
            '["2020-06-16T18:30:00.000Z","Central","Kivell","Desk",5,125,625],' +
            '["2020-07-03T18:30:00.000Z","East","Jones","Pen Set",62,4.99,309.38],' +
            '["2020-07-20T18:30:00.000Z","Central","Morgan","Pen Set",55,12.49,686.95],' +
            '["2020-08-06T18:30:00.000Z","Central","Kivell","Pen Set",42,23.95,1005.9],' +
            '["2020-08-23T18:30:00.000Z","West","Sorvino","Desk",3,275,825],' +
            '["2020-09-09T18:30:00.000Z","Central","Gill","Pencil",7,1.29,9.030000000000001],' +
            '["2020-09-26T18:30:00.000Z","West","Sorvino","Pen",76,1.99,151.24],' +
            '["2020-10-13T18:30:00.000Z","West","Thompson","Binder",57,19.99,1139.4299999999998],' +
            '["2020-10-30T18:30:00.000Z","Central","Andrews","Pencil",14,1.29,18.060000000000002],' +
            '["2020-11-16T18:30:00.000Z","Central","Jardine","Binder",11,4.99,54.89],' +
            '["2020-12-03T18:30:00.000Z","Central","Jardine","Binder",94,19.99,1879.06],' +
            '["2020-12-20T18:30:00.000Z","Central","Andrews","Binder",28,4.99,139.72]],' +
   '"rowRange":{"header":1,"rowStart":10,"rowEnd":40},' +
   '"metric":"Units",' +
   '"dimensions":["Item","Region"],' +
   '"summaryOperator":"Sum",' +
   '"isAsc":false,' +
   '"k":"null",' +
   '"slices":[{"sliceOp":"In","sliceCol":"Region","sliceVal":["West","East"]}],' +
   '"dateRange":"null",' +
   '"timeGranularity":"null",' +
   '"comparisonValue":"null"}';                 
var outputTableShow = [
  ['Item', 'Region', 'Units'], 
  ['Binder', 'East', 174.0],
  ['Binder', 'West', 64.0], 
  ['Desk', 'West', 3.0], 
  ['Pen', 'East', 175.0], 
  ['Pen', 'West', 76.0], 
  ['Pen Set', 'East', 152.0], 
  ['Pencil', 'East', 35.0], 
  ['Pencil', 'West', 32.0]
];
// Suggestions not wired up for show                       
var suggestionsShow = [];

/**
 * TopK intent
 * Query: Find the top-7 Item with maximum Total where Region is Equal to Central
 */
var jsonQueryTopK = 
  '{"intent":"topk",' +
   '"table":[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
            '["2019-01-05T18:30:00.000Z","East","Jones","Pencil",95,1.99,189.05],' +
            '["2019-01-22T18:30:00.000Z","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
            '["2019-02-08T18:30:00.000Z","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
            '["2019-02-25T18:30:00.000Z","Central","Gill","Pen",27,19.99,539.7299999999999],' +
            '["2019-03-14T18:30:00.000Z","West","Sorvino","Pencil",56,2.99,167.44],' +
            '["2019-03-31T18:30:00.000Z","East","Jones","Binder",60,4.99,299.40000000000003],' +
            '["2019-04-17T18:30:00.000Z","Central","Andrews","Pencil",75,1.99,149.25],' +
            '["2019-05-04T18:30:00.000Z","Central","Jardine","Pencil",90,4.99,449.1],' +
            '["2019-05-21T18:30:00.000Z","West","Thompson","Pencil",32,1.99,63.68],' +
            '["2019-06-07T18:30:00.000Z","East","Jones","Binder",60,8.99,539.4],' +
            '["2019-06-24T18:30:00.000Z","Central","Morgan","Pencil",90,4.99,449.1],' +
            '["2019-07-11T18:30:00.000Z","East","Howard","Binder",29,1.99,57.71],' +
            '["2019-07-28T18:30:00.000Z","East","Parent","Binder",81,19.99,1619.1899999999998],' +
            '["2019-08-14T18:30:00.000Z","East","Jones","Pencil",35,4.99,174.65],' +
            '["2019-08-31T18:30:00.000Z","Central","Smith","Desk",2,125,250],' +
            '["2019-09-17T18:30:00.000Z","East","Jones","Pen Set",16,15.99,255.84],' +
            '["2019-10-04T18:30:00.000Z","Central","Morgan","Binder",28,8.99,251.72],' +
            '["2019-10-21T18:30:00.000Z","East","Jones","Pen",64,8.99,575.36],' +
            '["2019-11-07T18:30:00.000Z","East","Parent","Pen",15,19.99,299.84999999999997],' +
            '["2019-11-24T18:30:00.000Z","Central","Kivell","Pen Set",96,4.99,479.04],' +
            '["2019-12-11T18:30:00.000Z","Central","Smith","Pencil",67,1.29,86.43],' +
            '["2019-12-28T18:30:00.000Z","East","Parent","Pen Set",74,15.99,1183.26],' +
            '["2020-01-14T18:30:00.000Z","Central","Gill","Binder",46,8.99,413.54],' +
            '["2020-01-31T18:30:00.000Z","Central","Smith","Binder",87,15,1305],' +
            '["2020-02-17T18:30:00.000Z","East","Jones","Binder",4,4.99,19.96],' +
            '["2020-03-06T18:30:00.000Z","West","Sorvino","Binder",7,19.99,139.92999999999998],' +
            '["2020-03-23T18:30:00.000Z","Central","Jardine","Pen Set",50,4.99,249.5],' +
            '["2020-04-09T18:30:00.000Z","Central","Andrews","Pencil",66,1.99,131.34],' +
            '["2020-04-26T18:30:00.000Z","East","Howard","Pen",96,4.99,479.04],' +
            '["2020-05-13T18:30:00.000Z","Central","Gill","Pencil",53,1.29,68.37],' +
            '["2020-05-30T18:30:00.000Z","Central","Gill","Binder",80,8.99,719.2],' +
            '["2020-06-16T18:30:00.000Z","Central","Kivell","Desk",5,125,625],' +
            '["2020-07-03T18:30:00.000Z","East","Jones","Pen Set",62,4.99,309.38],' +
            '["2020-07-20T18:30:00.000Z","Central","Morgan","Pen Set",55,12.49,686.95],' +
            '["2020-08-06T18:30:00.000Z","Central","Kivell","Pen Set",42,23.95,1005.9],' +
            '["2020-08-23T18:30:00.000Z","West","Sorvino","Desk",3,275,825],' +
            '["2020-09-09T18:30:00.000Z","Central","Gill","Pencil",7,1.29,9.030000000000001],' +
            '["2020-09-26T18:30:00.000Z","West","Sorvino","Pen",76,1.99,151.24],' +
            '["2020-10-13T18:30:00.000Z","West","Thompson","Binder",57,19.99,1139.4299999999998],' +
            '["2020-10-30T18:30:00.000Z","Central","Andrews","Pencil",14,1.29,18.060000000000002],' +
            '["2020-11-16T18:30:00.000Z","Central","Jardine","Binder",11,4.99,54.89],' +
            '["2020-12-03T18:30:00.000Z","Central","Jardine","Binder",94,19.99,1879.06],' +
            '["2020-12-20T18:30:00.000Z","Central","Andrews","Binder",28,4.99,139.72]],' +
   '"rowRange":{"header":1,"rowStart":10,"rowEnd":40},' +
   '"metric":"Total",' +
   '"dimensions":["Item"],' +
   '"summaryOperator":"null",' +
   '"isAsc":false,' +
   '"k":7,' +
   '"slices":[{"sliceOp":"Equal to","sliceCol":"Region","sliceVal":"Central"}],' +
   '"dateRange":"null",' +
   '"timeGranularity":"null",' +
   '"comparisonValue":"null"}';
var outputTableTopK = [
  ['Item', 'Total'], 
  ['Binder', 1305.0], 
  ['Pen Set', 1005.9], 
  ['Binder', 719.2], 
  ['Pen Set', 686.95], 
  ['Desk', 625.0],
  ['Pen Set', 479.04],
  ['Pencil', 449.1]
];
var suggestionsTopK = [
  {'suggestion': 'The results has duplicates'}
];

/**
 * Slice-Compare intent
 * Query: Compare the Mean of Units for the Item Pen and everything by Region 
 * where Region is Not equal to Central
 */
var jsonQuerySliceCompare = 
  '{"intent":"slice_compare",' +
   '"table":[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
            '["2019-01-05T18:30:00.000Z","East","Jones","Pencil",95,1.99,189.05],' +
            '["2019-01-22T18:30:00.000Z","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
            '["2019-02-08T18:30:00.000Z","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
            '["2019-02-25T18:30:00.000Z","Central","Gill","Pen",27,19.99,539.7299999999999],' +
            '["2019-03-14T18:30:00.000Z","West","Sorvino","Pencil",56,2.99,167.44],' +
            '["2019-03-31T18:30:00.000Z","East","Jones","Binder",60,4.99,299.40000000000003],' +
            '["2019-04-17T18:30:00.000Z","Central","Andrews","Pencil",75,1.99,149.25],' +
            '["2019-05-04T18:30:00.000Z","Central","Jardine","Pencil",90,4.99,449.1],' +
            '["2019-05-21T18:30:00.000Z","West","Thompson","Pencil",32,1.99,63.68],' +
            '["2019-06-07T18:30:00.000Z","East","Jones","Binder",60,8.99,539.4],' +
            '["2019-06-24T18:30:00.000Z","Central","Morgan","Pencil",90,4.99,449.1],' +
            '["2019-07-11T18:30:00.000Z","East","Howard","Binder",29,1.99,57.71],' +
            '["2019-07-28T18:30:00.000Z","East","Parent","Binder",81,19.99,1619.1899999999998],' +
            '["2019-08-14T18:30:00.000Z","East","Jones","Pencil",35,4.99,174.65],' +
            '["2019-08-31T18:30:00.000Z","Central","Smith","Desk",2,125,250],' +
            '["2019-09-17T18:30:00.000Z","East","Jones","Pen Set",16,15.99,255.84],' +
            '["2019-10-04T18:30:00.000Z","Central","Morgan","Binder",28,8.99,251.72],' +
            '["2019-10-21T18:30:00.000Z","East","Jones","Pen",64,8.99,575.36],' +
            '["2019-11-07T18:30:00.000Z","East","Parent","Pen",15,19.99,299.84999999999997],' +
            '["2019-11-24T18:30:00.000Z","Central","Kivell","Pen Set",96,4.99,479.04],' +
            '["2019-12-11T18:30:00.000Z","Central","Smith","Pencil",67,1.29,86.43],' +
            '["2019-12-28T18:30:00.000Z","East","Parent","Pen Set",74,15.99,1183.26],' +
            '["2020-01-14T18:30:00.000Z","Central","Gill","Binder",46,8.99,413.54],' +
            '["2020-01-31T18:30:00.000Z","Central","Smith","Binder",87,15,1305],' +
            '["2020-02-17T18:30:00.000Z","East","Jones","Binder",4,4.99,19.96],' +
            '["2020-03-06T18:30:00.000Z","West","Sorvino","Binder",7,19.99,139.92999999999998],' +
            '["2020-03-23T18:30:00.000Z","Central","Jardine","Pen Set",50,4.99,249.5],' +
            '["2020-04-09T18:30:00.000Z","Central","Andrews","Pencil",66,1.99,131.34],' +
            '["2020-04-26T18:30:00.000Z","East","Howard","Pen",96,4.99,479.04],' +
            '["2020-05-13T18:30:00.000Z","Central","Gill","Pencil",53,1.29,68.37],' +
            '["2020-05-30T18:30:00.000Z","Central","Gill","Binder",80,8.99,719.2],' +
            '["2020-06-16T18:30:00.000Z","Central","Kivell","Desk",5,125,625],' +
            '["2020-07-03T18:30:00.000Z","East","Jones","Pen Set",62,4.99,309.38],' +
            '["2020-07-20T18:30:00.000Z","Central","Morgan","Pen Set",55,12.49,686.95],' +
            '["2020-08-06T18:30:00.000Z","Central","Kivell","Pen Set",42,23.95,1005.9],' +
            '["2020-08-23T18:30:00.000Z","West","Sorvino","Desk",3,275,825],' +
            '["2020-09-09T18:30:00.000Z","Central","Gill","Pencil",7,1.29,9.030000000000001],' +
            '["2020-09-26T18:30:00.000Z","West","Sorvino","Pen",76,1.99,151.24],' +
            '["2020-10-13T18:30:00.000Z","West","Thompson","Binder",57,19.99,1139.4299999999998],' +
            '["2020-10-30T18:30:00.000Z","Central","Andrews","Pencil",14,1.29,18.060000000000002],' +
            '["2020-11-16T18:30:00.000Z","Central","Jardine","Binder",11,4.99,54.89],' +
            '["2020-12-03T18:30:00.000Z","Central","Jardine","Binder",94,19.99,1879.06],' +
            '["2020-12-20T18:30:00.000Z","Central","Andrews","Binder",28,4.99,139.72]],' +
   '"rowRange":{"header":1,"rowStart":10,"rowEnd":40},' +
   '"metric":"Units",' +
   '"dimensions":["Region"],' +
   '"summaryOperator":"Mean",' +
   '"isAsc":false,' +
   '"k":"null",' +
   '"slices":[{"sliceOp":"Not equal to","sliceCol":"Region","sliceVal":"Central"}],' +
   '"dateRange":"null",' +
   '"timeGranularity":"null",' +
   '"comparisonValue":["Item","Pen","*"]}';              
var outputTableSliceCompare = [
  ['Region', 'Item', 'Units'], 
  ['East', '*', 48.72727272727273], 
  ['East', 'Pen', 58.333333333333336], 
  ['West', '*', 35.0], 
  ['West', 'Pen', 76.0]
];
// Suggestions not wired up for slice-compare
var suggestionsSliceCompare = [];

/**
 * Test: evalQuery(intent,metric,summaryOperator,isAsc,k,dimensions,slices,
 *                 dateRange,timeGranularity,comparisonValue)
 *
 * To test the show intent
 * Query: Show Sum of Units for Item, Region where Region is In West,East
 */
function testEvalQueryShow() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A10:G40', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = 
    IntentsUi.evalQuery('show', 
                        'Units', 
                        'Sum', 
                        false, 
                        'null', 
                        ['Item', 'Region'], 
                        [{'sliceOp': 'In', 'sliceCol': 'Region', 'sliceVal': ['West', 'East']}],
                        'null', 
                        'null', 
                        'null');                                          
  var expectedOutput = {
    'jsonQuery': jsonQueryShow,
    'outputTable': outputTableShow,
    'suggestions': suggestionsShow
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryShow');
}

/**
 * Test: evalQuery(intent,metric,summaryOperator,isAsc,k,dimensions,slices,
 *                 dateRange,timeGranularity,comparisonValue)
 *
 * To test the top-k intent
 * Query: Find the top-7 Item with maximum Total where Region is Equal to Central
 */
function testEvalQueryTopK() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A10:G40', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput =
   IntentsUi.evalQuery('topk', 
                       'Total', 
                       'null', 
                       false, 
                       7.0, 
                       ['Item'], 
                       [{'sliceOp': 'Equal to', 'sliceCol': 'Region', 'sliceVal': 'Central'}],
                       'null', 
                       'null', 
                       'null');
  var expectedOutput = {
    'jsonQuery': jsonQueryTopK,
    'outputTable': outputTableTopK,
    'suggestions': suggestionsTopK
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQueryTopK');
}

/**
 * Test: evalQuery(intent,metric,summaryOperator,isAsc,k,dimensions,slices,
 *                 dateRange,timeGranularity,comparisonValue)
 *
 * To test the slice-compare intent
 * Query: Compare the Mean of Units for the Item Pen and everything by Region
 * where Region is Not equal to Central
 */
function testEvalQuerySliceCompare() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A10:G40', 1, 'A1:G1');
  
  // Call the function to test
  var generatedOutput = 
    IntentsUi.evalQuery('slice_compare', 
                        'Units', 
                        'Mean', 
                        false, 
                        'null', 
                        ['Region'], 
                        [{'sliceOp': 'Not equal to', 'sliceCol': 'Region', 'sliceVal': 'Central'}],
                        'null', 
                        'null', 
                        ['Item', 'Pen', '*']);
  var expectedOutput = {
    'jsonQuery': jsonQuerySliceCompare,
    'outputTable': outputTableSliceCompare,
    'suggestions': suggestionsSliceCompare
  };

  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'evalQuerySliceCompare');
}

/**
 * Test: getTable()
 */
function testGetTable() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Sheet1');
  IntentsUi.setUserProperties(sheet, 'A10:G40', 1, 'A1:G1');
  
  // Call the function to test
  IntentsUi.getTable();
  var generatedOutput = {
    'table': IntentsUi.jsonObj.table,
    'rowRange': IntentsUi.jsonObj.rowRange
  };
  var expectedOutput = {
    'table': [["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],
              [new Date("2019-01-05T18:30:00.000Z"),"East","Jones","Pencil",95,1.99,189.05],
              [new Date("2019-01-22T18:30:00.000Z"),"Central","Kivell","Binder",50,19.99,999.4999999999999],
              [new Date("2019-02-08T18:30:00.000Z"),"Central","Jardine","Pencil",36,4.99,179.64000000000001],
              [new Date("2019-02-25T18:30:00.000Z"),"Central","Gill","Pen",27,19.99,539.7299999999999],
              [new Date("2019-03-14T18:30:00.000Z"),"West","Sorvino","Pencil",56,2.99,167.44],
              [new Date("2019-03-31T18:30:00.000Z"),"East","Jones","Binder",60,4.99,299.40000000000003],
              [new Date("2019-04-17T18:30:00.000Z"),"Central","Andrews","Pencil",75,1.99,149.25],
              [new Date("2019-05-04T18:30:00.000Z"),"Central","Jardine","Pencil",90,4.99,449.1],
              [new Date("2019-05-21T18:30:00.000Z"),"West","Thompson","Pencil",32,1.99,63.68],
              [new Date("2019-06-07T18:30:00.000Z"),"East","Jones","Binder",60,8.99,539.4],
              [new Date("2019-06-24T18:30:00.000Z"),"Central","Morgan","Pencil",90,4.99,449.1],
              [new Date("2019-07-11T18:30:00.000Z"),"East","Howard","Binder",29,1.99,57.71],
              [new Date("2019-07-28T18:30:00.000Z"),"East","Parent","Binder",81,19.99,1619.1899999999998],
              [new Date("2019-08-14T18:30:00.000Z"),"East","Jones","Pencil",35,4.99,174.65],
              [new Date("2019-08-31T18:30:00.000Z"),"Central","Smith","Desk",2,125,250],
              [new Date("2019-09-17T18:30:00.000Z"),"East","Jones","Pen Set",16,15.99,255.84],
              [new Date("2019-10-04T18:30:00.000Z"),"Central","Morgan","Binder",28,8.99,251.72],
              [new Date("2019-10-21T18:30:00.000Z"),"East","Jones","Pen",64,8.99,575.36],
              [new Date("2019-11-07T18:30:00.000Z"),"East","Parent","Pen",15,19.99,299.84999999999997],
              [new Date("2019-11-24T18:30:00.000Z"),"Central","Kivell","Pen Set",96,4.99,479.04],
              [new Date("2019-12-11T18:30:00.000Z"),"Central","Smith","Pencil",67,1.29,86.43],
              [new Date("2019-12-28T18:30:00.000Z"),"East","Parent","Pen Set",74,15.99,1183.26],
              [new Date("2020-01-14T18:30:00.000Z"),"Central","Gill","Binder",46,8.99,413.54],
              [new Date("2020-01-31T18:30:00.000Z"),"Central","Smith","Binder",87,15,1305],
              [new Date("2020-02-17T18:30:00.000Z"),"East","Jones","Binder",4,4.99,19.96],
              [new Date("2020-03-06T18:30:00.000Z"),"West","Sorvino","Binder",7,19.99,139.92999999999998],
              [new Date("2020-03-23T18:30:00.000Z"),"Central","Jardine","Pen Set",50,4.99,249.5],
              [new Date("2020-04-09T18:30:00.000Z"),"Central","Andrews","Pencil",66,1.99,131.34],
              [new Date("2020-04-26T18:30:00.000Z"),"East","Howard","Pen",96,4.99,479.04],
              [new Date("2020-05-13T18:30:00.000Z"),"Central","Gill","Pencil",53,1.29,68.37],
              [new Date("2020-05-30T18:30:00.000Z"),"Central","Gill","Binder",80,8.99,719.2],
              [new Date("2020-06-16T18:30:00.000Z"),"Central","Kivell","Desk",5,125,625],
              [new Date("2020-07-03T18:30:00.000Z"),"East","Jones","Pen Set",62,4.99,309.38],
              [new Date("2020-07-20T18:30:00.000Z"),"Central","Morgan","Pen Set",55,12.49,686.95],
              [new Date("2020-08-06T18:30:00.000Z"),"Central","Kivell","Pen Set",42,23.95,1005.9],
              [new Date("2020-08-23T18:30:00.000Z"),"West","Sorvino","Desk",3,275,825],
              [new Date("2020-09-09T18:30:00.000Z"),"Central","Gill","Pencil",7,1.29,9.030000000000001],
              [new Date("2020-09-26T18:30:00.000Z"),"West","Sorvino","Pen",76,1.99,151.24],
              [new Date("2020-10-13T18:30:00.000Z"),"West","Thompson","Binder",57,19.99,1139.4299999999998],
              [new Date("2020-10-30T18:30:00.000Z"),"Central","Andrews","Pencil",14,1.29,18.060000000000002],
              [new Date("2020-11-16T18:30:00.000Z"),"Central","Jardine","Binder",11,4.99,54.89],
              [new Date("2020-12-03T18:30:00.000Z"),"Central","Jardine","Binder",94,19.99,1879.06],
              [new Date("2020-12-20T18:30:00.000Z"),"Central","Andrews","Binder",28,4.99,139.72]],
    'rowRange': { 'rowStart': 10.0, 'header': 1.0, 'rowEnd': 40.0}
  };

  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'getTable');
}

/**
 * Test: callGcpToGetQueryResult()
 *
 * To test the show intent
 * Query: Show Sum of Units for Item, Region where Region is In West,East
 */
function testCallGcpToGetQueryResultShow() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResult(jsonQueryShow);                                         
  var expectedOutput = {
    'outputTable': outputTableShow,
    'suggestions': suggestionsShow
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultShow');
}

/**
 * Test: callGcpToGetQueryResult()
 *
 * To test the top-k intent
 * Query: Find the top-7 Item with maximum Total where Region is Equal to Central
 */
function testCallGcpToGetQueryResultTopK() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResult(jsonQueryTopK);                                         
  var expectedOutput = {
    'outputTable': outputTableTopK,
    'suggestions': suggestionsTopK
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultTopK');
}

/**
 * Test: callGcpToGetQueryResult()
 *
 * To test the slice-compare intent
 * Query:  Compare the Mean of Units for the Item Pen and everything by Region
 * where Region is Not equal to Central
 */
function testCallGcpToGetQueryResultSliceCompare() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResult(jsonQuerySliceCompare);                                         
  var expectedOutput = {
    'outputTable': outputTableSliceCompare,
    'suggestions': suggestionsSliceCompare
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultSliceCompare');
}

/**
 * Test: callGcpToGetQueryResultUsingJson()
 *
 * To test the show intent
 * Query: Show Sum of Units for Item, Region where Region is In West,East
 */
function testCallGcpToGetQueryResultUsingJsonShow() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResultUsingJson(jsonQueryShow);                                         
  var expectedOutput = {
    'jsonQuery': jsonQueryShow,
    'outputTable': outputTableShow,
    'suggestions': suggestionsShow
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultUsingJsonShow');
}

/**
 * Test: callGcpToGetQueryResultUsingJson()
 *
 * To test the top-k intent
 * Query: Find the top-7 Item with maximum Total where Region is Equal to Central
 */
function testCallGcpToGetQueryResultUsingJsonTopK() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResultUsingJson(jsonQueryTopK);                                         
  var expectedOutput = {
    'jsonQuery': jsonQueryTopK,
    'outputTable': outputTableTopK,
    'suggestions': suggestionsTopK
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultUsingJsonTopK');
}

/**
 * Test: callGcpToGetQueryResultUsingJson()
 *
 * To test the slice-compare intent
 * Query:  Compare the Mean of Units for the Item Pen and everything by Region
 * where Region is Not equal to Central
 */
function testCallGcpToGetQueryResultUsingJsonSliceCompare() {
  // Call the function to test
  var generatedOutput = IntentsUi.callGcpToGetQueryResultUsingJson(jsonQuerySliceCompare);                                         
  var expectedOutput = {
    'jsonQuery': jsonQuerySliceCompare,
    'outputTable': outputTableSliceCompare,
    'suggestions': suggestionsSliceCompare
  };
 
  // Checking if generated output is same as expected output
  assertEquals(expectedOutput, generatedOutput, 'callGcpToGetQueryResultUsingJsonSliceCompare');
}