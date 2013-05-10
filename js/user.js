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
} else {
    xhttp = new ActiveXObject('Microsoft.XMLHTTP');
}

var number;
var firstName;
function initAll() {
    number = document.getElementById("phone_number");
    firstName = getById("firstName");
    var login_btn = document.getElementById("login_btn");
    login_btn.onclick = verify_user;
    //	
    var signup_btn = getById("signup_btn");
    signup_btn.onclick = createUser;
    
    setInterval(checkHistory, 5000);
}

function verify_user(evt) {
    // evt.preventDefault();
    var phonenumber = document.getElementById('in_phone_number').value;
    var password = document.getElementById('in_password').value;
    // console.log(phonenumber, password);
    if (phonenumber && password) {
        xhttp.onreadystatechange = function() {
            // alert(xhttp.readyState + " Status: " + xhttp.status);
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                var resp = xhttp.responseText;
                if (resp.indexOf('failed') != -1) {

                    var error = "Username or password incorrect";
                    var el = document.getElementById("login_error");
                    el.innerHTML = error;
                    el.style.display = "block";
                    evt.preventDefault();

                } else {

                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url.lastIndexOf("#")) + "#start_page";
                    number.value = phonenumber;
                    firstName.value = resp;

                    getById("welcome_user").innerHTML = "Welcome "+ firstName.value;

                    window.location.replace(passenger_url);
                    // window.location.href = passenger_url;
//                    checkHistory();
                }
            }
        }
        var url = '/verifyuser?phonenumber='
                + phonenumber + '&password=' + password;
        xhttp.open('POST', url, true);
        xhttp.send();
    } else {
        var error = "Phone number and password required";
        // getError("login_error");
        alert(error);
        navigator.notification.beep(2);
        evt.preventDefault();
    }

}

function loginNavigate() {
    window.location.replace("http://localhost:9082/signup#login");
}

function signupNavigate() {
    window.location.replace("http://localhost:9082/signup#signup");
}

function createUser(evt) {
//    evt.preventDefault();
    var phone_number = getById("signup_phoneNumber").value;
    var password = getById("signup_password").value;
    var verify_password = getById("verify_password").value;
    var email = getById("signup_email").value;
    var first_name = getById("signup_fName").value;
    var last_name = getById('signup_lName').value;

    if (phone_number && password && verify_password && email && first_name && last_name) {
        // alert("data received");
        if (checkNumber(phone_number) && getEqualPassword(password, verify_password) && validateEmail(email)) {
            xhttp.onreadystatechange = function() {
                if (xhttp.readyState == 4 && xhttp.status == 200) {
                    var resp = xhttp.responseText;
                    window.console.log(resp);
                    if (resp.indexOf('failed') != -1) {
                        var error = resp;
                        getById("error").style.display = "block";
                        getById("error").innerHTML = error;
                    } else {
                        var code_entry = prompt("A verification code has been sent to you as text. Please enter code to complete signup");
                        var count =1;
                        if (code_entry == resp) {
                            verifyNumber(phone_number, password, first_name,
                                    last_name, email);
                        }
                        if (code_entry != resp && count <= 3) {
                            code_entry = prompt("Wrong code entered, try again.");
                        }
                        
                        if (count > 3) {
                            alert("Sorry you have exceeded your number of tries.");
                        }
                    }
                }
            }
            var url = '/createuser?option=verify_number'
                    + "&phone_number="
                    + phone_number
                    + "&first_name="
                    + firstName.value;
            xhttp.open('POST', url, true);
            xhttp.send();
        }
        
    } else {
        var error = "All data are required please";
        getById("error").style.display = "block";
        getById("error").innerHTML = error;
    }
    // console.log(phone_number, password, verify_password, email);
}

function getEqualPassword(password, verify) {
    if (password === verify) {
        return true;
    }
    else {
        alert("Passwords do not match");
        return false;
    }
}

function checkNumber(number) {
    if (number.length == 12 || number.length == 13) {
        return true
    }
    else {
        alert("Invalid number enterd. Check if number starts with your country code");
    }
}

function verifyNumber(phone_number, password, first_name, last_name, email) {
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
//            alert(xhttp.readyState + " " + xhttp.status)
            var resp = xhttp.responseText;
            if (resp.indexOf('failed') == -1) {
                var current_url = window.location.href;
                
                number.value = phone_number;
                firstName.value = resp;
                getById("welcome_user").innerHTML = "Welcome "+ firstName.value;
                
                var passenger_url = current_url.substring(0, current_url.lastIndexOf("#")) + "#start_page";
                window.location.replace(passenger_url);
            } else {
                // alert(resp);
                var error = "Something went wrong";
                var error_el = getById("request_error");
                error_el.innerHTML = error;
                error_el.style.display = "block"
            }

        }
    }
    var url = '/createuser?option=create_user'
            + '&phone_number=' + phone_number + '&password=' + password
            + "&email=" + email + "&first_name=" + first_name + "&last_name="
            + last_name;
    xhttp.open('POST', url, true);
    xhttp.send();

}

function validateEmail(email) {
    var atpos = email.indexOf("@");
    var dotpos = email.lastIndexOf(".");
    if (atpos < 1 || dotpos < atpos + 2 || dotpos + 2 >= email.length) {
        alert("The email entered is not valid");
        return false;
    }
    else {
        return true;
    }
}


