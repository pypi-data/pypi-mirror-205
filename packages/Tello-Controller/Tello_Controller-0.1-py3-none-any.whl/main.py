from tello import Tello
from script_sender import ScriptSender

ips = ["192.168.0.1", "192.168.0.2", "192.168.0.3"]
scripts = [["spin", "takeoff\ncw 360\nland"], ["flip", "takeoff\nflip f\nflip r\nflip b\n flip l"]]

ss = ScriptSender()
for ip in ips:
    ss.save_drone(Tello(ip))

for name, script in scripts:
    ss.save_script(name, script=script)

ss.start_script("spin", 1, 2)