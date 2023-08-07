import requests
from .errors import PlayerNotFound


class user:
    def __str__(self):
        return self.name
        
    def player(self, id):
        request = requests.get(f'https://api.rbxflip.com/users/{id}').json()
        if request['success']:
            self.id: int = id
            self.name: str = request['name']
            self.roles: str = request['roles']
            self.tags: str = request['tags']
            self.rank: int = request['rank']
        else:
            raise PlayerNotFound(f'Player {id} does not exist')
    
    def wager(self, period=0):
        url = f'https://api.rbxflip.com/wagers/users/{self.id}/stats?period={period}'
        request = requests.get(url).json()
        if request['success']:
            self.wager: int = request['total_wagers']
            self.wins: int = request['total_wins']
            self.losses: int = request['total_losses']
        else:
            raise Exception('Error retrieving wager stats')
    
    def __init__(self, data: dict, key: str):
        self.name: str = key
        self.obtained: int = data[key]
