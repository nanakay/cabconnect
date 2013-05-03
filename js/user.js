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
//	              login_btn.href = passenger_url;
//	              alert(login_btn.href);
//	              if (current_url == "file:///android_asset/www/index.html#login") {
//	                    login_btn.click();
////	                    alert("true");
//	                }
//	                else {
//	                    evt.preventDefault();
//	                    alert("false");
//	                }
//	              var button = evt.target;
//	              button = ascendDom(button, 'a');
//	              button.href = "#start-page";
//	              console.log(button);
//	              $('#login_btn').click();
	                
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
	    xhttp.open('GET', url, true);
	    xhttp.send();
}

//function Navigate (evt) {
//	var el = evt.target;
//	var link = ascendDom(el, "a");
//	var url = link.href;
//	
////	console.log(url);
//	window.location = url;
//}

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
			if (xhttp.readyState == 4 && xhttp.status == 200) {
				var resp = xhttp.responseText;
				
				if (resp.indexOf('failed') != -1) {
					var error = resp;
					getById("error").style.display = "block";
					getById("error").innerHTML = error;
				}
				else {
//					data = resp.split(",");
//					phone_number = data[0];
//					password = data[1];
//					email = data[2];
//					finalCreateUser(phone_number, password, email);
					var current_url = window.location.href;
					var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#start_page";
//					alert(passenger_url);
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
		var url = '/createuser?phone_number=' + phone_number + '&password=' + password + "&email=" + email + "&first_name=" + first_name + "&last_name=" + last_name;
		xhttp.open('GET', url, true);
		xhttp.send();
	}
	else {
		var error = "All data are required please";
		getById("error").style.display = "block";
		getById("error").innerHTML = error;
	}
//	console.log(phone_number, password, verify_password, email);
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
    time_frame = getById("timeframe").value;
    time_label = getById("timeframe_option").value;
    other_info = getById("other_info").value;
    
    timeFrame = time_frame + " " + time_label;
    
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
        var url = '/request?current_location=' + current_location + '&destination=' + destination + "&time=" + pickup_time + "&timeframe=" + timeFrame + "&phone_number=" + number.value + "&other_info=" + other_info;
        alert (url);
        xhttp.open('GET', url, true);
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








