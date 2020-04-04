#!/bin/bash

# Start HTML server
xdotool key ctrl+shift+t
sleep 0.1
xdotool type "python3 -m http.server 9000"
sleep 0.1
xdotool key Return

# Start Relay
xdotool key ctrl+shift+t
sleep 0.1
xdotool type "python3 relay.py"
sleep 0.1
xdotool key Return

# Start Controller
xdotool key ctrl+shift+t
sleep 0.1
xdotool type "python3 fadetest.py"
sleep 0.1
xdotool key Return
