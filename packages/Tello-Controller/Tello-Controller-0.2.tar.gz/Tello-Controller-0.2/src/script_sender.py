from tello import Tello
from datetime import datetime
import time



class ScriptSender():

    def ScriptSender(self):
        self.scripts = {}
        self.drones = []


    def save_drone(self, tello: Tello) -> int:
        self.drones.append(tello)
        return len(self.drones)-1


    def save_script(self, name: str, file_name="", script="") -> str:
        if file_name != "":
            with open(file_name, 'r') as f:
                commands = f.readlines()
        elif script != "":
            commands = script.split("\n")
        else:
            raise Exception("No script provided")
        
        self.scripts[name] = commands
        
        return name


    def start_script(self, name: str, *droneids: int):
        start_time = str(datetime.now())

        if not name in self.scripts.keys():
            raise Exception("Selected script doesn't exist")

        tellos = []
        for id in droneids:
            tellos.append(self.drones[id])

            if id < 0 or id >= len(self.drones):
                raise Exception("One or multiple selected drones don't exist")

        for command in self.scripts[name]:
            for tello in tellos:
                if command != '' and command != '\n':
                    command = command.rstrip()

                    if command.find('delay') != -1:
                        sec = float(command.partition('delay')[2])
                        print(f'delay {sec}')
                        time.sleep(sec)
                        break
                    else:
                        tello.send_command(command)

        for id in droneids:
            with open(f'log/{start_time}-{id}.txt', 'w') as out:
                log = self.drones[id].get_log()

                for stat in log:
                    stat.print_stats()
                    s = stat.return_stats()
                    out.write(s)