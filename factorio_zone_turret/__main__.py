import asyncio
import logging

from factorio_zone_turret import colors
from factorio_zone_turret.config import config
from factorio_zone_turret.fz_manager.fz_manager.factorio_zone_api import FZClient
from factorio_zone_turret.handlers import create_button_press_handler, \
    create_server_status_change_handler, handle_hosting_started, handle_players_count
from factorio_zone_turret.pi_utils import button, pulse_led

pulse_led(colors.DARK_WHITE, colors.WHITE)  # Initial state
client = FZClient(token=config.FZ_TOKEN)

# Create button handlers
button.when_activated = create_button_press_handler(client)

# Create server status handlers
handle_server_status_change = create_server_status_change_handler(client)
client.add_message_listener(handle_server_status_change)
client.add_logs_listener(handle_players_count)
client.add_logs_listener(handle_hosting_started)

class bcolors:  
    ORANGE =  '\033[38;5;202m'
    ENDC      = '\033[0m'

logo = """  ______ ______  _______                  _   
 |  ____|___  / |__   __|                | |  
 | |__     / /     | |_   _ _ __ _ __ ___| |_ 
 |  __|   / /      | | | | | '__| '__/ _ \ __|
 | |     / /__     | | |_| | |  | | |  __/ |_ 
 |_|    /_____|    |_|\__,_|_|  |_|  \___|\__|
"""
print(f"{bcolors.ORANGE}{logo}{bcolors.ENDC}")

logging.info("Starting server...")
while True:
    try:
        asyncio.run(client.connect())
    except Exception as error:
        logging.warning("Reconnecting due to the following exception: %s", error, exc_info=True)
