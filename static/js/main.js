var map;
var directions;

$(function () {
    //    initMap();


});

$('#mapping').click(() => {
    //    renderMap();
    dispRoute();
});

$(window).on('load', () => {
    console.log('onload')
    if (GBrowserIsCompatible()) {
        map = new GMap2(document.getElementById("map_canvas"));
        map.setCenter(new GLatLng(35.681379, 139.765577), 13);

        directions = new GDirections(map, document.getElementById('route'));
    }

    // LIFF
    liff.init(function (data) {
        alert(data)
        initializeApp(data);
    });
})

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

    directions.clear();

    str = 'from: ' + from + ' to: ' + to;
    directions.load(str, { locale: 'ja_JP' });
}

function initializeApp(data) {
    document.getElementById('languagefield').textContent = data.language;
    document.getElementById('viewtypefield').textContent = data.context.viewType;
    document.getElementById('useridfield').textContent = data.context.userId;
    document.getElementById('utouidfield').textContent = data.context.utouId;
    document.getElementById('roomidfield').textContent = data.context.roomId;
    document.getElementById('groupidfield').textContent = data.context.groupId;
}