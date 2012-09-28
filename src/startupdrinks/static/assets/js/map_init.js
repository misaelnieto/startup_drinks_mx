$(document).ready(function(){
    'use strict';

    $.getJSON(base_url + '/map/places_json', function(data) {
        var map;
        var myOptions = {
            zoom: 4,
            center: new google.maps.LatLng(20.68017, -101.35437000000002),
            mapTypeId: google.maps.MapTypeId.ROADMAP
        };
        map = new google.maps.Map(
            document.getElementById("map_canvas"),
            myOptions
        );

        $.each(data, function(indx, place){
            var infoWindow = new google.maps.InfoWindow();
            var marker = new google.maps.Marker({
                animation: google.maps.Animation.DROP,
                map: map,
                position: new google.maps.LatLng(place.latitude, place.longitude),
                title:"Click para abrir"
            });

            google.maps.event.addListener(marker, 'click', function() {
                infoWindow.close();
                infoWindow.setContent('<h3>' + place.title + '</h3><p>' + place.description +'</p><p><a href="' + place.url + '">' + place.url + '<a/></p>');
                infoWindow.open(map, marker);
            });
        });
    });
});