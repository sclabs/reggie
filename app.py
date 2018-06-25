import json
import os.path
import os
from flask_sqlalchemy import SQLAlchemy
from time import sleep
import threading
import requests
from lxml import html
from flask import Flask, request, jsonify
import reggieconstants
from itertools import permutations
from scipy import stats

app = Flask(__name__)

# To initialize DB, pop open a Python interpreter and run:
# >>> from app import db
# >>> db.create_all()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://REDACTED:REDACTED@REDACTED/reggiedb"
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    steamID = db.Column(db.String(64))

class HeroVsHero(db.Model):
    __tablename__ = "heroVsHero"
    id = db.Column(db.Integer, primary_key=True)
    thishero = db.Column(db.String(64))
    for hero in reggieconstants.global_hero_list:
        locals()[hero] = db.Column(db.String(64))

class PlayerOnHero(db.Model):
    __tablename__ = "playerOnHero"
    id = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.String(64))
    for hero in reggieconstants.global_hero_list:
        locals()[hero] = db.Column(db.String(64))

class NumGamesOnHero(db.Model):
    __tablename__ = "numGamesOnHero"
    id = db.Column(db.Integer, primary_key=True)
    playerID = db.Column(db.String(64))
    for hero in reggieconstants.global_hero_list:
        locals()[hero] = db.Column(db.String(64))

def draft_start(current_players):
    if os.path.isfile('draft.json'):
        return 'Draft already in progress!'

    response = 'NOW DRAFTING: '
    data = {'players': [],
            'friendlies': [None, None, None, None, None],
            'enemies': [],
            'rec_pool': reggieconstants.global_hero_list}

    for player in current_players:
        if player not in [player.name for player in Player.query.all()]:
            return 'INVALID PLAYER: ' + player
        response = response + player + ', '
        data['players'].append(player)

    with open('draft.json', 'w') as outfile:
        json.dump(data, outfile)

    return response[:-2]

def draft_cancel():
    if os.path.isfile('draft.json'):
        os.remove('draft.json')
        return 'Killed draft.'
    else:
        return 'No draft in progress.'

def player_add(player_name, player_ID):
    if os.path.isfile('draft.json'):
        return 'There\'s a draft in progress. Mess with the players later!'

    new_player = Player(name = player_name, steamID = player_ID)
    db.session.add(new_player)
    db.session.commit()

    return 'Added player ' + player_name + ' with ID ' + player_ID + '.'

def player_remove(player_name):
    if os.path.isfile('draft.json'):
        return 'There\'s a draft in progress. Mess with the players later!'

    players_matching_name = Player.query.filter(Player.name == player_name)

    if len(players_matching_name.all()) == 0:
        return 'Player ' + player_name + ' isn\'t on my list.'
    players_matching_name.delete()

    return 'Removed player ' + player_name + '.'

def player_list():
    if os.path.isfile('draft.json'):
        return 'There\'s a draft in progress. Mess with the players later!'

    all_players = Player.query.all()

    if len(all_players) == 0:
        return 'No players in my database!'
    response = ''
    for player in all_players:
        response += player.name + ': ' + player.steamID + '\n'
    return response

def reload_roles():
    if os.path.isfile('roles.json'):
        os.remove('roles.json')

    role_frequencies = ['infobox-color-always', 'infobox-color-very often',
                        'infobox-color-often']
    roles_to_numbers = {'Hard Carry': '1', 'Mid Lane Core': '2',
                        'Offlaner': '3', 'Roaming Support': '4',
                        'Hard Support': '5'}
    role_data = {'1': [], '2': [], '3': [], '4': [], '5': []}

    for hero in reggieconstants.global_hero_list:
        liquipedia_hero = hero.replace('-', ' ').title().replace(' ', '_')
        print('Gathering hero: ' + hero)
        page = requests.get('https://liquipedia.net/dota2/' + liquipedia_hero)
        tree = html.fromstring(page.content)
        roleblox = tree.xpath("//div[contains(@class, 'infobox-cell-6')]")
        for element in roleblox:
            if any(frequency in element.get('class') for frequency in role_frequencies):
                role_data[roles_to_numbers[element.get('title')]].append(hero)

    with open('roles.json', 'w') as outfile:
        json.dump(role_data, outfile)

    return str(role_data)

# Most hacky thing ever
def reload_hero_vs_hero():
    for hero in reggieconstants.global_hero_list:
        print('Gathering hero winrates: ' + hero)
        cached_page = requests.get('http://webcache.googleusercontent.com/search?q=cache:https://www.dotabuff.com/heroes/' + hero + '/counters&num=1&strip=0&vwsrc=1')
        dotabuff_page = html.fromstring(html.fromstring(cached_page.content).xpath('/html/body/div[2]/pre/text()[1]')[0])
        all_elements = dotabuff_page.xpath('//tr')
        hero_matchup_dict = {'thishero': hero}
        for element in all_elements:
            if element.get('data-link-to') is not None:
                enemy_hero = element.get('data-link-to')[8:]
                winrate_against = list(element.iter('td'))[3].get('data-value')
                hero_matchup_dict[enemy_hero] = winrate_against
        hero_db_row = HeroVsHero(**hero_matchup_dict)
        db.session.add(hero_db_row)
        db.session.commit()

