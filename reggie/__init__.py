from flask import Flask
app = Flask(__name__)

state = {
    'in_progress': False,
    'players': [],
    'bans': [],
    'friendly_picks': [],
    'enemy_picks': []
}

import reggie.views
