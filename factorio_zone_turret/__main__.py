import asyncio

from factorio_zone_turret.config import config
from factorio_zone_turret.fz_manager.fz_manager.factorio_zone_api import FZClient, ServerStatus

from factorio_zone_turret.pi_utils import turn_green, turn_red, turn_yellow


client = FZClient(token=config.FZ_TOKEN)
CURRENT_STATUS = None


def handle_server_status_change(*_):
    global CURRENT_STATUS
    if CURRENT_STATUS != client.server_status:
        CURRENT_STATUS = client.server_status

        if CURRENT_STATUS == ServerStatus.OFFLINE:
            turn_red()
        elif CURRENT_STATUS == ServerStatus.STARTING:
            turn_yellow()
        elif CURRENT_STATUS == ServerStatus.RUNNING:
            turn_green()
        elif CURRENT_STATUS == ServerStatus.STOPPING:
            turn_yellow()


handle_server_status_change()
client.add_message_listener(handle_server_status_change)
asyncio.run(client.connect())
