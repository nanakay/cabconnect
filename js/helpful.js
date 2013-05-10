//A Library of Custom Helper Functions
//Created by Nana Ewusi
/**********************
/**********************




/*******************************************************************************************
--------------------------
DOM Manipulation Functions
--------------------------
*******************************************************************************************/
function createElement(tagName, attValString)
{
	var elem = document.createElement(tagName);

	if (attValString) //Check there are any attributes to set
	{
		var attribs = []; //will hold the attribute-value pairs in a 2-dimensional array
		if (attValString.indexOf(",") === -1)
		{
			attribs.push(attValString);
		}
		else
		{
			//First retrieve the last attribut:value pair and insert it into the attribs array
			//Since the last pair will have no comma symbol after it
			attribs.push(attValString.substring(attValString.lastIndexOf(",") + 1));

			var sFlag = 0;
			var commaPos = attValString.indexOf(",", sFlag);

			while (commaPos !== -1)
			{

				attribs.push(attValString.substring(sFlag, commaPos));
				sFlag = commaPos + 1;
				commaPos = attValString.indexOf(",", sFlag);
			}
		}

		for (var p = 0; p < attribs.length; p++)
		{
			//retrieve attribute & value info
			var att = attribs[p].substring(0, attribs[p].indexOf(":"));
			var val = attribs[p].substring(attribs[p].indexOf(":") + 1);

			elem.setAttribute(att, val);
		}
	}
	return elem;
}

function createTextNode(value)
{
	var textNode = document.createTextNode(value);
	return textNode;
}

function appendElement(elm, parent)
{
	if (parent)
	{
		parent.appendChild(elm);
	}
}

function removeElement(elm)
{
	var eParent = (elm.parentNode || null);
	if (eParent)
	{
		eParent.removeChild(elm);
	}
}

function getParent(elm)
{
	return elm.parentNode;
}

function replaceElement(newElm, oldElm)
{
	var eParent = (oldElm.parentNode || null);
	if (eParent)
	{
		eParent.replaceChild(newElm, oldElm);
	}
}

/*
function getAttribute(elm, attrib)
{
	if (elm)
	{
		var attribute = attrib;
		return elm.attribute;
	}
}*/

function hasChild(elm, childName)
{
	if (!elm.hasChildNodes()) return false;

	var children = elm.childNodes;
	for (var i = 0; i < children.length; i++)
	{
		var child = children[i];

		if (child.nodeType !== 1)
		{
			continue;
		}
		if (child.nodeName.toLowerCase() == childName) return true;
	}
}

function getById(id)
{
	return document.getElementById(id);
}

function getByTag(tagname, container)
{
	var searchArea = (container || window.document);
	return searchArea.getElementsByTagName(tagname);
}

function getByClass(classname)
{
	var allElems
	if (typeof document.all !== "undefined")
	{
		allElems = document.all;
	}
	else
	{
		allElems = document.getElementsByTagName("*");
	}

	var matchedElems = [];
	var pattern = new RegExp("(^| )" + classname + "( |$)");
	for (var e = 0; e < allElems.length; e++)
	{
		if (testPattern(pattern, allElems[e].className))
		{
			matchedElems.push(allElems[e]);
		}
	}
	return matchedElems;
}

function cloneElem(elm, cloneChildren)
{
	var copy = elm.cloneNode(cloneChildren);
	return copy;
}

function hasClass(elm, classname)
{
	var pattern = new RegExp("(^| )" + classname + "( |$)");
	return testPattern(pattern, elm.className);
}

function addClass(elm, classname)
{
	if (!hasClass(elm, classname))
	{
		if (elm.className == "")
		{
			elm.className = classname;
		}
		else
		{
			elm.className += " " + classname;
		}
	}
}

function removeClass(elm, classname)
{
	var pattern = new RegExp("(^| )" + classname + "( |$)");

	elm.className = replacePattern(pattern, elm.className, "$1");
	elm.className = replacePattern(/ $/, elm.className, "");
}

