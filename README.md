# Reggie 0.0.7-alpha

## Run
```
$ docker build -t reggie .
$ docker run -e 'DB_USERNAME=uname' -e 'DB_PASSWORD=pw' -e 'DB_URL=mysqlurl' reggie
```

## Usage
Reggie exposes its methods as a REST API and can also be used as a Slack bot.
```
{
	"in_progress": false,
	"players": [],
	"bans": [],
	"friendly_picks": [],
	"enemy_picks": []
}
```

## 0.1 roadmap:
- refactor
- draft_hero
    - force draft hero for player, role, or both
- player x hero permutation calculations
- soft pairings - if we've already picked crystal-maiden for gilgi, return `drow-ranger - global xx%, gilgi yy% - manlytomb (zz%) takes crystal-maiden`

## 0.2:
- experiment with the weights between "player good on hero" and "hero good globally"
- /draft suggest by role/player/both

## 1.0:
- hero name aliases
- player aliases
- list heroes by role, roles by hero
- more informative and more decorative prints
- more selection parameters? favor versatility? pick cores last?
- user lock
- list the top reasons why this is a good pick
- add browser string to request to avoid dotabuff rate limit OR
- calculate stats yourself by grabbing the last month of pub games
    - recalculate existing stats
    - synergies between heroes on the same team
- use globals instead of the local file
- move roles to the db instead of local file
- unit tests? lol

## X.X (probably never):
- calculate permutations of the other team too; try to generate laning suggestions by expected matchup (oh yeah, this'll work)
- draft logging + fetching + editing? (gross)
- fetch hero names from API? (painful because Dota names != Dotabuff names != Opendota names, hero pool changes infrequently)