def threaded_reload(response_url):
    # reload_roles()
    # data = {'response_type':'in_channel', 'text':'Reloaded hero roles.'}
    # requests.post(url = response_url, json = data)
    # reload_hero_vs_hero()
    # data = {'response_type':'in_channel', 'text':'Reloaded hero vs. hero winrates.'}
    # requests.post(url = response_url, json = data)
    # data = {'response_type':'in_channel', 'text':'Reloaded player-on-hero winrates.'}
    # requests.post(url = response_url, json = data)
    data = {'response_type':'in_channel', 'text':'Reloading temporarily disabled to avoid hitting rate limits.'}
    requests.post(url = response_url, json = data)

def reload(response_url):
    if os.path.isfile('draft.json'):
        return 'There\'s a draft in progress. No reloading during draft.'

    thread = threading.Thread(target=threaded_reload, args=(response_url, ))
    thread.start()
    return 'Starting reload...'

def recommendations():
    response = 'RECOMMENDED: '

    with open('draft.json') as file:
        current_draft = json.load(file)

    hero_data = {}
    results = []
    all_hero_v_hero_matchups = HeroVsHero.query.all()

    for matchup in all_hero_v_hero_matchups:
        if matchup.thishero in current_draft['rec_pool']:
            hero_data[matchup.thishero] = {}
            for enemy_hero in current_draft['enemies']:
                hero_data[matchup.thishero][enemy_hero] = float(getattr(matchup, enemy_hero))/100

    for hero in hero_data.keys():
        results.append((hero, str(stats.gmean(list(hero_data[hero].values())))))

    results.sort(key=lambda x: x[1], reverse = True)
    for result in results[:5]:
        response += '*' + result[0] + '* - ' + str(round(float(result[1])*100, 2)) + '%, '
    response = response[:-2]

    return response

def draft_hero(command):
    if not os.path.isfile('draft.json'):
        return 'No draft in progress.'
    if not os.path.isfile('roles.json'):
        return "Roles aren't loaded. Please run `/draft reload`."

    with open('draft.json') as file:
        current_draft = json.load(file)
    with open('roles.json') as file:
        heroes_by_role = json.load(file)

    words = command.split()

    if words[0] == 'enemy':
        hero = words[1]
    else:
        hero = command

    if hero in current_draft['friendlies']:
        return hero + ' is already on your team.'
    if hero in current_draft['enemies']:
        return hero + ' is already on the other team.'

    if words[0] == 'enemy':
        current_draft['enemies'].append(hero)
        if hero in current_draft['rec_pool']:
            current_draft['rec_pool'].remove(hero)
        response = 'Got it. Adding ' + hero + ' to the enemy team.'
    else:
        current_draft['friendlies'].pop(0)
        current_draft['friendlies'].append(hero)

        still_draftable = [False, False, False, False, False]
        valid_permutations = []

        for permutation in list(permutations(current_draft['friendlies'])):
            if (permutation[0] is None or permutation[0] in heroes_by_role['1']) and (permutation[1] is None or permutation[1] in heroes_by_role['2']) and (permutation[2] is None or permutation[2] in heroes_by_role['3']) and (permutation[3] is None or permutation[3] in heroes_by_role['4']) and (permutation[4] is None or permutation[4] in heroes_by_role['5']):
                valid_permutations.append(permutation)
                for index in range(0, len(permutation)):
                    if permutation[index] is None:
                        still_draftable[index] = True

        os.remove('draft.json')

        if len(valid_permutations) == 0:
            return "According to my database, there are no more valid role permutations of your heroes. Killing the draft."

        response = 'Got it. Please draft one of these roles: *'
        rec_pool = []

        for index in range(0, len(still_draftable)):
            if still_draftable[index] is True:
                rec_pool = list(set(rec_pool + heroes_by_role[str(index+1)]))
                response += str(index+1) + ' '
        current_draft['rec_pool'] = [x for x in rec_pool if (x not in current_draft['friendlies'] and x not in current_draft['enemies'])]
        response += '*'

    if None not in current_draft['friendlies']:
        response = 'All done! Here are your valid permutations: \n'
        for permutation in valid_permutations:
            response += str(permutation) + '\n'
    else:
        with open('draft.json', 'w') as outfile:
            json.dump(current_draft, outfile)
        response += '\n' + recommendations()

    return response

@app.route('/draft', methods=['POST'])
def draft():
    command = request.form['text']
    response_url = request.form['response_url']
    response = ''
    words = command.split()

    if len(words) == 0:
        return jsonify({'response_type':'in_channel', 'text':response})

    if command == 'info':
        return reggieconstants.infotext

    if command == 'cancel':
        response = draft_cancel()

    if command == 'reload':
        response = reload(response_url)

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
            response = draft_start(words[1:])
        else:
            response = '`/draft start` takes a list of up to 5 players.'

    if words[0] == 'enemy':
        if len(words) != 2:
            response = 'You need to specify an enemy hero.'
        else:
            response = draft_hero(command)

    if command in reggieconstants.global_hero_list:
        response = draft_hero(command)

    # if words[0] in all_players:
    #    response = 'Drafting for player ' + command

    if response == '':
        return reggieconstants.default_response

    return jsonify({'response_type':'in_channel', 'text':response})

@app.route('/', methods=['GET'])
def health():
    return 'Reggie is alive'

if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=80)