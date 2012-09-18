var map = null;
var infoWindow = null;

function openInfoWindow(marker) {
    var markerLatLng = marker.getPosition();
    infoWindow.setContent([
        '&lt;b&gt;La posicion del marcador es:&lt;/b&gt;&lt;br/&gt;',
        markerLatLng.lat(),
        ', ',
        markerLatLng.lng(),
        '&lt;br/&gt;&lt;br/&gt;Arr&amp;aacute;strame y haz click para actualizar la posici&amp;oacute;n.'
    ].join(''));
    infoWindow.open(map, marker);
}

function initializeMap() {
    var latlng = new google.maps.LatLng(20.68017, -101.35437000000002);

    var myOptions = {
        zoom: 4,
        center: latlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
    map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
    // infoWindow = new google.maps.InfoWindow();

    // var marker = new google.maps.Marker({
    //     position: latlng,
    //     draggable: true,
    //     map: map,
    //     title:&quot;Sede de StartUpDrinks&quot;
    // });

    // google.maps.event.addListener(marker, 'click', function(){
    //     document.location = 'http://puebla.startupdrinks.mx';
    // });
}

$(document).ready(function(){
    initializeMap();
});