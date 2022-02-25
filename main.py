from flask import Flask, render_template, redirect, url_for, request
from tinydb import TinyDB, Query

from flask_socketio import SocketIO, send

import json

from configs import IP_SERVER


app = Flask(__name__)
# app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app, cors_allowed_origins='*')


@socketio.on('message')
def handleMessage(msg):
	print('Message: ' + str(msg))
	send(msg, broadcast=True)

tiny_db = TinyDB('./static/db.json')
User = Query()
Team = Query()

tiny_db.drop_tables()
table_user = tiny_db.table('table_user')
table_team = tiny_db.table('table_team')
with open('./static/config_team.json') as f:
    players_config = json.load(f)
    for player in players_config["players"]:
        table_user.upsert(
            {'name': player['name'], 
             'team': player['team'], 
             'passwd': player['passwd'],
             'selected': False}, User.name == player['name'])
    for team in players_config["team_color"]:
        table_team.upsert(
            {'key': team['key'], 
             'color': team['color']}, Team.key == team['color'])
table_user.all()

@app.route("/")
def hello_world():
    return render_template("select_player.html", user_list=table_user.all())

# @app.route("/sudo/")
# def sudo():
#     return render_template("modify_teams.html", user_list=table_user.all())

# @app.route("/valid_user", methods=['GET', 'POST'])
# def valid_user():
#     player_select = request.args.get('players')
#     print(player_select)
#     return redirect(url_for("click/", username=player_select))

@app.route('/click', methods=['POST'])
def click():
    username = request.form.get('players')
    passwd = request.form.get('passwd')
    print(username)
    print(passwd)
    current_user = table_user.search(User.name == username)[0]
    current_team = table_team.search(Team.key == current_user['team'])[0]
    print(current_user)
    print(current_team)
    if current_user and int(passwd) == current_user['passwd']:
        team_color = current_team["color"]
        return render_template("click_to_buzz.html", 
        ip_server=IP_SERVER,
        user_name=username, team_color=team_color, cmd_root=None)
    else:
        print("error login")
        return redirect(url_for("hello_world"))

# @app.route("/update/<user_name>/")
# def update(user_name):
#     table_user.upsert({'name': user_name, 'team': 0, 'selected': False}, User.name == user_name)
#     return redirect(url_for("sudo"))
     
@app.route("/buzzer/")
def buzzer():
    return render_template("main_buzzer.html", 
        ip_server=IP_SERVER)

if __name__ == "__main__":

    # app.run(debug=True, use_reloader=True)
    socketio.run(app, host=IP_SERVER)

# https://stackoverflow.com/questions/15871391/implementing-flask-login-with-multiple-user-classes