function requestCab() {
    current_location = getById("reserve_location").value;
    destination = getById("reserve_destination").value;
    from_date = getById("from_date").value;
    to_date = getById("to_date").value;
    pickup_time = getById("reserve_pickup_time").value;
    to_time = getById("reserve_to_time").value;
    passengers = getById("total_passengers").value;
    other_info = getById("reserve_other_info").value;

    if (current_location && destination && from_date && to_date && pickup_time
            && to_time && passengers) {
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                 alert(xhttp.readyState + " " + xhttp.status)
                var resp = xhttp.responseText;
                alert(resp);
                if (resp === "successful") {
                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url
                            .lastIndexOf("#"))
                            + "#request-confirmation";
                    window.location.href = passenger_url;
                    setInterval(getUpdates, 10000);
                } else {
                    var error = "Please check your internet connection";
                    getError("request_error", error)
                }

            }
        }
        var url = '/request?current_location=' + current_location + '&destination='
                + destination + "&from_date=" + from_date + "&to_date="
                + to_date + "&reserve_pickup_time=" + pickup_time + "&to_time="
                + to_time + "&phone_number=" + number.value
                + "&total_passengers=" + passengers + "&other_info="
                + other_info;
        xhttp.open('POST', url, true);
        xhttp.send();
    } else {
        var error = "Some required data have not been provided";
        getError("request_error", error);
    }

}

function getError(elId, error) {
    var error_el = getById(elId);
    error_el.innerHTML = error;
    error_el.style.display = "block";
}

// Ajax call to get all transactions of client
function checkHistory() {
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
//             alert(xhttp.readyState + " " + xhttp.status)
            var resp = xhttp.responseText;
            if (resp != "empty") {
                var current_url = window.location.href;
                var passenger_url = current_url.substring(0, current_url
                        .lastIndexOf("#"))
                        + "#check-history";

                var history = JSON.parse(resp);
                var data = "";
                var history_elem = getById("history_list");
                for ( var i = 0; i < history.length; i++) {

                    data += "<li><p>You requested for a cab on " + history[i].request_date + "</p><br>" + "<label>From:</label>" + history[i].request_location
                    		+ "<br><label>To:</label>" + history[i].request_destination + "</li>";

                }
                window.console.log(data);
                history_elem.innerHTML = data;

            } else {
                history_elem = getById("history_list");
                var list_member = document.createElement("li");
                var data = document.createTextNode("Hi " + firsName.value
                        + ", you havn't conducted any transactions yet");
                list_member.appendChild(data);
                history_elem.appendChild(list_member);
            }

        }
    }
    var url = "/history?phone_number="
            + number.value;
    xhttp.open('GET', url, true);
    xhttp.send();
}

function createHistoryElements(date, location, destination, status) {
    var data = "<li><p>You requested for a cab on " + date + "</p><br>" + "<label>From:</label>" + location
    		+ "<label>To:</label>" + destination + "</li>";
    return data;
}

function sendFeedback() {
    var price_value = getRateValue("price");
    var punctuality_value = getRateValue("punctuality");
    var security_value = getRateValue("security");
    var care_value = getRateValue("customercare");
    var standard_value = getRateValue("standard");

    var text_feedback = getById("text_feedback").value;

    if (price_value || punctuality_value || security_value || care_value
            || standard_value || text_feedback && number.value) {
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                alert(xhttp.readyState + " " + xhttp.status)
                var resp = xhttp.responseText;
                // alert(resp);
                if (resp === "successful") {
                    var current_url = window.location.href;
                    var passenger_url = current_url.substring(0, current_url
                            .lastIndexOf("#"))
                            + "#feedback-thanks";

                    window.location.href = passenger_url;
                } else {
                    var error = "Could not connect to the server";
                    getError("feedback_error", error)
                }

            }
        }
        var url = "/feedback?phone_number="
                + number.value + "&price_rating=" + price_value
                + "&punctuality_rating=" + punctuality_value
                + "&security_rating=" + security_value + "&care_rating="
                + care_value + "&standard_rating=" + standard_value
                + "&message=" + text_feedback;
        xhttp.open('POST', url, true);
        xhttp.send();
    } else {
        var error = "No feedback chosen or entered to send";
        getError("feedback_error", error)
    }
}

function getRateValue(name) {
    var checks = document.getElementsByName(name);
    var value;

    for ( var i = 0; i < checks.length; i++) {
        if (checks[i].checked) {
            value = checks[i].value;
            break;
        } else {
            value = 0;
        }
    }
    return value;
}

function getUpdates() {
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            // alert(xhttp.readyState + " " + xhttp.status)
            var resp = xhttp.responseText;
            alert(resp);
            if (resp != "empty") {
//                var current_url = window.location.href;
//                var passenger_url = current_url.substring(0, current_url
//                        .lastIndexOf("#"))
//                        + "#request-confirmation";
//                
//                window.location.href = passenger_url;
                setInterval(getUpdates, 10000);
            } else {
                var error = "Please check your internet connection";
                getError("request_error", error)
            }

        }
    }
    var url = 'http://cabkonekt.appspot.com/update?phone_number=' + number.value;
    xhttp.open('POST', url, true);
    xhttp.send();
}
