//var map;
//var directions;
rendererOptions = {
    draggable: true,
    preserveViewport: false
};
var directionsDisplay =
    new google.maps.DirectionsRenderer(rendererOptions);
var directionsService =
    new google.maps.DirectionsService();
var map;

$('#mapping').click(() => {
    dispRoute();
});

function initialize() {
    var zoom = 7;
    var mapTypeId = google.maps.MapTypeId.ROADMAP

    var opts = {
        zoom: zoom,
        mapTypeId: mapTypeId
    };
    map = new google.maps.Map
        (document.getElementById("map_canvas"), opts);
    directionsDisplay.setMap(map);

    google.maps.event.addListener(directionsDisplay,
        'directions_changed', function () {
        });
    calcRoute("東京", "名古屋");
}


function calcRoute(src, dst) {
    var request = {
        origin: src,
        destination: dst,
        travelMode: google.maps.DirectionsTravelMode.DRIVING,
        unitSystem: google.maps.DirectionsUnitSystem.METRIC,
        optimizeWaypoints: true,
        avoidHighways: false,
        avoidTolls: false
    };
    directionsService.route(request,
        function (response, status) {
            if (status == google.maps.DirectionsStatus.OK) {
                directionsDisplay.setDirections(response);
            }
        });
}

$(window).on('unload', () => {
    console.log('unload')
    GUnload()
})



function initMap() {
    console.log('initMap')
    var opts = {
        zoom: 15,
        center: new google.maps.LatLng(35.1239654, 136.9417741)
    };
    var map = new google.maps.Map(document.getElementById("map"), opts);
    $('#msg').text('堀田')
}

function renderMap() {
    console.log('renderMap')
    var src = $('#src').text()
    var dst = $('#dst').text()
    var opts = {
        zoom: 15,
        center: new google.maps.LatLng(35.1253694, 136.9073667)
    };
    var map = new google.maps.Map(document.getElementById("map"), opts);
    $('#msg').text('熱田神宮')
}

function dispRoute() {
    console.log('dispRoute')
    var from = $('#src').val()
    var to = $('#dst').val()
    console.log(from)
    console.log(to)

    calcRoute(from, to)
}
