var xhttp;
if (window.XMLHttpRequest) {
	xhttp = new XMLHttpRequest();
}
else {
	xhttp = new ActiveXObject('Microsoft.XMLHTTP');
}

var number; 
var firstName;
function initAll() {
//	startBtnArray = getByClass("start_btn");
	
//	for (var i = 0; i < startBtnArray.length; i++) {
////		alert(startBtnArray[i]);
//		startBtnArray[i].onclick = Navigate;
//	}
	number = document.getElementById("phone_number");
    firstName = getById("firstName");
	
	var login_btn = document.getElementById("login_btn")
	login_btn.onclick = verify_user;
	
	var signup_btn = getById("signup_btn");
	signup_btn.onclick = createUser;
	
}

function verify_user(evt) {
//	evt.preventDefault();
	var phonenumber = document.getElementById('in_phone_number').value;
	var password = document.getElementById('in_password').value;
	
	 xhttp.onreadystatechange = function() {
//	      alert(xhttp.readyState + " Status: " + xhttp.status);
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
	            var resp = xhttp.responseText;
	            if (resp.indexOf('failed') != -1) {
	                
	                var error = "Username or password incorrect";
                   var el = document.getElementById("login_error");
                   el.innerHTML = error;
                   el.style.display = "block";
	                
	            } else {
	                
	               var current_url = window.location.href;
                   var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#start_page";
                   
                   number.value = phonenumber;
                   firstName.value = resp;
                   
                   getById("welcome_user").innerHTML = "Welcome " + firstName.value;
                   
                   window.location.href = passenger_url;
	            }
	        }
	    }
	    var url = '/verifyuser?phonenumber=' + phonenumber + '&password=' + password;
	    xhttp.open('POST', url, true);
	    xhttp.send();
}

function loginNavigate () {
//	evt.preventDefault();
	window.location.replace("http://localhost:8081/signup#login");
}

function signupNavigate () {
//	evt.preventDefault();
	window.location.replace("http://localhost:8081/signup#signup");
}

function createUser(evt) {
	
	evt.preventDefault();
	var phone_number = getById("signup_phoneNumber").value;
	var password = getById("signup_password").value;
	var verify_password = getById("verify_password").value;
	var email = getById("signup_email").value;
	var first_name = getById("signup_fName").value;
	var last_name = getById('signup_lName').value;
	
	
	
	if (phone_number && password && verify_password && email && first_name && last_name) {
//		alert("data received");
		
		xhttp.onreadystatechange = function() {
			//alert("Still signing Up " + xhttp.readyState + " " + xhttp.status);
			if (xhttp.readyState == 4 && xhttp.status == 200) {
				alert(xhttp.readyState + " " + xhttp.status)
				var resp = xhttp.responseText;
				alert(resp)
				if (resp.indexOf('failed') != -1) {
					var error = resp;
					getById("error").style.display = "block";
					getById("error").innerHTML = error;
				}
				else {
					var current_url = window.location.href;
					var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#start_page";
					window.location.href = passenger_url;
				}
//					var current_url = window.location.href;
//					var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#user_details";
//					alert(current_url);
////					window.location.href = passenger_url;
//					
//				} else {
//					document.getElementById("error").style.display = "block";
//					
//				}
			}
		}
		var url = '/createuser?option=verify_number' + "&phone_number=" + phone_number;
		xhttp.open('POST', url, true);
		xhttp.send();
	}
	else {
		var error = "All data are required please";
		getById("error").style.display = "block";
		getById("error").innerHTML = error;
	}
//	console.log(phone_number, password, verify_password, email);
}

function verifyNumber(number) {
	alert("in verify number function")
	if (number) {
		xhttp.onreadystatechange = function() {
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
	        	alert(xhttp.readyState + " " + xhttp.status)
	            var resp = xhttp.responseText;
	            alert(resp)
	            if (resp === "successful") {
	                var current_url = window.location.href;
	                var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#request-confirmation";
	                window.location.href = passenger_url;
	            }
	            else {
	//            	alert(resp);
	                var error = "Something went wrong";
	                var error_el = getById("request_error");
	                error_el.innerHTML = error;
	                error_el.style.display = "block"
	            }
	            
	        }
    	}
		var url = '/createuser?option=create_user' + '&phone_number=' + phone_number + '&password=' + password + "&email=" + email + "&first_name=" + first_name + "&last_name=" + last_name;
        alert (url);
        xhttp.open('POST', url, true);
        xhttp.send();
	}
	
}

