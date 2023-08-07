import requests

class Roulette:
    def __init__(self, data: dict):
        roulette_data = data['roulette']
        self.round = roulette_data['round']
        self.id = roulette_data['id']
        self.players = roulette_data['players']
        self.client_seed = roulette_data['clientSeed']


    def __str__(self):
        return f"Round: {self.round}\nID: {self.id}\nPlayers: {self.players}\nClient Seed: {self.client_seed}"

def get_roulette():
    r = requests.get('https://api.rbxflip.com/games/roulette').json()
    return Roulette(r)
