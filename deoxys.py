import pokepy
import random
client = pokepy.V2Client()

MAX_POKENUM = 807

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

        self.types = []
        self.types = [x.type.name for x in data.types]

    # returns type effectiveness based on the attacking and defending
    # pokemon's types
    # @staticmethod
    # def type_effectiveness(attacking_types, defending_types):

    # @staticmethod
    # def single_type_effectiveness(attacking_type, defending_type)


# stores pokemon team informations
class Team:

    def __init__(self):
        self.pokemons = [0] * 6
        self.fainted = False

    def randomize(self):
        for i in range(6):
            self.pokemons[i] = client.get_pokemon(random.randint(1, MAX_POKENUM))

    # battles another team and returns
    # a 1 if the current (self) team wins
    # else 0 (other wins)
    def battle(self, other):

        turn = 1 # 1 == self, 0 == other
        self_index = 0
        other_index = 0
        # while (not self.fainted) and (not other.fainted):




# creates a new simulation
# inital = # of inital pokemon teams
# iterations = # of iterations the simulation goes through
# mutation_rate = how often mutations occur (higher = more often)
class Simulation:

    def __init__(self, inital, iterations, mutation_rate):
        self.inital = inital
        self.iterations = iterations
        self.mutation_rate = mutation_rate
        self.teams = [0] * inital

        for i in range(inital):
            temp = Team()
            temp.randomize()
            self.teams[i] = temp

    def battle_phase():
        fitnesses = []

        # for i in range(self.iterations):
            # for j in range(self.iterations - 1):


    # start the simulation
    def start(self):

        for i in range(self.iterations):
            fitnesses = battle

        # battle all

        # select fittest

        # mutate

        # iterate once more
