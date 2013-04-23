$(document).ready(function () {
            $('.dropdown-toggle').dropdown();
        });

$(document).ready(function () {
    $('label.tree-toggler').click(function () {
        $(this).parent().children('ul.tree').toggle(300);
    });
});


function initialize() {

	  var input = /** @type {HTMLInputElement} */(document.getElementById('searchTextField'));
	  var autocomplete = new google.maps.places.Autocomplete(input);

	  autocomplete.bindTo('bounds', map);

	}
