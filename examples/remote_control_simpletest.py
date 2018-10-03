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