import asyncio

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

asyncio.run(client.connect())
