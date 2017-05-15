# API endpoints listed here
# https://developer.riotgames.com/api-methods

URL = {
    'base': 'https://{region}.api.riotgames.com/lol/{url}',
    'league': 'league/{version}/leagues/by-summoner/{summonerId}',
    'match': 'match/{version}/matches/by-account/{accountId}',
    'spectate': 'spectator/{version}/active-games/by-summoner/{summonerId}'
}

API_VERSIONS = {
    'league': '3',
    'match': '3',
    'spectator': '3'
}

REGIONS = {
    'north_america': 'na',
    'europe_nordic_and_east': 'eune',
    'europe_west': 'euw',
    'korea': 'kr'
}