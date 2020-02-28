# The MIT License (MIT)
#
# Copyright (c) 2018 Frank Morton for Neighborhood Makers Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`makers_remote_control`
====================================================

.. CircuitPython helper for remote controls

* Author(s): Frank Morton for Neighborhood Makers Inc

Implementation Notes
--------------------

**Hardware:**

* `Circuit Playground Express <https://www.adafruit.com/product/3333>`_
* `Mini Remote Control <https://www.adafruit.com/product/389>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://github.com/adafruit/circuitpython/releases

* Adafruit CircuitPython drivers for IR remote send and receive
  https://github.com/adafruit/Adafruit_CircuitPython_IRRemote

"""

import board
import pulseio
import adafruit_irremote

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fmorton/Makers_CircuitPython_remote_control.git"


"""
  Demo code for Circuit Playground Express:

  import time
  import makers_remote_control

  remote_control = makers_remote_control.RemoteControl(debug=False)

  while True:
      code = remote_control.code()

      if(code == remote_control.UP):
          print("Forward")
      elif(code == remote_control.DOWN):
          print("Backwards")
      elif(code == remote_control.LEFT):
          print("Left")
      elif(code == remote_control.RIGHT):
          print("Right")
      elif(code == 4):
          print("Something for Four")
      elif(code == 6):
          print("Something for Six")

      time.sleep(0.1)
"""

class RemoteControl:
    """Remote control helper class"""
    UNKNOWN = -1
    UP_ = 128
    DOWN = 129
    RIGHT = 130
    LEFT = 131
    ENTER = 132
    SETUP = 133
    STOP = 134
    BACK = 135
    VOL_MINUS = 136
    VOL_PLUS = 137
    PLAY_PAUSE = 138
    LEFT_BUTTON = 139
    RIGHT_BUTTON = 140
    MENU = 141
    CODE = {
        #  adafruit mini remote control
        53040: 0,
        63240: 1,
        30600: 2,
        46920: 3,
        55080: 4,
        22440: 5,
        38760: 6,
        59160: 7,
        26520: 8,
        42840: 9,
        24480: UP_,
        20400: DOWN,
        44880: RIGHT,
        61200: LEFT,
        28560: ENTER,
        57120: SETUP,
        40800: STOP,
        36720: BACK,
        65280: VOL_MINUS,
        48960: VOL_PLUS,
        32640: PLAY_PAUSE,

        #  lego power remote control (middle switch in position 1 (top)
        29819: LEFT_BUTTON,
        31995: LEFT_BUTTON,
        32250: RIGHT_BUTTON,
        30074: RIGHT_BUTTON,
        41720: LEFT,
        43640: LEFT,
        46072: RIGHT,
        47992: RIGHT,
        41977: DOWN,
        43897: DOWN,
        45817: UP_,
        47737: UP_,

        #  lego power remote control (middle switch in position 2)
        30059: LEFT_BUTTON,
        32235: LEFT_BUTTON,
        29802: RIGHT_BUTTON,
        31978: RIGHT_BUTTON,
        41960: LEFT,
        43880: LEFT,
        45800: RIGHT,
        47720: RIGHT,
        46057: UP_,
        47977: UP_,
        41705: DOWN,
        43625: DOWN,

        #  lego power remote control (middle switch in position 3)
        32475: LEFT_BUTTON,
        30299: LEFT_BUTTON,
        30554: RIGHT_BUTTON,
        32730: RIGHT_BUTTON,
        41176: LEFT,
        43096: LEFT,
        45528: RIGHT,
        47448: RIGHT,
        45273: UP_,
        47193: UP_,
        41433: DOWN,
        43353: DOWN,

        #  lego power remote control (middle switch in position 4 (bottom)
        30539: LEFT_BUTTON,
        32715: LEFT_BUTTON,
        30282: RIGHT_BUTTON,
        32458: RIGHT_BUTTON,
        41416: LEFT,
        43336: LEFT,
        45256: RIGHT,
        47176: RIGHT,
        45513: UP_,
        47433: UP_,
        41161: DOWN,
        43081: DOWN,

        #  apple tv remote control (old style silver)
        17834: ENTER,
        34218: PLAY_PAUSE,
        49066: MENU,
        61354: LEFT,
        8106: RIGHT,
        12202: UP_,
        20394: DOWN,

        # apple tv remote control (old old style white plastic)
        57224: PLAY_PAUSE,
        12168: VOL_PLUS,
        20360: VOL_MINUS,
        61320: LEFT,
        8072: RIGHT,
        49032: MENU
    }

    def __init__(self, debug=False):
        self.pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
        self.decoder = adafruit_irremote.GenericDecode()
        self.debug = debug

    #@ classmethod
    #def debug_print(cls, debug, *message):
    def debug_print(self, *message):
        """Print a debug message"""
        if self.debug:
            print("remote_control:", *message)

    def code(self, blocking=False):
        """Return the decoded remote control code value"""
        try:
            pulses = self.decoder.read_pulses(self.pulsein, blocking=blocking)

            if pulses is None:
                return RemoteControl.UNKNOWN

            self.debug_print(len(pulses), "pulses:", pulses)

            code = self.decoder.decode_bits(pulses)

            self.debug_print("decoded:", code)

            if len(code) == 2:
                #  lego power functions ir speed remote control
                code_mask = (code[1] << 8) | code[0]
            elif (len(code) == 4) & (code[0] == 136) & (code[1] == 30):
                #  apple tv remote control
                code_mask = (code[2] << 8) | code[3]
            elif (code[0] == 255) or (code[1] == 2):
                #  adafruit mini remote control
                code_mask = (code[2] << 8) | code[3]
            else:
                return RemoteControl.UNKNOWN

            return RemoteControl.CODE.get(code_mask, RemoteControl.UNKNOWN)
        except adafruit_irremote.IRNECRepeatException:
            self.debug_print("repeat exception")
        except adafruit_irremote.IRDecodeException as exception:
            self.debug_print("failed to decode:", exception.args)
        except IndexError as exception:
            self.debug_print("index error:", exception.args)
        except MemoryError as exception:
            self.debug_print("memory error:", exception.args)

        return RemoteControl.UNKNOWN
