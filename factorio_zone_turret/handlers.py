import re
from typing import Optional

from factorio_zone_turret import colors
from factorio_zone_turret.fz_manager.fz_manager.factorio_zone_api import FZClient, ServerStatus
from factorio_zone_turret.pi_utils import change_led_color, pulse_led

current_status: Optional[ServerStatus] = None
current_players: int = 0
hosting_started: bool = False


def create_server_status_change_handler(client: FZClient):
    """ Create a handler that will handle color based on the server status """

    def handle_server_status_change(*_):
        """ Handle color based on the server status """
        global current_status, current_players, hosting_started
        if current_status == client.server_status:
            return

        current_status = client.server_status
        current_players = 0  # reset players count on status change
        hosting_started = False  # reset hosting started flag on status change
        if current_status == ServerStatus.OFFLINE:
            change_led_color(colors.RED)
        elif current_status == ServerStatus.STARTING:
            pulse_led(colors.YELLOW, colors.DARK_YELLOW)
        elif current_status == ServerStatus.STOPPING:
            pulse_led(colors.RED, colors.DARK_RED)

    return handle_server_status_change


def handle_players_count(log: str):
    """ Handle color based on the players count """
    global current_players
    # check if the server is running
    if current_status != ServerStatus.RUNNING:
        return
    # check if the player count changes
    if re.search(r"peerID.*?newState\(ConnectedWaitingForMap\)", log):
        pulse_led(colors.GREEN, colors.DARK_GREEN)
        current_players += 1
    elif re.search(r"peerID.*?newState\(InGame\)", log):
        change_led_color(colors.GREEN)
    elif re.search(r"\[LEAVE] .*? left the game", log):
        current_players = max(current_players - 1, 0)  # fail-safe
        if current_players == 0:
            change_led_color(colors.BLUE)


def handle_hosting_started(log: str):
    """
    Handle color during starting sequence:
    - Server turns into RUNNING state earlier than it actually starts hosting
    - The LED is kept in STARTING state until we get the "hosting" message
    """
    global current_status, hosting_started
    if hosting_started or current_status not in (ServerStatus.STARTING, ServerStatus.RUNNING):
        return
    if re.search(r"Hosting game at IP ADDR", log):
        hosting_started = True
        change_led_color(colors.BLUE)
