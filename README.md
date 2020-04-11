# Vibrance
##### Audience-based concert lighting.

Vibrance takes advantage of the smartphone in everyone's pocket to create massively interactive lighting experiences for concerts and other events.
Each user loads a webpage on their device, someone runs the controller software on a laptop, and Vibrance takes care of the rest.


## Current Status

This is **not ready for use.** The protocol for the relay/client is unstable, latency is still being reduced, etc.
The code also hardcodes in my relay server hostname (plz no hax), so getting it up and running might be hard.
It's lacking some *very important* features like a graphical controller app.
Finally, it hasn't been tested nearly enough. This might all just break the moment it's used in production.
(If all that doesn't convince you to not use this code yet, I don't know what will.)

## Functional Parts

### Website (i.e., client software)

Static HTML/CSS/JS. Can be hosted anywhere (although if hosted over HTTPS, the relay must support HTTPS.)
This is the software that runs on the smartphones; it establishes a connection to the relay, reads in color data, and displays it.

This can be found in the `client` directory.
`index.html` is the landing page, `selector.html` allows the user to choose which part of the room they're in,
and `app.html` is the part that changes color.

### Relay (i.e., server-side magic)

A Python script that receives commands from the controller app and forwards them onto the clients.
This exists for a few reasons:

* Punch through NATs - don't worry about port-forwarding the controller app
* Allow for multiple controller app instances to coexist
* Reduce the load on the controller app

This can be found at `relay/relay.py`.

### Controller App

Receives signals from some device (computer keyboard, joystick, MIDI port, etc), maps them to colors, and forwards the colors to the relay.
Multiple versions are planned for different input channels.

The base python lib is at `controller/controller.py`, and several other examples (e.g. `midi_controller.py`, `pygame_controller.py`) are present as well. No GUI yet though.

## Messages (i.e., the protocols between the controller, relay, and clients)

Messages use JSON in order to be extensible in the future.
A basic message from the relay to a client looks like this:

```
{
    "color":"00FF00", // optional, changes the color of the client
    "delay":0,        // optional, delay in ms before the color change occurs
    "duration":1000,  // optional, duration that the color is on
                      // (after this it switches to black)
    "motd":"Welcome"  // optional, message to display on the user's screen
}
```

Messages from the controller to the relay take the form
```
{"9001": [message as described above] , "9002": [message as described above], [etc.] }
```

Each number (9001, 9002, etc.) addresses only clients connected to that port
(clients who selected different zones in the room connect to different ports).
A message from the controller can update clients on one port, multiple ports, all ports, or no ports.
