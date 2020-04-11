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

### Relay (i.e., server-side magic)

A Python script that receives commands from the controller app and forwards them onto the clients.
This exists for a few reasons:

* Punch through NATs - don't worry about port-forwarding the controller app
* Allow for multiple controller app instances to coexist
* Reduce the load on the controller app

### Controller App

Receives signals from some device (computer keyboard, joystick, MIDI port, etc), maps them to colors, and forwards the colors to the relay.
Multiple versions are planned for different input channels.