function ascendDom(elm, target)
{
	while (elm.nodeName.toLowerCase() !== target && elm.nodeName.toLowerCase() !== 'html')
	{
		elm = elm.parentNode;
	}
	return (elm.nodeName.toLowerCase() == 'html') ? null : elm;
}




/***********************************************************************************************
------------------------
Event Handling Functions
------------------------
************************************************************************************************/

function addListener(elm, event, fn, useCapture)
{
	if (elm.addEventListener)
	{
		elm.addEventListener(event, fn, useCapture);
		return true;
	}
	else if (elm.attachEvent)
	{
		var r = elm.attachEvent('on' + event, fn);
		return r;
	}
	else
	{
		elm['on' + event] = fn;
	}
}

function getSourceElement(eObj)
{
	var e, targ;
	e = (eObj || window.event);
	if (e.target)
	{
		targ = e.target;
	}
	else
	{
		targ = e.srcElement;
	}
	if (targ.nodeType == 3) targ = targ.parentNode; //Possible browser bug
	return targ;
}
function getEvent(eObj)
{
	var e = (eObj || window.event);
	return e.type;
}
function getButton(eObj)
{
	var e = (eObj || window.event);
	return e.button;
}
function getKeyCode(eObj)
{
	var e = (eObj || window.event);
	if (e.which)
	{
		return e.which;
	}
	else if (e.keyCode)
	{
		return e.keyCode;
	}
}

//function getKeyCode(eObj) {
//    var keycode = null;
//    if(window.event) {
//        keycode = window.event.keyCode;
//    }else if(eObj) {
//        keycode = eObj.which;
//    }
//    return keycode;
//}

function getMousePosition(eObj) //Returns the horizontal(y) & vertical(x) positions of the cursor relative to the whole document (!NOT THE WINDOW)
{
	var positions = [];
	var posx = 0;
	var posy = 0;

	var e = (eObj || window.event);

	if (e.pageX || e.pageY)
	{
		posx = e.pageX;
		posy = e.pageY;
	}
	else if (e.clientX || e.clientY)
	{
		posx = e.clientX;
		posy = e.clientY;
	}
	if (!window.opera && navigator.userAgent.indexOf('MSIE') != -1)
	{
		posx += document.body.scrollLeft;
		posy += document.body.scrollTop;
	}

	positions.push(posx);
	positions.push(posy);
	return positions;
}

function preventDefaultAction(eObj)
{
	if (eObj && eObj.preventDefault)
	{
		eObj.preventDefault();
	}
	else
	{
		window.event.returnValue = false;
	}
}

function stopPropagation(eObj)
{
	if (eObj && eObj.stopPropagation)
	{
		eObj.stopPropagation();
	}
	else
	{
		window.event.cancelBubble = true;
	}
}




/***********************************************************************************************
-------------------
Animation Functions
-------------------
************************************************************************************************/

function findPos(elm) //Returns the horizontal(x) and vertical(y) positions of a given element
{
	var pos = [];
	var curLeft = 0;
	var curTop = 0;

	if (elm.offsetParent)
	{
		do
		{
			curLeft += elm.offsetLeft;
			curTop += elm.offsetTop;
		} while (elm = elm.offsetParent);
	}
	else if (elm.x && elm.y)
	{
		curLeft += elm.x;
		curTop += elm.y;
	}
	pos.push(curLeft);
	pos.push(curTop);
	return pos;
}

function getStyle(elm, styleProp) //Returns the specified style value for a given element
{
	var value;
	if (elm.currentStyle)
	{
		value = elm.currentStyle[styleProp];
	}
	else if (window.getComputedStyle)
	{
		value = document.defaultView.getComputedStyle(elm,null).getPropertyValue(styleProp);
	}
	return value;
}


/***********************************************************************************************
----------------
String Functions
----------------
************************************************************************************************/

//Function Name: testPattern
//Arguments: Requires two arguments namely, pattern & targetString, both of which are compulsory
//Description: Tests for a match of "pattern" in "targetString".
//Returns true if a match is found or false if otherwise

var testPattern = function(pattern, targetString)
{
	return pattern.test(targetString);
}

