var port = location.hash.substring(1);


function runApp() {
    var socket = new WebSocket("ws://10.0.1.170:"+port, "binary");
    socket.binaryType = "arraybuffer";

    socket.onopen = function(event) {
        document.getElementById("status").innerText = port+" OK";

        function sendAcknowledges() {
            if (socket) {
                socket.send("OK");
                setTimeout(sendAcknowledges, 1000);
            }
        }
        sendAcknowledges();
    }

    socket.onmessage = function(event) {
        //console.log(event.data)
        var decodedString = String.fromCharCode.apply(null, new Uint8Array(event.data));
        var message = JSON.parse(decodedString);
        setTimeout(function(color) {
            document.getElementById("screen").style.backgroundColor = color;
        }, message[1], message[0]);
    }

    socket.onclose = function(event) {
        socket = null;
        document.getElementById("screen").style.backgroundColor = "#000";
        document.getElementById("status").innerText = "RECONN";
        setTimeout(runApp, 500);
    }
}

runApp();
