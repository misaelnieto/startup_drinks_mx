var map = null;
var marker = null;

function initializeMap() {
    var lat_input = document.getElementById('form-widgets-latitude');
    var lon_input = document.getElementById('form-widgets-longitude');
    var latlng;

    if (lat_input.value === '' && lon_input.value === '') {
        latlng = new google.maps.LatLng(20.68017, -101.35437000000002);
    } else {
        latlng = new google.maps.LatLng(lat_input.value, lon_input.value);
    }

    var myOptions = {
        zoom: 4,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };


    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    marker = new google.maps.Marker({
        position: latlng,
        draggable: true,
        map: map,
        title:"Mueve el marcador para seleccionar la posicion del evento"
    });
    google.maps.event.addListener(marker, 'mouseup', function(evt) {
        lat_input.value = evt.latLng.lat();
        lon_input.value = evt.latLng.lng();
    });

}

$(document).ready(function(){
    initializeMap();
});