
function init() {

//  var input = /** @type {HTMLInputElement} */(document.getElementById('searchTextField'));
//  var autocomplete = new google.maps.places.Autocomplete(input);

 // autocomplete.bindTo('bounds', map);
	var input = document.getElementById('request_location');
	var input2 = document.getElementById('request_destination');
	var reserve_input = document.getElementById('reserve_location');
    var reserve_input2 = document.getElementById('reserve_destination');
	
	var options = {
	componentRestrictions: {country: 'gh'}
	};

	autocomplete = new google.maps.places.Autocomplete(input, options);
	autocomplete = new google.maps.places.Autocomplete(input2, options);
	autocomplete = new google.maps.places.Autocomplete(reserve_input, options);
    autocomplete = new google.maps.places.Autocomplete(reserve_input2, options);
	

	var map,myPosition;
	
	map = new google.maps.Map(document.getElementById('map_canvas'), {
		   
        mapTypeId: google.maps.MapTypeId.ROADMAP	
    });
   
    var directionsRenderer = new google.maps.DirectionsRenderer({
        map: map,
       
    });

    if (navigator.geolocation) {
	    
        navigator.geolocation.getCurrentPosition(function(position){
            myPosition = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
                                                
			map.setCenter(myPosition)
			map.setZoom(17)
			var options = {
			  position: myPosition
			};
			var marker = new google.maps.Marker(options);
			marker.setMap(map);
			marker.setAnimation(google.maps.Animation.BOUNCE);	
		
        });
        
    }
    
    var geocoder = new google.maps.Geocoder();
    var center = new google.maps.LatLng(-34.397, 150.644);
    var request = {
    	      address: "-34.397, 150.644"
    	    };
	
    geocoder.geocode({'latLng': myPosition}, function(results, status) {
    	if (status == google.maps.GeocoderStatus.OK) {
    		if (results[0]) {
    			input.value = results[1].formatted_address;
    			window.console.log(results[0] + " " + myPosition);
    			}
    		else {
    			window.console.log("nothing found");
    		}
    	}
    	else {
    		window.console.log("nothing found for " + myPosition + " " + status);
    	}
    });
    
//    geocoder.geocode(request, function(results, status) {
//        if (status == google.maps.GeocoderStatus.OK) {
//            position = results[0].geometry.location
//            window.console.log(position.formatted_address + " "  + status);
//        } else {
//          window.console.log('failed to geocode address: '  + status);
//        }
//      });
}






