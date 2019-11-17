import pokepy
import random
import pprint
client = pokepy.V2Client()

MAX_POKENUM = 807
LEVEL = 100

# stores pokemon information
class Pokemon:

    def __init__(self, number):
        data = client.get_pokemon(number)

        random.shuffle(data.moves)
        self.moves = [client.get_move(x.move.url[31:-1]) for x in data.moves[:4]]

        # sets base stats
        self.stats = {}
        for stat in data.stats:
            self.stats[stat.stat.name] = stat.base_stat

        self.stats['level'] = 100 # all lvl 100
        self.adaptability = True if 'adaptability' in [x.ability.name for x in data.abilities] else False

        self.types = []
        self.types = [x.type.name for x in data.types]

    # calculates damage done by a move given stats
    def dmg(self, attack, defense, power, stab, type_effect):
        mod = random.uniform(0.85, 1.0) * stab * type_effect
        return ((((((2*LEVEL) / 5) + 2) * power * (attack / defense)) / 50) + 2) * mod

    # returns highest dmg possible
    def best_move(self, defense, defending_types):
        max_dmg = 0
        for move in self.moves:
            move_type = move.type.name
            move_power = 0 if move.power is None else move.power
            stab = (2 if self.adaptability else 1.5) if move_type in self.types else 1
            type_effect = Pokemon.type_effectiveness(move_type, defending_types)

            dmg = self.dmg(self.stats['attack'], defense, move_power, stab, type_effect)
            if dmg > max_dmg:
                max_dmg = dmg

        return max_dmg


    # returns type effectiveness based on the attacking and defending
    # pokemon's types
    @staticmethod
    def type_effectiveness(attacking_type, defending_types):
        effectiveness = 1
        for dt in defending_types:
            effectiveness *= Pokemon.single_type_effectiveness(attacking_type, dt)

        return effectiveness


    @staticmethod
    def single_type_effectiveness(attacking_type, defending_type):
        if attacking_type == 'normal':
            if defending_type == 'ghost':
                return 0
            elif defending_type in ['rock', 'steel']:
                return 0.5
            else:
                return 1
        elif attacking_type == 'fighting':
            if defending_type == 'ghost':
                return 0
            elif defending_type in ['flying', 'poison', 'bug', 'psychic', 'fairy']:
                return 0.5
            elif defending_type in ['normal', 'rock', 'steel', 'ice', 'dark']:
                return 2
            else:
                return 1
        elif attacking_type == 'flying':
            if defending_type in ['rock', 'steel', 'electric']:
                return 0.5
            elif defending_type in ['fighting', 'bug', 'grass']:
                return 2
            else:
                return 1
        elif attacking_type == 'poison':
            if defending_type == 'steel':
                return 0
            elif defending_type in ['poison', 'ground', 'rock', 'ghost']:
                return 0.5
            elif defending_type in ['grass', 'fairy']:
                return 2
            else:
                return 1
        elif attacking_type == 'ground':
            if defending_type == 'flying':
                return 0
            elif defending_type in ['bug', 'grass']:
                return 0.5
            elif defending_type in ['poison', 'rock', 'steel', 'fire', 'electric']:
                return 2
            else:
                return 1
        elif attacking_type == 'rock':
            if defending_type in ['fighting', 'ground', 'steel']:
                return 0.5
            elif defending_type in ['flying', 'bug', 'fire', 'ice']:
                return 2
            else:
                return 1
        elif attacking_type == 'bug':
            if defending_type in ['fighting', 'flying', 'poison', 'ghost', 'steel', 'fire', 'fairy']:
                return 0.5
            elif defending_type in ['grass', 'psychic', 'dark']:
                return 2
            else:
                return 1
        elif attacking_type == 'ghost':
            if defending_type == 'normal':
                return 0
            elif defending_type == 'dark':
                return 0.5
            elif defending_type in ['ghost', 'psychic']:
                return 2
            else:
                return 1
        elif attacking_type == 'steel':
            if defending_type in ['steel', 'fire', 'water', 'electric']:
                return 0.5
            elif defending_type in ['rock', 'ice', 'fairy']:
                return 2
            else:
                return 1
        elif attacking_type == 'fire':
            if defending_type in ['rock', 'fire', 'water', 'dragon']:
                return 0.5
            elif defending_type in ['bug', 'steel', 'grass', 'ice']:
                return 2
            else:
                return 1
        elif attacking_type == 'water':
            if defending_type in ['water', 'grass', 'dragon']:
                return 0.5
            elif defending_type in ['ground', 'rock', 'fire']:
                return 2
            else:
                return 1
        elif attacking_type == 'grass':
            if defending_type in ['flying', 'poison', 'bug', 'steel', 'fire', 'grass', 'dragon']:
                return 0.5
            elif defending_type in ['ground', 'rock', 'water']:
                return 2
            else:
                return 1
        elif attacking_type == 'electric':
            if defending_type == 'ground':
                return 0
            elif defending_type in ['grass', 'electric', 'dragon']:
                return 0.5
            elif defending_type in ['flying', 'water']:
                return 2
            else:
                return 1
        elif attacking_type == 'psychic':
            if defending_type == 'dark':
                return 0
            elif defending_type in ['steel', 'psychic']:
                return 0.5
            elif defending_type in ['fighting', 'poison']:
                return 2
            else:
                return 1
        elif attacking_type == 'ice':
            if defending_type in ['steel', 'fire', 'water', 'ice']:
                return 0.5
            elif defending_type in ['flying', 'ground', 'grass', 'dragon']:
                return 2
            else:
                return 1
        elif attacking_type == 'dragon':
            if defending_type == 'fairy':
                return 0
            elif defending_type == 'steel':
                return 0.5
            elif defending_type == 'dragon':
                return 2
            else:
                return 1
        elif attacking_type == 'dark':
            if defending_type in ['fighting', 'dark', 'fairy']:
                return 0.5
            elif defending_type in ['ghost', 'psychic']:
                return 2
            else:
                return 1
        elif attacking_type == 'fairy':
            if defending_type in ['poison', 'steel', 'fire']:
                return 0.5
            elif defending_type in ['fighting', 'dragon', 'dark']:
                return 2
            else:
                return 1

        return 1 # wtf ??? (shouldnt be possible to get to)