//Function Name: matchPattern
//Arguments: Requires two arguments namely, pattern & targetString, both of which are compulsory
//Description: Searches 'targetString' for a match against a regular expression, 'pattern'
//Returns an array containing the matched items or false if no match is found

var matchPattern = function(pattern, targetString)
{
	var matchedItems;
	if (targetString.match(pattern))
	{
		matchedItems = targetString.match(pattern);
		return matchedItems;
	}
	else
	{
		return false;
	}
}

//Function Name: replacePattern
//Arguments: Requires three arguments namely, pattern, targetString & replacementString, all of which are compulsory
//Description: Searches 'targetString' for all matches against a regular expression, 'pattern'
//All matches found in 'targetString' are replaced with 'replacementString'
//The function then returns a new string with the replacements made

var replacePattern = function(pattern, targetString, replacementString)
{
	var newString = targetString.replace(pattern, replacementString);
	return newString;
}



/*******************************************************************************************
---------------
Array Functions
---------------
*******************************************************************************************/

//Function Name: indexOf
//Arguments: accepts four arguments, 'item', 'arr', 'start', 'stop'
//'item' is compulsory and specifies the subject (whose index is) being search for
//'arr' is compulsory and specifies the array to be searched
//'start' is optional and specifies the index from which to start searching. Search will begin at the index 0, if 'start' is not specified
//'stop' is optional and specifies the index at which the search should stop. Search will stop at the end of the array if 'stop' is not specified
//Description: The function searches the arrary 'arr' (from the position 'start' to the position 'stop') for the first occurrence of the subject 'item'.
//It returns the index at which 'item' is found or -1 if 'item' is not found in the array

function indexOf(item, arr, start, stop)
{
	if (start >= arr.length || start < 0 || stop >= arr.length || stop < 0 || stop < start) return -1;
	var index;
	var startPoint = (start || 0);
	var stopFlag = (stop+1 || arr.length);

	var i;
	for (i = startPoint; i < stopFlag; i++)
	{
		if (arr[i] === item)
		{
			index = i;
			return index;
		}
	}
	index = -1;
	return index;
}

//Function Name: lastIndexOf
//Arguments: accepts four arguments, 'item', 'arr', 'start', 'stop'
//'item' is compulsory and specifies the subject (whose index is) being search for
//'arr' is compulsory and specifies the array to be searched
//'start' is optional and specifies the index from which to start searching. Search will begin at the end of the array if 'start' is not specified
//'stop' is optional and specifies the index at which the search should stop. Search will stop at the beginning of the array if 'stop' is not specified
//Description: The function searches the arrary 'arr' (from the position 'start' to the position 'stop') for the first occurrence of the subject 'item'.
//It returns the index at which 'item' is found or -1 if 'item' is not found in the array

function lastIndexOf(item, arr, start, stop)
{
	if (start >= arr.length || start < 0 || stop >= arr.length || stop < 0 || start < stop) return -1;
	var index;
	var startPoint = (start || arr.length-1);
	var stopFlag = (stop-1 || -1); //ensures that the first element in the array is checked

	var i;
	for (i = startPoint; i > stopFlag; i--)
	{
		if (arr[i] === item)
		{
			index = i;
			return index;
		}
	}
	index = -1;
	return index;
}

//Function Name: some
//Arguments: accepts two arguments, 'arr', 'func' both of which are compulsory
//'arr' is an array
//'func' is an function that will perform some kind of test on each element in the 'arr' array
//Description: The function 'some' is an array testing function.
//For each element it finds in the array 'arr' it calls the function 'func', passing it the elements value, index and parent array
//The function 'func' in turn tests the element against some condition and returns true or false depending on the results
//'some' will return true, so long as AT LEAST ONE, of the elements in the 'arr' array passes the test in the function 'func'
//If this is not the case, it returns false

function some(arr, func)
{
	var result = false;
	if (arr.length == 0) return result;
	for (var i = 0; i < arr.length; i++)
	{
		if (func(arr[i], i, arr))
		{
			result = true;
			break;
		}
	}
	return result;
}

