var port = location.hash.substring(1);


function runApp() {
    var socket = new WebSocket("ws://10.0.1.170:"+port, "base64");

    socket.onopen = function(event) {
        document.getElementById("status").innerText = "Connected";
    }

    socket.onmessage = function(event) {
        var message = JSON.parse(atob(event.data));
        setTimeout(function(color) {
            document.getElementById("screen").style.backgroundColor = color;
        }, message[1], message[0]);
    }

    socket.onclose = socket.onerror = function(event) {
        document.backgroundColor = "#000";
        document.getElementById("status").innerText = "Reconnecting...";
        setTimeout(runApp, 500);
    }
}

runApp();
