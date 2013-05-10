//$("document").ready(function(){
//    $("#login_btn").on("click",function(evt){
////        alert("Logging in");
//        verify_user(evt);
//        return false;
//    });
//});


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
	var login_btn = document.getElementById("login_btn");
	login_btn.onclick = verify_user;
	
	var signup_btn = getById("signup_btn");
	signup_btn.onclick = createUser;
	
//	var a = getById("request_btn").onclick = requestCab();
	
}

function verify_user(evt) {
    //alert("Verifying User");
	evt.preventDefault();
	var phonenumber = document.getElementById('in_phone_number').value;
	var password = document.getElementById('in_password').value;
//	console.log(phonenumber, password);
	if (phonenumber && password){
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
//	              if (current_url == "file:///android_asset/www/disp-login.html#login") {
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
	    var url = 'http://cabkonekt.appspot.com/verifyuser?phonenumber=' + phonenumber + '&password=' + password;
	    xhttp.open('GET', url, true);
	    xhttp.send();
	}
	else {
	    var error = "Both phone number and password required";
        var el = document.getElementById("login_error");
        el.innerHTML = error;
        el.style.display = "block";
	}
	
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
		
		xhttp.onreadystatechange = function() {
			if (xhttp.readyState == 4 && xhttp.status == 200) {
				var resp = xhttp.responseText;
				
				if (resp.indexOf('failed') != -1) {
					var error = resp;
					getById("error").style.display = "block";
					getById("error").innerHTML = error;
				}
				else {
	                number.value = phonenumber;
	                firstName.value = resp;
	                
	                getByID("welcome_user").value + " " + firstName;
					var current_url = window.location.href;
					var passenger_url = current_url.substring(0, current_url.lastIndexOf("/"))+ "#start-page";
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
		var url = 'http://cabkonekt.appspot.com/createuser?phone_number=' + phone_number + '&password=' + password + "&email=" + email + "&first_name=" + first_name + "&last_name=" + last_name;
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
    //          alert(xhttp.readyState + " " + xhttp.status)
                var resp = xhttp.responseText;
                
                if (resp === "successful") {
                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#request-confirmation";
                    window.location.href = passenger_url;
                }
                else {
                    var error = "Something went wrong";
                    var error_el = getById("request_error");
                    error_el.innerHTML = error;
                    error_el.style.display = "block"
                }
                
            }
        }
        var url = 'http://cabkonekt.appspot.com/request?option=request_cab' + '&current_location=' + current_location + '&destination=' + destination + "&time=" + pickup_time + "&timeframe=" + timeFrame + "&phone_number=" + number.value + "&other_info=" + other_info;
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

function reserveCab() {
    alert("I'm in reserve");
    current_location = getById("reserve_location");
    destination = getById("reserve_destination");
    from_date = getById("from_date");
    to_date = getById("to_date");
    pickup_time = getById("reserve_pickup_time");
    to_time = getById("reserve_to_time");
    passengers = getById("total_passengers");
    other_info = getById("reserve_other_info");
    
    if (current_location && destination && from_date && to_date && pickup_time && to_time && passengers) {
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
    //          alert(xhttp.readyState + " " + xhttp.status)
                var resp = xhttp.responseText;
                
                if (resp === "successful") {
                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url.lastIndexOf("#"))+ "#reserve-confirmation";
                    window.location.href = passenger_url;
                }
                else {
                    var error = "Something went wrong";
                    getError("request_error", error)
                }
                
            }
        }
        var url = 'http://cabkonekt.appspot.com/request?option=reserve_cab' + '&current_location=' + current_location + '&destination=' + destination + "&time=" + pickup_time + "&timeframe=" + timeFrame + "&phone_number=" + number.value + "&other_info=" + other_info;
        alert (url);
        xhttp.open('GET', url, true);
        xhttp.send();
    }
    else {
        var error = "Some required data have not been provided";
        getError("reserve_error", error);
    }
    
}

function getError(elId, error) {
    var error_el = getById(elID); 
    error_el.innerHTML = error;
    error_el.style.display = "block";
}