# stores pokemon team informations
class Team:

    def __init__(self):
        self.pokemons = [0] * 6

    def randomize(self):
        for i in range(6):
            self.pokemons[i] = Pokemon(random.randint(1, MAX_POKENUM))

    # battles another team and returns
    # a 1 if the current (self) team wins
    # else 0 (other wins)
    def battle(self, other):

        turn = 1 # 1 == self, 0 == other
        self_index = 0
        other_index = 0

        self_hp = [x.stats['hp'] for x in self.pokemons]
        other_hp = [x.stats['hp'] for x in other.pokemons]

        while True:
            if turn == 1:
                # self's turn
                turn = 0
                other_hp[other_index] -= self.pokemons[self_index].best_move(other.pokemons[other_index].stats['defense'], other.pokemons[other_index].types)
                if other_hp[other_index] <= 0:
                    other_index += 1

                    if other_index == 6:
                        return 1

            else:
                # other's turn
                turn = 1
                self_hp[self_index] -= other.pokemons[other_index].best_move(self.pokemons[self_index].stats['defense'], self.pokemons[self_index].types)
                if self_hp[self_index] <= 0:
                    self_index += 1

                    if self_index == 6:
                        return 0


def sortSecond(val):
    return val[1]

# creates a new simulation
# initial = # of initial pokemon teams
# iterations = # of iterations the simulation goes through
# mutation_rate = how often mutations occur (higher = more often)
class Simulation:

    def __init__(self, initial, iterations, mutation_rate):
        self.initial = initial
        self.iterations = iterations
        self.mutation_rate = mutation_rate
        self.teams = [0] * initial

        for i in range(initial):
            temp = Team()
            temp.randomize()
            self.teams[i] = temp

    def battle_phase(self):
        fitnesses = [0] * self.initial

        i = 0
        for team1 in self.teams:
            for team2 in [x for x in self.teams if x is not team1]:
                fitnesses[i] += team1.battle(team2)

            i += 1

        return [(ind, x) for ind, x in enumerate(fitnesses)]

    def crossover(self, parent1, parent2):
        index = random.randint(1, 4)
        temp1 = parent1[:index] + parent2[index:]
        temp2 = parent2[:index] + parent1[index:]

        return (temp1, temp2)

    def breed(self, fitnesses):
        temp_teams = [0] * self.initial
        top = .1 * self.initial

        for i in range(self.initial):
            temp_teams[i] = crossover(self.teams[random.randint(0, top)], self.teams[random.randint(0, top)])

        self.teams = temp_teams

    def mutate(self):
        for i in range(self.initial):
            if random.randint(0, 100) <= mutation_rate:
                self.teams[i].pokemons[random.randint(0,5)] = Pokemon(random.randint(1, MAX_POKENUM))


    # start the simulation
    def start(self):
        pp = pprint.PrettyPrinter(depth=6)
        for i in range(self.iterations):
            # battle all
            fitnesses = self.battle_phase()

            # select fittest
            fitnesses.sort(key = sortSecond)

            if i != self.iterations - 1:
                # breed uwu
                self.breed(fitnesses)

                # mutate
                self.mutate()

        pp.pprint(self.teams)
