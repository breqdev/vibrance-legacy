const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);


function runApp() {
    var socket = new WebSocket("wss://"+urlParams.get("host")+":"+urlParams.get("port"), "binary");
    socket.binaryType = "arraybuffer";

    socket.onopen = function(event) {
        document.getElementById("status").innerText = "Connected";

        function sendAcknowledges() {
            if (socket) {
                socket.send("OK");
                console.log("ACK sent")
                setTimeout(sendAcknowledges, 1000);
            }
        }
        sendAcknowledges();
    }

    socket.onmessage = function(event) {
        var decodedString = String.fromCharCode.apply(null,
                                                new Uint8Array(event.data));
        var message = JSON.parse(decodedString);
        console.log(message);
        var color = message["color"];
        var delay = message["delay"] | 0;
        var duration = message["duration"];
        var motd = message["motd"];

        if (typeof color !== "undefined") {
            setTimeout(function(color) {
                document.getElementById("screen").style.backgroundColor = "#"+color;
            }, delay, color);

            if (duration > 0) {
                setTimeout(function() {
                    document.getElementById("screen").style.backgroundColor = "#000";
                }, delay+duration);
            }
        }

        if (typeof motd !== "undefined") {
            document.getElementById("status").innerText = motd;
        }

        if (color === "000000" || color === "000") {
            document.getElementById("status").style.color = "#FFF";
        } else {
            document.getElementById("status").style.color = "#000";
        }
    }

    socket.onclose = function(event) {
        socket = null;
        document.getElementById("screen").style.backgroundColor = "#000";
        document.getElementById("status").innerText = "Reconnecting";
        setTimeout(runApp, 1000); // Try again in 1s
    }
}

runApp();
