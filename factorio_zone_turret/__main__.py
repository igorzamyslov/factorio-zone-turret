import asyncio
import re

from factorio_zone_turret.config import config
from factorio_zone_turret.fz_manager.fz_manager.factorio_zone_api import FZClient, ServerStatus

from factorio_zone_turret.pi_utils import pulse_red, pulse_yellow, \
    turn_green, turn_red, turn_yellow

from typing import Optional

client = FZClient(token=config.FZ_TOKEN)

current_status: Optional[ServerStatus] = None
current_players: int = 0


def handle_players_count(log: str):
    global current_players
    # check if the server is running
    if current_status != ServerStatus.RUNNING:
        return
    # check if the player count changes
    if re.search(r"\[JOIN] .*? joined the game", log):
        current_players += 1
    elif re.search(r"\[LEAVE] .*? left the game", log):
        current_players -= 1
    else:
        return

    if current_players:
        turn_green()
    else:
        turn_yellow()


def handle_server_status_change(*_):
    global current_status
    if current_status == client.server_status:
        return

    current_status = client.server_status
    if current_status == ServerStatus.OFFLINE:
        turn_red()
    elif current_status == ServerStatus.STARTING:
        pulse_yellow()
    elif current_status == ServerStatus.RUNNING:
        turn_yellow()
    elif current_status == ServerStatus.STOPPING:
        pulse_red()


handle_server_status_change()
client.add_message_listener(handle_server_status_change)
client.add_logs_listener(handle_players_count)
asyncio.run(client.connect())
