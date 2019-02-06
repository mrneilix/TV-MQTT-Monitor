# TV-MQTT-Monitor
I have no experience with python, so this is probably pretty unintuitive, pieced together from random things I found online.

please comment if you find any improvements or anything... I really have very little experience.

It polls my TV IP to see if it's on, every 30 seconds, and posts to my MQTT server on HASS
I also set it so when I turn the TV on through HASS, it stops the python script from running for 60 seconds, so it can stabilize, then reinitialize it (I tried to send a command to control the TV through MQTT, but it kept reverting back to the previous state without disabling it).
