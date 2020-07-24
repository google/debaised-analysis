// Master test file

/**
 * Master test function which calls all tests of the project
 */
function masterTestFunction() {
  // Tests for selecting data range
  testTableSelectionFunctions();

  // Tests for detecting date columns and their format
  testDetectDateFunctions();

  // Tests for processing queries
  testQueryProcessingFunctions();

  // Tests for formatting table cells
  testDataFormattingFunctions();

  // Tests for creating query from given json
  testCreateQueryFunctions();

  // Tests for error check functions on client-side javascript
  testErrorCheckFunctions();
}
