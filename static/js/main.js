rendererOptions = {
    draggable: true,
    preserveViewport: false
};
var directionsDisplay =
    new google.maps.DirectionsRenderer(rendererOptions);
var directionsService =
    new google.maps.DirectionsService();
var map;

$(window).on('load', function () {

    // init で初期化。基本情報を取得。
    // https://developers.line.me/ja/reference/liff/#initialize-liff-app
    liff.init(function (data) {

        getProfile();
        initializeApp(data);
    });
});

// プロファイルの取得と表示
function getProfile() {
    // https://developers.line.me/ja/reference/liff/#liffgetprofile()
    liff.getProfile().then(function (profile) {
        document.getElementById('useridprofilefield').textContent = profile.userId;
        document.getElementById('displaynamefield').textContent = profile.displayName;

        var profilePictureDiv = document.getElementById('profilepicturediv');
        if (profilePictureDiv.firstElementChild) {
            profilePictureDiv.removeChild(profilePictureDiv.firstElementChild);
        }
        var img = document.createElement('img');
        img.src = profile.pictureUrl;
        img.alt = "Profile Picture";
        img.width = 200;
        profilePictureDiv.appendChild(img);

        document.getElementById('statusmessagefield').textContent = profile.statusMessage;
    }).catch(function (error) {
        window.alert("Error getting profile: " + error);
    });
}

function initializeApp(data) {
    document.getElementById('languagefield').textContent = data.language;
    document.getElementById('viewtypefield').textContent = data.context.viewType;
    document.getElementById('useridfield').textContent = data.context.userId;
    document.getElementById('utouidfield').textContent = data.context.utouId;
    document.getElementById('roomidfield').textContent = data.context.roomId;
    document.getElementById('groupidfield').textContent = data.context.groupId;
}


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
