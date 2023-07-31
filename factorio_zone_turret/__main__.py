import logging
from time import sleep

from factorio_zone_turret.server import FZTurretServer


# Logo
def print_logo():
    class bcolors:
        ORANGE = '\033[38;5;202m'
        ENDC = '\033[0m'

    logo = """
     ______ ______  _______                  _   
    |  ____|___  / |__   __|                | |  
    | |__     / /     | |_   _ _ __ _ __ ___| |_ 
    |  __|   / /      | | | | | '__| '__/ _ \ __|
    | |     / /__     | | |_| | |  | | |  __/ |_ 
    |_|    /_____|    |_|\__,_|_|  |_|  \___|\__|
    """
    print(f"{bcolors.ORANGE}{logo}{bcolors.ENDC}")


print_logo()

# Main loop
server = FZTurretServer()
while True:
    try:
        server.start()
    except Exception as error:
        logging.warning("Reconnecting due to the following exception: %s", error, exc_info=True)
        sleep(5)
        server.reset()
