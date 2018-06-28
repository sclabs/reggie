"""Functions for draft management."""

from flask import session
from reggie import state

def start(current_players):
    if state['in_progress']:
        return 'Draft already in progress!'

    state['in_progress'] = True

    return 'Draft started.'

    # response = 'NOW DRAFTING: '
    # data = {'players': [],
    #         'friendlies': [None, None, None, None, None],
    #         'enemies': [],
    #         'rec_pool': reggie_constants.global_hero_list}
    #
    # for player in current_players:
    #     if player not in [player.name for player in Player.query.all()]:
    #         return 'INVALID PLAYER: ' + player
    #     response = response + player + ', '
    #     data['players'].append(player)
    #
    # with open('draft.json', 'w') as outfile:
    #     json.dump(data, outfile)
    #
    # return response[:-2]


def cancel():
    if state['in_progress']:
        state['in_progress'] = False
        return 'Killed draft.'
    else:
        return 'No draft in progress.'

def status():
    return state
