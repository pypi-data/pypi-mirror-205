import requests
from .errors import PlayerNotFound

class User:
    def __init__(self, data: dict, key: str):
        self.name: str = key
        self.obtained: int = data[key]
        self.id: int = None
        self.roles: str = None
        self.tags: str = None
        self.rank: int = None
        self.wager: int = None
        self.wins: int = None
        self.losses: int = None

    def __str__(self):
        return self.name

    def player(self, id):
        request = requests.get(f'https://api.rbxflip.com/users/{id}').json()
        if request['success']:
            self.id = id
            self.name = request['name']
            self.roles = request['roles']
            self.tags = request['tags']
            self.rank = request['rank']
        else:
            raise PlayerNotFound(f'Player {id} does not exist')

    def wager(self, period=0):
        url = f'https://api.rbxflip.com/wagers/users/{self.id}/stats?period={period}'
        request = requests.get(url).json()
        if request['success']:
            self.wager = request['total_wagers']
            self.wins = request['total_wins']
            self.losses = request['total_losses']
        else:
            raise Exception('Error retrieving wager stats')
