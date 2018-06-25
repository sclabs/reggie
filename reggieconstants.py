default_response = '''I didn't understand that. Try these:
`start player1 player2...`: Starts a new draft with specified players.
`draft heroname`: Drafts a hero to your team for flexible player. I'll figure out the best player-hero matches at the end.
`draft player heroname`: Drafts a hero to your team for a specific player. Use `pub` for a pub teammate.
`draft enemy heroname`: Drafts a hero to the enemy team.
`cancel`: Immediately ends the current draft.

When you aren't in the middle of a draft, you can do these too:
`addplayer name ID`: Adds a player to my database.
`removeplayer name`: Removes a player from my database.
`listplayers`: Returns all the players in my database.
`reload`: Reloads per-hero player winrates, global hero winrates, and maybe hero roles if those are coming from somewhere.

`info`: Find out more about yours truly.'''

infotext = '''```[SC] Reggie v0.0.4 alpha
bug tracker:
- 500s on wrong names instead of returning response -> unexpected results

v0.1 roadmap:
- reload
    - get player-hero frequencies and winrates
- draft_hero
    - return a situational recommendation after each pick
        - use player-hero winrates (filtered by frequency)
    - additional arguments
        - draft to enemy team
        - draft to pub teammate
        - force draft hero for player, role, or both

v1.0:
- bans
- /draft suggest by role/player/both
- hero name aliases
- player aliases
- list heroes by role, roles by hero
- more informative and more decorative prints
- more selection parameters? favor versatility? pick cores last?
- user lock
- list the top reasons why this is a good pick
- add browser string to request to avoid dotabuff rate limit

vX.X (probably never):
- synergies between heroes on the same team
- calculate permutations of the other team too; try to generate laning suggestions by expected matchup (oh yeah, this'll work)
- draft logging + fetching + editing? (gross)
- fetch hero names from API? (painful because Dota names != Dotabuff names != Opendota names, hero pool changes infrequently)```'''

global_hero_list = ['abaddon', 'alchemist', 'axe', 'beastmaster', 'brewmaster', 'bristleback', 'centaur-warrunner', 'chaos-knight', 'clockwerk', 'doom', 'dragon-knight', 'earth-spirit', 'earthshaker', 'elder-titan', 'huskar', 'io', 'kunkka', 'legion-commander', 'lifestealer', 'lycan', 'magnus', 'night-stalker', 'omniknight', 'phoenix', 'pudge', 'sand-king', 'slardar', 'spirit-breaker', 'sven', 'tidehunter', 'timbersaw', 'tiny', 'treant-protector', 'tusk', 'underlord', 'undying', 'wraith-king', 'anti-mage', 'arc-warden', 'bloodseeker', 'bounty-hunter', 'broodmother', 'clinkz', 'drow-ranger', 'ember-spirit', 'faceless-void', 'gyrocopter', 'juggernaut', 'lone-druid', 'luna', 'medusa', 'meepo', 'mirana', 'monkey-king', 'morphling', 'naga-siren', 'nyx-assassin', 'pangolier', 'phantom-assassin', 'phantom-lancer', 'razor', 'riki', 'shadow-fiend', 'slark', 'sniper', 'spectre', 'templar-assassin', 'terrorblade', 'troll-warlord', 'ursa', 'vengeful-spirit', 'venomancer', 'viper', 'weaver', 'ancient-apparition', 'bane', 'batrider', 'chen', 'crystal-maiden', 'dark-seer', 'dark-willow', 'dazzle', 'death-prophet', 'disruptor', 'enchantress', 'enigma', 'invoker', 'jakiro', 'keeper-of-the-light', 'leshrac', 'lich', 'lina', 'lion', 'natures-prophet', 'necrophos', 'ogre-magi', 'oracle', 'outworld-devourer', 'puck', 'pugna', 'queen-of-pain', 'rubick', 'shadow-demon', 'shadow-shaman', 'silencer', 'skywrath-mage', 'storm-spirit', 'techies', 'tinker', 'visage', 'warlock', 'windranger', 'winter-wyvern', 'witch-doctor', 'zeus']
