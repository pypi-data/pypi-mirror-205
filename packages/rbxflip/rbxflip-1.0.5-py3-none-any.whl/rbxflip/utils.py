import requests
from bs4 import BeautifulSoup

class utils:
    def __init__(self):
        self.cli = requests.Session()

    def getshopitem(self):
        return self.cli.get('https://api.rbxflip.com/roblox/shop').json()

    def checkuser(self, user_id):
        players = []
        try:
            request = self.cli.get(f'https://api.rbxflip.com/users/{user_id}')
            soup = BeautifulSoup(request.text, 'html.parser')
            player_meta = soup.find_all('div', attrs={'class': 'pb-2 mb-3 item_cell shadow_md_35 shift_up_md mx-0'})
            for i, p in enumerate(player_meta):
                player_soup = BeautifulSoup(str(p), 'html.parser')
                username = player_soup.find('h6', attrs={'class': 'my-0 px-2 text-light py-1 text-truncate'}).get_text()
                value_data = [user.get_text().replace('R$ ', '') for user in player_soup.find_all('span', attrs={'class': 'text-truncate'})[1:]]
                user_stats = self.getuserstats(user_id)
                players.append(user([i+1, username, value_data[0], value_data[1], user_stats['total_wagers'], user_stats['total_wins'], user_stats['total_losses']]))
        except Exception as e:
            print(f"Error fetching players: {str(e)}")
        return players
    
    def getuserstats(self, user_id):
        stats = self.cli.get(f'https://api.rbxflip.com/wagers/users/{user_id}/stats?period=0').json()
        return [        
            stats['wagers']['total_wagers'],
            stats['wagers']['total_wins'],
            stats['wagers']['total_losses']
        ]

class user:
    def __init__(self, data: list):
        self.rank: int = data[6]
        self.name: str = data[5]
        self.display: int = data[8]
        self.wager: int = data[2]
        self.profit: int = data[3]
        self.total_losses: int = data[4]
