import requests

class roulette:
    def __init__(self, data: dict):
        self.round = data['round']
        self.id = data['id']
        self.players = data['players']
        self.client_seed = data['clientSeed']

    def __str__(self):
        return f"Round: {self.round}\nID: {self.id}\nPlayers: {self.players}\nClient Seed: {self.client_seed}"

def roulette():
    r = requests.get('https://api.rbxflip.com/games/roulette').json()
    return roulette(r)
