# Factorio.zone Turret

The project uses Raspberry PI to be able to start and track the status of the `factorio.zone`
server:

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

1. Connect RGB LED to the following control pins:
    - Red: `GPIO17`
    - Green: `GPIO27`
    - Blue: `GPIO22`
    - Ground
1. Connect button to:
    - `GPIO2`
    - Ground

### Repository

- Install requirements: `pip install -r requirements.txt`
- Get required submodule(s): `git submodule update --init`
- Create `.env` file according to the [.env.example](.env.example)

## Running

Start the server with the following command: `python -m factorio_zone_turret`

## Auto-start

Open crontab: `crontab -e` \
Add the following line there:
```
@reboot sleep 90 && cd ~/factorio-zone-turret && git pull && python -m factorio_zone_turret >~/log.txt 2>&1
```
which:
- waits until the system is fully booted
- navigates to the repository folder
- pulls the latest version of the code
- starts the server, redirecting all the logs to the `log.txt` in the home folder