function validateEmail (email) {
	var atpos=email.indexOf("@");
	var dotpos=email.lastIndexOf(".");
	if (atpos<1 || dotpos<atpos+2 || dotpos+2>=email.length)
	  {
		alert("The email entered is not valid");
	  return false;
	  }
	
}

function requestCab() {
    current_location = getById("request_location").value;
    destination = getById("request_destination").value;
    pickup_time = getById("pickup_time").value;
    other_info = getById("other_info").value;
    
    
    if (current_location && destination && pickup_time && number.value) {
    	xhttp.onreadystatechange = function() {
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
	//        	alert(xhttp.readyState + " " + xhttp.status)
	            var resp = xhttp.responseText;
	            if (resp === "successful") {
	                var current_url = window.location.href;
	                var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#request-confirmation";
	                window.location.href = passenger_url;
	            }
	            else {
	//            	alert(resp);
	                var error = "Something went wrong";
	                var error_el = getById("request_error");
	                error_el.innerHTML = error;
	                error_el.style.display = "block"
	            }
	            
	        }
    	}
        var url = '/request?current_location=' + current_location + '&destination=' + destination + "&time=" + pickup_time + "&phone_number=" + number.value + "&other_info=" + other_info;
        alert (url);
        xhttp.open('POST', url, true);
        xhttp.send();
    }
    
    else {
        var error = "Some required data have not been provided";
        var error_el = getById("request_error");
        error_el.innerHTML = error;
        error_el.style.display = "block";
    }
}

function addDriver () {
	first_name = getById("driver_first_name").value;
	last_name = getById("driver_last_name").value;
	password = getById("driver_password").value;
	email = getById("driver_p_number").value;
	
//	alert(first_name + " " + last_name + " " + password + " " + email);
	
	if (first_name && last_name && password && email) {
		xhttp.onreadystatechange = function() {
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
	            var resp = xhttp.responseText;
	            if (resp.indexOf("successfully") != -1) {
	                var current_url = window.location.href;
	                var passenger_url = current_url.substring(0, current_url.lastIndexOf("&"));
//	                var passeger_url = current_url + "#driver_confirmation";
	                
	                window.location.href = passenger_url;
	                
	            }
	            else {
	                var error = "Sorry, You cannot create two accounts with the same number";
	                var error_el = getById("driver_error");
	                error_el.innerHTML = error;
	                error_el.style.display = "block"
	            }
	            
	        }
    	}
        var url = '/admin?option=add_driver' + "&driver_first_name=" + first_name + '&driver_last_name=' + last_name + "&driver_password=" + password + "&driver_p_number=" + email;
        xhttp.open('POST', url, true);
        xhttp.send();
	} 
	else {
		var error = "Please provide all details";
        var error_el = getById("driver_error");
        error_el.innerHTML = error;
        error_el.style.display = "block"
	}
}

function assignDriver() {
	driver = getById("assigned_driver").value;
	name_array = driver.split(" "); 
	
	var first_name = name_array[0];
	var last_name = name_array[1];
	var message = getById("acceptance_note").value;
	var key = getById("request_key").value;
	
	if (first_name && last_name && message && key) {
		xhttp.onreadystatechange = function() {
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
	            var resp = xhttp.responseText;
	            if (resp.indexOf("successful") != -1) {
	                var current_url = window.location.href;
	                var passenger_url = current_url.substring(0, current_url.lastIndexOf("&"));
//	                var passeger_url = current_url + "#driver_confirmation";
	                window.location.href = passenger_url;
	                location.reload();
	            }
	            else {
	                var error = "Sorry, process could not finish";
	                var error_el = getById("driver_error");
	                error_el.innerHTML = error;
	                error_el.style.display = "block"
	            }
	            
	        }
    	}
        var url = '/admin?option=assign_driver' + "&driver_first_name=" + first_name + '&driver_last_name=' + last_name + "&message=" + message + "&request_key=" + key;
        xhttp.open('POST', url, true);
        xhttp.send();
	} 
	else {
		var error = "Please additional information will help the client";
        var error_el = getById("assign_error");
        error_el.innerHTML = error;
        error_el.style.display = "block"
	}
}

