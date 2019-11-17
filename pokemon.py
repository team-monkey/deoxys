import pokepy
import random
client = pokepy.V2Client()

MAX_POKENUM = 807

class Pokemon:

    def __init__(self, number):
        data = client.get_pokemon(number)

        # sets base stats
        for stat in data.stats:
            self.stats[stat.stat.name] = stat.base_stat

        self.stats['level'] = 100 # all lvl 100


class Team:

    def __init__(self):
        self.pokemons = [0] * 6

    def randomize(self):
        for i in range(6):
            self.pokemons[i] = client.get_pokemon(random.randint(1, MAX_POKENUM))


