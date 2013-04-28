var xhttp;
if (window.XMLHttpRequest) {
	xhttp = new XMLHttpRequest();
}
else {
	xhttp = new ActiveXObject('Microsoft.XMLHTTP');
}

function initAll() {
	var login_btn = document.getElementById("login_btn");
	login_btn.onclick = verify_user;
}

function verify_user(evt) {
	evt.preventDefault();
	var phonenumber = document.getElementById('phoneNumber').value;
	var password = document.getElementById('password').value;
//	console.log(phonenumber, password);
	
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			var resp = xhttp.responseText;
			if (resp.indexOf('success') != -1) {
				var current_url = window.location.href;
				var passenger_url = current_url.substring(0, current_url.lastIndexOf("/"))+ "/passenger";
				window.location = passenger_url;
			} else {
				document.getElementById("error").style.display = "block";
				
			}
		}
	}
	var url = '/verifyuser?phonenumber=' + phonenumber + '&password=' + password;
	xhttp.open('GET', url, true);
	xhttp.send();
}

