// Json created for each intent

/**
 * SHOW
 * Show Sum of Units for Item from OrderDate 2019-01-06 to 2019-07-12
 */
var jsonQueryShow = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"show",' +
	'"metric":"Units",' +
	'"summaryOperator":"Sum",' +
	'"isAsc":false,' +
	'"topKLimit":10,' +
	'"dimensions":["Item"],' +
	'"dateRange":{"dateCol":"OrderDate","dateStart":"2019-01-06","dateEnd":"2019-07-12"},' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';

/**
 * TOP-K
 * Find the top-7 Rep with maximum Total where Units is Greater than 50
 */
var jsonQueryTopK = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"topk",' +
	'"metric":"Total",' +
	'"isAsc":false,' +
	'"topKLimit":7,' +
	'"dimensions":["Rep"],' +
	'"slices":[{"sliceCol":"Units","sliceOp":"Greater than","sliceVal":50}],' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';

/**
 * SLICE-COMPARE
 * Compare the Mean of Unit Cost for the Region East and West by Item
 */
var jsonQuerySliceCompare = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"slice_compare",' +
	'"metric":"Unit Cost",' +
	'"summaryOperator":"Mean",' +
	'"isAsc":false,' +
	'"topKLimit":10,' +
	'"dimensions":["Item"],' +
	'"comparisonValue":{"comparisonColumn":"Region","slice1":"East","slice2":"West"},' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';

/**
 * TIME-COMPARE
 * Compare the Mean of Unit Cost for the OrderDate 2019-01-06 to 2019-03-15 and 2019-04-01 to 2019-07-12 by Region
 */
var jsonQueryTimeCompare = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"time_compare",' +
	'"metric":"Unit Cost",' +
	'"summaryOperator":"Mean",' +
	'"isAsc":false,' +
	'"topKLimit":10,' +
	'"dimensions":["Region"],' +
	'"compareDateRange":' +
      '{"dateCol":"OrderDate",' + 
      '"dateStart1":"2019-01-06",' + 
      '"dateEnd1":"2019-03-15",' + 
      '"dateStart2":"2019-04-01",' + 
      '"dateEnd2":"2019-07-12"},' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';
    
/**
 * TREND
 * Monthly trend of Sum of Units where Item is In Binder, Pencil, Pen from OrderDate 2019-01-06 to 2019-07-12
 */
var jsonQueryTrend = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"trend",' +
	'"metric":"Units",' +
	'"summaryOperator":"Sum",' +
	'"isAsc":false,' +
	'"topKLimit":10,' +
	'"slices":[{"sliceCol":"Item","sliceOp":"In","sliceVal":["Binder","Pencil","Pen"]}],' +
	'"dateRange":{"dateCol":"OrderDate","dateStart":"2019-01-06","dateEnd":"2019-07-12"},' +
	'"timeGranularity":"Monthly",' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';	

/**
 * CORRELATION
 * Correlation between Unit Cost and Total for each Item
 */
var jsonQueryCorrelation = 
	'{"table":' +
      '[["OrderDate","Region","Rep","Item","Units","Unit Cost","Total"],' +
      '["1/6/2019","East","Jones","Pencil",95,1.99,189.05],' +
      '["1/23/2019","Central","Kivell","Binder",50,19.99,999.4999999999999],' +
      '["2/9/2019","Central","Jardine","Pencil",36,4.99,179.64000000000001],' +
      '["2/26/2019","Central","Gill","Pen",27,19.99,539.7299999999999],' +
      '["3/15/2019","West","Sorvino","Pencil",56,2.99,167.44],' +
      '["4/1/2019","East","Jones","Pen",60,4.99,299.40000000000003],' +
      '["4/18/2019","Central","Andrews","Pencil",75,1.99,149.25],' +
      '["5/5/2019","Central","Jardine","Pencil",90,4.99,449.1],' +
      '["5/22/2019","West","Thompson","Pencil",32,1.99,63.68],' +
      '["6/8/2019","East","Jones","Binder",60,8.99,539.4],' +
      '["6/25/2019","Central","Morgan","Pencil",90,4.99,449.1],' +
      '["7/12/2019","East","Howard","Binder",29,1.99,57.71]],' +
	'"intent":"correlation",' +
	'"isAsc":false,' +
	'"topKLimit":10,' +
	'"dimensions":["Item"],' +
	'"correlationMetrics":{"metric1":"Unit Cost","metric2":"Total"},' +
	'"dateColumns":' +
      '{"OrderDate":' +
        '{"type":"CONSISTENT",' +
        '"day_first":false,' +
        '"min_date":{"day_first_false":"2019-01-06"},' +
        '"max_date":{"day_first_false":"2019-07-12"}}' +       
      '}' +
	'}';
