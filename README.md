# Factorio.zone Turret

The project uses Raspberry PI to track the status of the `factorio.zone` server:

| Color           | Status                                      |
|-----------------|---------------------------------------------|
| RED             | server is stopped                           |
| BLINKING YELLOW | server is starting                          |
| BLUE            | server is running, no players on the server |
| BLINKING GREEN  | server is running, player connecting        |
| GREEN           | server is running, players on the server    |
| BLINKING RED    | server is stopping                          |

## Initial setup

### Raspberry Pi

Connect RGB LED to the following control pins:

- Red: GPIO17
- Green: GPIO27
- Blue: GPIO22

### Repository

- Install requirements: `pip install -r requirements.txt`
- Get required submodule(s): `git submodule update --init`
- Create `.env` file according to the [.env.example](.env.example)

## Running

Start the server with the following command: `python -m factorio_zone_turret`
