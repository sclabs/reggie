"""Flask views - aka app routes."""

from flask import jsonify, request
from reggie import app, draft, player

@app.route('/start', methods=['GET'])
def draft_start():
    return draft.start([])

@app.route('/cancel', methods=['GET'])
def draft_cancel():
    return draft.cancel()

@app.route('/status', methods=['GET'])
def draft_status():
    return jsonify(draft.status())


@app.route('/list', methods=['GET'])
def list_players():
    return player.list_all()


@app.route('/draft', methods=['POST'])
def slack_command():
    command = request.form['text']
    response_url = request.form['response_url']
    response = ''
    words = command.split()

    if len(words) == 0:
        return jsonify({'response_type': 'in_channel', 'text': response})

    if command == 'info':
        response = 'https://github.com/sclabs/reggie'

    if command == 'cancel':
        response = draft.cancel()

    # if command == 'reload':
    #     response = reload(response_url)
    #
    if words[0] == 'addplayer':
        if len(words) == 3:
            response = player_add(words[1], words[2])
        else:
            response = '`draft addplayer` takes a name and an ID.'

    if words[0] == 'removeplayer' and len(words) == 2:
        response = player_remove(words[1])

    if command == 'listplayers':
        response = player_list()

    if words[0] == 'start':
        if len(words) > 1 and len(words) < 7:
            # response = draft_start(words[1:])
            response = draft.start([])
        else:
            response = '`/draft start` takes a list of up to 5 players.'

    # if words[0] == 'enemy':
    #     if len(words) == 2 and words[1] in reggie_constants.global_hero_list:
    #         response = draft_hero(command)
    #
    #     else:
    #         response = '`/draft enemy` needs exactly one hero specified.'
    #
    # if words[0] == 'pub' and len(words) == 2 and words[1] in reggie_constants.global_hero_list:
    #     response = draft_pub(words[1])
    #
    # if command in reggie_constants.global_hero_list:
    #     response = draft_hero(command)

    # if words[0] in all_players:
    #    response = 'Drafting for player ' + command

    # if response == '':
    #     return reggie_constants.default_response

    return jsonify({'response_type': 'in_channel', 'text': response})


@app.route('/', methods=['GET'])
def alive():
    return 'Reggie is alive'
