# Buzzer application

Buzzer for multiplayer games: after running the Flask server, each player must connect to the same local network with his device.

Teams and players are configured in `static/config_team.json` file and the IP address of the Flask server in `configs.py`.

## First init & run

```shell
python3 -m venv venv
. venv/bin/activate

export FLASK_APP=main
export FLASK_ENV=development # to debug and reload automatically Flask server after modification
flask run
```

Or for Windows
```shell
python3 -m venv venv
venv\Scripts\activate

$env:FLASK_APP = "main"
$env:FLASK_ENV = "development"
flask run
```
