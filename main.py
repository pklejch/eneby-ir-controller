"""Control IKEA Eneby 20 speaker using IR receiver."""

import machine
import ir_rx.sony
import time


INTEGRATED_LED_PIN = 2
VOLUME_DOWN_PIN = 19
VOLUME_UP_PIN = 21
POWER_PIN = 22
IR_PIN = 23


def boot_sequence():
    """Blink LED on startup."""
    led = machine.Pin(INTEGRATED_LED_PIN, machine.Pin.OUT)

    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)
    led.on()
    time.sleep(0.1)
    led.off()


class Receiver:
    """Handle IR messages."""

    def __init__(self, eneby_controller):
        self.eneby_controller = eneby_controller

        self.led = machine.Pin(INTEGRATED_LED_PIN, machine.Pin.OUT)

    def _delay(self):
        """Blink when received IR signal, also ignore rest of the IR data."""
        self.led.on()
        time.sleep(0.1)
        self.led.off()

    def _handle_volume_up(self):
        self._delay()
        self.eneby_controller.volume_up()

    def _handle_volume_down(self):
        self._delay()
        self.eneby_controller.volume_down()

    def _handle_power_button(self):
        self._delay()
        self.eneby_controller.press_power()

    def _handle_mute(self):
        self._delay()
        self.eneby_controller.mute()

    def _handle_unknown_action(self):
        print('unknown code received')

    def handle_button(self, data, addr, ctrl):
        CODE_TO_FUNCTION = {
               18: self._handle_volume_up,  # 0x12
               19: self._handle_volume_down,  # 0x13
               20: self._handle_mute,  # 0x14
               21: self._handle_power_button,  # 0x15
        }

        CODE_TO_FUNCTION.get(data, self._handle_unknown_action)()


class EnebyController:
    VOLUME_PATTERN = [(0, 0), (1, 0), (1, 1), (0, 1)]
    DEFAULT_VOLUME = 4

    def __init__(self, power_button_pin, volume_up_pin, volume_down_pin):
        self.power_button_pin = power_button_pin
        self.volume_up_pin = volume_up_pin
        self.volume_down_pin = volume_down_pin

        self.current_volume = self.DEFAULT_VOLUME
        self.old_volume = self.current_volume

    def press_power(self):
        """Simulate pressing a button."""
        self.power_button_pin = machine.Pin(POWER_PIN, machine.Pin.OUT)

        self.power_button_pin.off()
        time.sleep(0.2)
        self.power_button_pin.on()

        # stop forcing state on power pin so it can be powered off by pressing physical button
        self.power_button_pin = machine.Pin(POWER_PIN, machine.Pin.IN)

    def _move_knob(self, index, direction, offset):
        """Simulate moving a know in the given direction."""
        new_index = (index + (direction * offset)) % 4
        value_volume_down, value_volume_up = self.VOLUME_PATTERN[new_index]

        self.volume_down_pin = machine.Pin(VOLUME_DOWN_PIN, machine.Pin.OUT)
        self.volume_up_pin = machine.Pin(VOLUME_UP_PIN, machine.Pin.OUT)

        self.volume_down_pin.value(value_volume_down)
        self.volume_up_pin.value(value_volume_up)

    def _set_volume(self, direction):
        self.current_volume += direction

        self.volume_down_pin = machine.Pin(VOLUME_DOWN_PIN, machine.Pin.IN)
        self.volume_up_pin = machine.Pin(VOLUME_UP_PIN, machine.Pin.IN)

        value_volume_down = self.volume_down_pin.value()
        value_volume_up = self.volume_up_pin.value()

        index = self.VOLUME_PATTERN.index((value_volume_down, value_volume_up))

        # make 4 turns in selected direction
        self._move_knob(index, direction, 0)
        time.sleep(0.09)
        self._move_knob(index, direction, 1)
        time.sleep(0.09)
        self._move_knob(index, direction, 2)
        time.sleep(0.09)
        self._move_knob(index, direction, 3)

        # stop forcing pins
        self.volume_down_pin = machine.Pin(VOLUME_DOWN_PIN, machine.Pin.IN)
        self.volume_up_pin = machine.Pin(VOLUME_UP_PIN, machine.Pin.IN)

    def volume_up(self):
        self._set_volume(1)

    def volume_down(self):
        self._set_volume(-1)

    def mute(self):
        if self.current_volume > 0:
            self.old_volume = self.current_volume
            for _ in range(self.current_volume):
                self._set_volume(-1)
        else:  # unmute
            for _ in range(self.old_volume):
                self._set_volume(1)


def main():
    power_button_pin = machine.Pin(POWER_PIN, machine.Pin.OUT)
    volume_up_pin = machine.Pin(VOLUME_UP_PIN, machine.Pin.IN)
    volume_down_pin = machine.Pin(VOLUME_DOWN_PIN, machine.Pin.IN)

    eneby_controller = EnebyController(power_button_pin, volume_up_pin, volume_down_pin)
    receiver = Receiver(eneby_controller)
    ir = ir_rx.sony.SONY_12(machine.Pin(IR_PIN, machine.Pin.IN), receiver.handle_button)


boot_sequence()
main()
