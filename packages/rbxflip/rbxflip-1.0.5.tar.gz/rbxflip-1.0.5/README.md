An unofficial Python API wrapper for RBXFlip

RBXFlip is a roblox gambling website, and this libary lets you check many informations inside of the site like, listed items, roulette info, user info and more! 
Getting Started
pip install rbxflip

Quick Start 🛠️

import rbxflip


Check roulette info

```
from rbxflip import roulette

round_data = roulette()
print(round_data)
```

Check Shop Item

```
from rbxflip import shop

# create a new ShopItem object for the item with ID 123456
item = shop(123456)

# print out the name, rate, price, and RAP of the item
print(f"Name: {item.name}")
print(f"Rate: {item.rate}")
print(f"Price: {item.price}")
print(f"RAP: {item.rap}")
```


Check User

```
from rbxflip import user, PlayerNotFound

try:
    # Create a user object with the given ID
    user = user()
    user.player(123456)

    # Retrieve the wager statistics for the user
    user.wager()

    # Print the statistics
    print(f"Total wagers: {user.wager}")
    print(f"Total wins: {user.wins}")
    print(f"Total losses: {user.losses}")

except PlayerNotFound as e:
    print(e)
except Exception as e:
    print(f"An error occurred: {e}")

```