//Function Name: every
//Arguments: accepts two arguments, 'arr', 'func' both of which are compulsory
//'arr' is an array
//'func' is an function that will perform some kind of test on each element in the 'arr' array
//Description: The function 'every' is an array testing function.
//For each element it finds in the array 'arr' it calls the function 'func', passing it the elements value, index and parent array
//The function 'func' in turn tests the element against some condition and returns true or false depending on the results
//'some' will return true, so long as ALL the elements in the 'arr' array pass the test in the function 'func'
//If even one of the elements fail the test, it returns false

function every(arr, func)
{
	var result = true;
	if (arr.length == 0) return result;
	for (var i = 0; i < arr.length; i++)
	{
		if (!func(arr[i], i, arr))
		{
			result = false;
			break;
		}
	}
	return result;
}

//Function Name: filter
//Arguments: accepts two arguments, 'arr', 'func' both of which are compulsory
//'arr' is an array
//'func' is an function that will perform some kind of test on each element in the 'arr' array
//Description: The function 'filter' is an array testing function.
//For each element it finds in the array 'arr' it calls the function 'func', passing it the elements value, index and parent array
//The function 'func' in turn tests the element against some condition and returns true or false depending on the results
//'filter' will return an array containing all elements the pass the test in the function 'func'
//'filter' is most useful when used in combination with the function 'some' to make sure we are calling 'filter' as long as 'some' returns true

function filter(arr, func)
{
	var resultSet = [];
	if (arr.length == 0) return resultSet;
	for (var i = 0; i < arr.length; i++)
	{
		if (func(arr[i], i, arr))
		{
			resultSet.push(arr[i]);
		}
	}
	return resultSet;
}

//Function Name: forEach
//Arguments: accepts two arguments, 'arr', 'func' both of which are compulsory
//'arr' is an array
//'func' is an function that will perform some kind action on each element in the 'arr' array
//Description: The function 'forEach' is an iterative array function.
//For each element it finds in the array 'arr' it calls the function 'func', passing it the elements value, index and parent array
//The function 'func' performs some action on the element
//WORTH NOTING is the fact that 'forEach' does not return any value. It simply passes each element in 'arr' to the function 'func' to do something with
//but does not store the result of that operation in any way.

function forEach(arr, func)
{
	if (arr.length == 0) return;
	for (var i = 0; i < arr.length; i++)
	{
		func(arr[i], i, arr);
	}
}

//Function Name: map
//Arguments: accepts two arguments, 'arr', 'func' both of which are compulsory
//'arr' is an array
//'func' is an function that will perform some kind action on each element in the 'arr' array and return the result of the operation
//Description: The function 'map' is an iterative array function.
//For each element it finds in the array 'arr' it calls the function 'func', passing it the elements value, index and parent array
//The function 'func' performs some action on the element and returns the result of the operation
//The function 'map' then returns an array containing the values from each iteration of the function 'func'

function map(arr, func)
{
	var resultSet = [];
	if (arr.length == 0) return resultSet;
	for (var i = 0; i < arr.length; i++)
	{
		resultSet.push(func(arr[i], i, arr));
	}
	return resultSet;
}

function randomItem(arr)
{
	var i; //Will hold a random number representing, the index of the element to return
	var from = 0;
	var to = arr.length - 1;
	i = randomNumber(from, to);
	return arr[i];
}

function removeItem(index, arr)
{
	if (index >= 0 || index < arr.length)
	{
		var removedItem = arr.splice(index, 1);
		return removedItem;
	}
	else
	{
		return;
	}
}


/*******************************************************************************************
----------------
Number Functions
----------------
*******************************************************************************************/

//Function Name: randomNumber
//Arguments: accepts two arguments, 'min' & 'max' both of which are compulsory
//Description: Returns a random number between min & max inclusive

function randomNumber(min, max)
{
	return Math.floor((Math.random() * ((max - min) + 1)) + min);
}

//Function Name: isNumber
//Arguments: accepts one argument, 'item'
//Description: Returns true if 'item' is a number or false if otherwise

var isNumber = function(item)
{
	return !isNaN(item);
}
