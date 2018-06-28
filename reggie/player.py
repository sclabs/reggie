"""Functions for managing the player database."""

from reggie import state
from reggie.database import db, Player


def add(name, steam_id):
    """Add a player to the reggie database."""
    for player in Player.query.all():
        if name == player.name:
            return 'Player ' + name + ' already exists.'
        if id == player.id:
            return 'Player with ID ' + steam_id + ' already exists.'

    new_player = Player(name=name, id=steam_id)
    db.session.add(new_player)
    db.session.commit()
    return 'Added player ' + name + ' with ID ' + str(steam_id) + '.'


def remove(name):
    """Remove a player or players matching a name from the reggie database."""
    players_matching_name = Player.query.filter(Player.name == name)
    if not players_matching_name.all():
        return 'Player ' + name + ' isn\'t in the database.'

    players_matching_name.delete()
    db.session.commit()
    return 'Removed player ' + name + '.'


def list_all():
    """List all the players in the reggie database."""
    if state['in_progress']:
        return 'Draft currently in progress!'

    all_players = Player.query.all()
    if not all_players:
        return 'No players in the database!'

    response = ''
    for player in all_players:
        response += player.name + ': ' + str(player.id) + '\n'
    return response