function reserveCab() {
    current_location = getById("reserve_location").value;
    destination = getById("reserve_destination").value;
    from_date = getById("from_date").value;
    to_date = getById("to_date").value;
    pickup_time = getById("reserve_pickup_time").value;
    to_time = getById("reserve_to_time").value;
    passengers = getById("total_passengers").value;
    other_info = getById("reserve_other_info").value;
    
    if (current_location && destination && from_date && to_date && pickup_time && to_time && passengers && number.value) {
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
              alert(xhttp.readyState + " " + xhttp.status)
                var resp = xhttp.responseText;
                alert(resp);
                if (resp === "successful") {
                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#request-confirmation";
                    window.location.href = passenger_url;
                }
                else {
                    var error = "Please check your internet connection";
                    getError("request_error", error)
                }
                
            }
        }
        var url = '/request?option=reserve_cab' + '&current_location=' + current_location + '&destination=' + destination + "&from_date=" + from_date + "&to_date=" + to_date + "&reserve_pickup_time=" + pickup_time + "&to_time=" + to_time + "&phone_number=" + number.value + "&total_passengers=" + passengers + "&other_info=" + other_info;
        xhttp.open('POST', url, true);
        xhttp.send();
    }
    else {
        var error = "Some required data have not been provided";
        getError("reserve_error", error);
    }
    
}

function getError(elId, error) {
    var error_el = getById(elId); 
    error_el.innerHTML = error;
    error_el.style.display = "block";
}

function checkHistory() {
	xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
//          alert(xhttp.readyState + " " + xhttp.status)
            var resp = xhttp.responseText;
//            alert(resp);
            if (resp) {
                var current_url = window.location.href;
                var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#check-history";
                
                window.console.log(resp);
                var history = JSON.parse(resp);
                
                var brk = document.createElement("br")
                history_elem = getById("history_list");
                for (var i =0; i < history.length; i++) {
                	var list_member = document.createElement("li");
                	
                	var aTag = document.createElement("a");
                	aTag.setAttribute("href", "");
                	var data = document.createTextNode("You requested for a cab from " + history[i].request_location + " to " + history[i].request_destination + " On " + history[i].request_date
                			+ ", the driver was " + history[i].driver); //+ " to " + history[i].request_destination + brk + "On " history[i].created + ", the driver was " + history[i].driver);
                	
                	list_member.appendChild(data);
//                	aTag.appendChild(data);
                	history_elem.appendChild(list_member);
                }
                
//                history_elem.innerHTML = history[0].request_location;
                
                window.location.href = passenger_url;
            }
            else {
                var error = "Something went wrong";
                getError("request_error", error)
            }
            
        }
    }
    var url = "/history?phone_number=" + number.value;
    xhttp.open('GET', url, true);
    xhttp.send();
}

function createHistoryElement() {
	var history_elem = getById("history_list");
	var list_member = document.createElement("li");
}

function sendFeedback() {
	var price_value = getRateValue ("price");
	var punctuality_value = getRateValue ("punctuality");
	var security_value = getRateValue ("security");
	var care_value = getRateValue ("customercare");
	var standard_value = getRateValue ("standard");
	
	var text_feedback = getById("text_feedback").value;
	
	if (price_value || punctuality_value || security_value || care_value || standard_value || text_feedback && number.value) {
		xhttp.onreadystatechange = function() {
	        if (xhttp.readyState == 4 && xhttp.status == 200) {
//	          alert(xhttp.readyState + " " + xhttp.status)
	            var resp = xhttp.responseText;
//	            alert(resp);
	            if (resp === "successful") {
	                var current_url = window.location.href;
	                var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#feedback-thanks";
	                
	                window.location.href = passenger_url;
	            }
	            else {
	            	var error = "Could not connect to the server";
		            getError("feedback_error", error)
	            }
	            
	        }
	        else{
	        	
	        }
	    }
	    var url = "/feedback?phone_number=" + number.value + "&price_rating=" + price_value + "&punctuality_rating=" + punctuality_value + "&security_rating=" + security_value + "&care_rating=" + care_value + "&standard_rating=" + standard_value + "&message=" + text_feedback;
	    xhttp.open('POST', url, true);
	    xhttp.send();
	}
	else {
		var error = "No feedback chosen or entered to send";
        getError("feedback_error", error)
	}
}

function getRateValue(name) {
var checks = document.getElementsByName(name);
var value;
	
	for (var i = 0; i < checks.length; i ++) {
		if (checks[i].checked) {
			value = checks[i].value;
			break;
		}
		else {
			value = 0;
		}
	}
	return value;
}









