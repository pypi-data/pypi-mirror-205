import requests
from .errors import ItemNotFound

class shop:
    def __init__(self, id: int):
        self.id = id
        self.data = self.get_item_data()

    def __str__(self):
        return self.name

    def get_item_data(self):
        request = requests.get(f'https://api.rbxflip.com/roblox/shop').json()
        if request['success']:
            for item in request['data']:
                if item['id'] == self.id:
                    return item
            raise ItemNotFound(f'Item {self.id} does not exist')
        else:
            raise ItemNotFound(f'Item {self.id} does not exist')

    @property
    def name(self):
        return self.data['name']

    @property
    def rate(self):
        return self.data['rate']

    @property
    def price(self):
        return self.data['price']

    @property
    def rap(self):
        return self.data['value']


    @property
    def sellerid(self):
        return self.data['sellerid']
    
    @property
    def serial(self):
        return self.data['serial']
    
    @property
    def projected(self):
        return self.data['projected']