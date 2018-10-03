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
`Makers_remote_control`
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

import adafruit_irremote
import board
import pulseio

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/fmorton/Makers_CircuitPython_remote_control.git"


"""
  Demo code for Circuit Playground Express:

  import time
  from makers_remote_control import remote_control

  remote_control = remote_control(debug=False)

  while True:
    code = remote_control.code()

    if(code == remote_control.CODE_UP):
      print("Forward")
    elif(code == remote_control.CODE_DOWN):
      print("Backwards")
    elif(code == remote_control.CODE_LEFT):
      print("Left")
    elif(code == remote_control.CODE_RIGHT):
      print("Right")
    elif(code == 4):
      print("Something for Four")
    elif(code == 6):
      print("Something for Six")

    time.sleep(0.1)


  Adafruit Mini Remote Control IR Mapping and Mask
  1: [255, 2, 247, 8]             63240
  2: [255, 2, 119, 136]           30600
  3: [255, 2, 183, 72]            46920
  4: [255, 2, 215, 40]            55080
  5: [255, 2, 87, 168]            22440
  6: [255, 2, 151, 104]           38760
  7: [255, 2, 231, 24]            59160
  8: [255, 2, 103, 152]           26520
  9: [255, 2, 167, 88]            42840
  0: [255, 2, 207, 48]            53040
  ^ : [255, 2, 95, 160]           24480
  v : [255, 2, 79, 176]           20400
  > : [255, 2, 175, 80]           44880
  < : [255, 2, 239, 16]           61200
  Enter: [255, 2, 111, 144]       28560
  Setup: [255, 2, 223, 32]        57120
  Stop/Mode: [255, 2, 159, 96]    40800
  Back: [255, 2, 143, 112]        36720
  Vol - : [255, 2, 255, 0]        65280
  Vol + : [255, 2, 191, 64]       48960
  Play/Pause: [255, 2, 127, 128]  32640
"""

class remote_control:
  CODE_UP = 128
  CODE_DOWN = 129
  CODE_RIGHT = 130
  CODE_LEFT = 131
  CODE_ENTER = 132
  CODE_SETUP = 133
  CODE_STOP_MODE = 134
  CODE_BACK = 135
  CODE_VOL_MINUS = 136
  CODE_VOL_PLUS = 137
  CODE_PLAY_PAUSE = 138
  CODE_UNKNOWN = -1


  def __init__(self, debug=False):
    self.pulsein = pulseio.PulseIn(board.REMOTEIN, maxlen=120, idle_state=True)
    self.decoder = adafruit_irremote.GenericDecode()
    self.debug = debug


  def debug_print(self, *message):
    print("remote_control:", *message)


  def code(self, blocking=False):
    try:
      pulses = self.decoder.read_pulses(self.pulsein, blocking=blocking)

      if(pulses == None): return(self.CODE_UNKNOWN)

      if self.debug: self.debug_print(len(pulses), "pulses:", pulses)

      code = self.decoder.decode_bits(pulses, debug=False)

      if self.debug: self.debug_print("decoded:", code)

      if((code[0] != 255) or (code[1] != 2)): return(self.CODE_UNKNOWN)

      code_mask = (code[2] << 8) | code[3]

      if(code_mask == 53040): return(0)
      if(code_mask == 63240): return(1)
      if(code_mask == 30600): return(2)
      if(code_mask == 46920): return(3)
      if(code_mask == 55080): return(4)
      if(code_mask == 22440): return(5)
      if(code_mask == 38760): return(6)
      if(code_mask == 59160): return(7)
      if(code_mask == 26520): return(8)
      if(code_mask == 42840): return(9)
      if(code_mask == 24480): return(self.CODE_UP)
      if(code_mask == 20400): return(self.CODE_DOWN)
      if(code_mask == 44880): return(self.CODE_RIGHT)
      if(code_mask == 61200): return(self.CODE_LEFT)
      if(code_mask == 28560): return(self.CODE_ENTER)
      if(code_mask == 57120): return(self.CODE_SETUP)
      if(code_mask == 40800): return(self.CODE_STOP_MODE)
      if(code_mask == 36720): return(self.CODE_BACK)
      if(code_mask == 65280): return(self.CODE_VOL_MINUS)
      if(code_mask == 48960): return(self.CODE_VOL_PLUS)
      if(code_mask == 32640): return(self.CODE_PLAY_PAUSE)

      return(self.CODE_UNKNOWN)
    except adafruit_irremote.IRNECRepeatException:
      if self.debug: self.debug_print("repeat exception")
      return(self.CODE_UNKNOWN)
    except adafruit_irremote.IRDecodeException as e:
      if self.debug: self.debug_print("failed to decode:", e.args)
      return(self.CODE_UNKNOWN)
    except MemoryError as e:
      if self.debug: self.debug_print("memory error:", e.args)
      return(self.CODE_UNKNOWN)
