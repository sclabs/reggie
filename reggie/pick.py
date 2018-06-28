"""Functions for hero selection."""

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
            return 'According to my database, there are no more valid role permutations of your heroes. Killing the draft.'

        response = 'Got it. Please draft one of these roles: *'
        rec_pool = []

        for index in range(0, len(still_draftable)):
            if still_draftable[index] is True:
                rec_pool = list(set(rec_pool + heroes_by_role[str(index+1)]))
                response += str(index+1) + ' '
        current_draft['rec_pool'] = [x for x in rec_pool if (
            x not in current_draft['friendlies'] and x not in current_draft['enemies'])]
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
