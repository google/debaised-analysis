// Master test file

/**
 * Master test function which calls all tests of the project
 */
function masterTestFunction() {
  testTableSelectionFunctions();
  testDetectDateFunctions();
  testQueryProcessingFunctions();
  testDataFormattingFunctions();
  testCreateQueryFunctions();
  testErrorCheckFunctions();
}

/**
 * Compare the values received and check if they are equal
 *
 * @param {(Object|Array|boolean|string|number)} generatedOutput The output received by function called
 * @param {(Object|Array|boolean|string|number)} expectedOutput The output expected to be received
 * @param {string} functionName The name of function being tested
 */
function assertEquals(expectedOutput, generatedOutput, functionName) {
  Logger.log('Function: ', functionName);
  Logger.log('Expected output: ', expectedOutput);
  Logger.log('Generated output: ', generatedOutput) ;
  
  // Flag variable is used to indicate if generated output and expected output are equal
  // True indicates they are equal and False indicates the are unequal
  var flag = true;
  
  // If the outputs don't have same type, set flag to false
  if(typeof generatedOutput !== typeof expectedOutput) {
    flag = false;
  }
  // Else if generated output is an object, compare values of 2 objects
  else if( typeof generatedOutput === 'object') {
    flag = objectCompare(expectedOutput, generatedOutput);
  }
  // Else generated and expected output will be of type: boolean/string/number
  else {
    flag = (generatedOutput === expectedOutput);
  }
  
  // If generated output and expected output are equal: success
  if(flag) {
    Logger.log('Function:',functionName,' Success');
  }
  // Else generated output and expected output are not equal: failure
  else {
    Logger.log('Function:',functionName,' Failure ');
    throw new Error('Function: ' + functionName + ' failed!');
  }
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
          Logger.log('failing at',p);
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