import asyncio
import logging
import re
from typing import Optional

from factorio_zone_turret import colors
from factorio_zone_turret.config import config
from factorio_zone_turret.fz_manager.fz_manager.factorio_zone_api import FZClient, ServerStatus
from factorio_zone_turret.pi_utils import button, change_led_color, pulse_led


class FZTurretServer:
    """ Communicates with the FZ server, keeps track of the current state """
    current_status: Optional[ServerStatus]
    current_players: int
    hosting_started: bool

    def __init__(self):
        logging.info("Initializing FZ Turret server")
        logging.info(config)
        pulse_led(colors.DARK_WHITE, colors.WHITE)
        self.current_status = None
        self.current_players = 0
        self.hosting_started = False
        self.client = FZClient(token=config.FZ_TOKEN)
        self.init_handlers()
        logging.info("FZ Turret server ready")

    def init_handlers(self):
        """ Init handlers for the Pi's led and button """
        # Create button handlers
        button.when_activated = self.create_button_press_handler()
        # Create led handlers (via FZ Client)
        self.client.add_message_listener(self.create_server_status_change_handler())
        self.client.add_logs_listener(self.create_players_count_handler())
        self.client.add_logs_listener(self.create_hosting_start_handler())

    def reset(self):
        """ Resets server state """
        self.__init__()

    def start(self):
        asyncio.run(self.client.connect())

    def create_server_status_change_handler(self):
        """ Create a handler that will handle color based on the server status """

        def handle_server_status_change(*_):
            """ Handle color based on the server status """
            if self.current_status == self.client.server_status:
                return

            self.current_status = self.client.server_status
            self.current_players = 0  # reset players count on status change
            self.hosting_started = False  # reset hosting started flag on status change
            if self.current_status == ServerStatus.OFFLINE:
                change_led_color(colors.RED)
            elif self.current_status == ServerStatus.STARTING:
                pulse_led(colors.YELLOW, colors.DARK_YELLOW)
            elif self.current_status == ServerStatus.STOPPING:
                pulse_led(colors.RED, colors.DARK_RED)

        return handle_server_status_change

    def create_players_count_handler(self):
        """ Create a handler for players count detection """

        def handle_players_count(log: str):
            """ Handle color based on the players count """
            # check if the server is running
            if self.current_status != ServerStatus.RUNNING:
                logging.info("Handling players count: self.current_status != ServerStatus.RUNNING")
                return
            # check if the player count changes
            if re.search(r"peerID.*?newState\(ConnectedWaitingForMap\)", log):
                pulse_led(colors.GREEN, colors.DARK_GREEN)
                self.current_players += 1
                logging.info(f"Handling players count: Changing led color to blinking, players +1, new count: {self.current_players}")
            elif re.search(r"peerID.*?newState\(InGame\)", log):
                change_led_color(colors.GREEN)
                logging.info(f"Handling players count: Changing led color to static")
            elif re.search(r"removing peer", log):
                self.current_players = max(self.current_players - 1, 0)  # fail-safe
                if self.current_players == 0:
                    change_led_color(colors.BLUE)
                logging.info(f"Handling players count: Removing peer, players -1, new count: {self.current_players}")

        return handle_players_count

    def create_hosting_start_handler(self):
        """ Create handler to track if the hosting has started """

        def handle_hosting_started(log: str):
            """
            Handle color during starting sequence:
            - Server turns into RUNNING state earlier than it actually starts hosting
            - The LED is kept in STARTING state until we get the "hosting" message
            """
            if self.hosting_started or \
                    self.current_status not in (ServerStatus.STARTING, ServerStatus.RUNNING):
                return
            if re.search(r"Hosting game at IP ADDR", log):
                self.hosting_started = True
                change_led_color(colors.BLUE)

        return handle_hosting_started

    def create_button_press_handler(self):
        """ Create handler for the button press which starts the server """

        def handle_button_press():
            """ Start the server """
            self.client.start_instance(region=config.FZ_SERVER_REGION,
                                       version=config.FZ_SERVER_VERSION,
                                       save=config.FZ_SERVER_SAVE,
                                       ipv6=config.FZ_SERVER_IPV6)

        return handle_button_press
