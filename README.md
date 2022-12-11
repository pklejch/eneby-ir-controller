# Eneby 20 IR controller

## The Problem
I watch quite a lot of movies and TV shows on the PS5. My setup is PS5 -> HDMI -> PC monitor -> 3.5mm Jack -> Eneby 20.

That worked fine, but I missed the option to control the volume wirelessly. So I bought the [PS5 Media Remote](https://www.playstation.com/en-us/accessories/media-remote/) which has dedicated volume buttons in hope to finally control the volume of PS5.

But after I bought it, I found found out, that the volume buttons use IR and do not control the PS5, but rather your TV! It turns out that PS5 does not have any master volume, you have to control the volume at the output (TV, soundbar, ...).

## The Solution
**Slap the microcontroller with IR receiver to the IKEA Eneby 20 and control the speaker using PS5 Media Remote.**

I am primarily Python programmer so I went with the MicroPython and ESP32.

### Required parts
* ESP32 (or similar microcontroller), I used the Espressif ESP32-WROOM-32
* IR receiver, I used the VS1838B
* Soldering iron, solder, wires, screwdriver, ...

### MicroPython
* You have to flash the board with MicroPython, see the [documentation](https://docs.micropython.org/en/latest/esp32/quickref.html)
* For the IR receiver part, I used [micropython_ir](https://github.com/peterhinch/micropython_ir) library which made receiving IR messages from the remote very simple.
* My glue [code](https://github.com/pklejch/eneby-ir-controller/blob/main/main.py) can be seen in the repository.
* We map the volume up and down buttons to increase and decrease the volume, obviously. Furthermore I used the "Turn on TV" button for powering on and off the Eneby 20 speaker, because I have no TV to turn on and off. Mute button kinda works, but it's done naively in software and I did not put much work in there.

### Wiring
* I went with the great project on [Espruino](https://www.espruino.com/Ikea+Eneby+Speaker+Controller) for controlling the Eneby 20.
* I just did not solder the LED pin, because I had no use for it.
* As said in the guide, the Eneby 20 already provides pins for controlling volume and power with 3.3 V, so we can just solder wires directly!

## How to do it
1. Flash the ESP32 with MicroPython
1. Tweak the [code](https://github.com/pklejch/eneby-ir-controller/blob/main/main.py), e.g. change the pins to be in line with your wiring
1. Upload the code and the library to the ESP (using Thonny, Ampy, Web REPL, ...)
1. Solder the wires to the ESP and Eneby 20
1. In the PS5 go the [Media Remote setup](https://www.playstation.com/en-us/support/hardware/ps5-media-remote-support/) and go for the "Set Up Manually" option.
1. Select TV type as Sony and use the first option (TV type), because it works with the `ir_rx.sony.SONY_12` class from the [IR library](https://github.com/peterhinch/micropython_ir)
    * You can definitely use other TV manufacturer, but you have to change the IR receiver class accordingly.
    * The [test script](https://github.com/peterhinch/micropython_ir/blob/master/RECEIVER.md) in the IR library will help you with that.
1. Now you can control the PS5 and volume on the Eneby speaker with the single remote. Enjoy !

## Credits
The IR receiver is powered by great library https://github.com/peterhinch/micropython_ir.

I took most of the code and wiring diagram from the https://www.espruino.com/Ikea+Eneby+Speaker+Controller, which just uses different board and Espruino (based on the JavaScript) to achieve essentially the same thing.