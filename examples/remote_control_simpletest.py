import time
import makers_remote_control

remote_control = makers_remote_control.RemoteControl(debug=False)

while True:
    code = remote_control.code()

    if code == remote_control.UP_:
        print("Faster")
    elif code == remote_control.DOWN:
        print("Slower")
    elif code == remote_control.LEFT:
        print("Left")
    elif code == remote_control.RIGHT:
        print("Right")
    elif code == 4:
        print("Something for Four")
    elif code == 6:
        print("Something for Six")
    elif code != remote_control.UNKNOWN:
        print("Code: ", code)

    time.sleep(0.1)
