rendererOptions = {
    draggable: true,
    preserveViewport: false
};
var directionsDisplay =
    new google.maps.DirectionsRenderer(rendererOptions);
var directionsService =
    new google.maps.DirectionsService();
var map;

function test_external() {
    alert('test');
}
