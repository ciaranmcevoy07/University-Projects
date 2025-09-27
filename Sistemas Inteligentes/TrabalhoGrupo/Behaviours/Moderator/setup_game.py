from random import randrange
from spade.behaviour import FSMBehaviour, State
from constants import EXAMPLE

STARTING_POSITIONS = "initial state STARTING_POSITIONS"
RANDOM_TEAM = "final state RANDOM_TEAM"


class SetupGame(FSMBehaviour):
    async def on_start(self):
        print("------------------------------------------------------------------------------------------------------------")
        print("[{}] SetupGame starting at {}".format(self.agent.name, self.current_state))

    async def on_end(self):
        print("[{}] SetupGame finished at {}".format(self.agent.name, self.current_state))
        self.agent.new_inturn()
        self.agent.add_behaviour(self.agent.pnt)


class StartingPositions(State):
    async def not_random_at_all(self):
        if EXAMPLE == 4:
            coords = [[10, 10], [10, 15], [15, 15], [15, 10], [20, 15], [97, 96], [90, 90], [85, 90], [90, 85], [96, 97]]
        elif EXAMPLE == 5:
            coords = [[10, 90], [10, 85], [15, 85], [15, 90], [20, 85], [94, 3], [93, 3], [92, 3], [95, 3], [96, 3]]
        elif EXAMPLE == 6:
            coords = [[10, 10], [10, 15], [15, 15], [99, 99], [94, 98], [94, 96], [93, 96], [92, 96], [99, 98], [98, 99]]
        counter = 0
        for team in self.agent.registered_teams_dic.keys():
            for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                new_x = coords[counter][0]
                new_y = coords[counter][1]
                soldier.setCoordinates(new_x, new_y)
                self.agent.board.matrix[new_y][new_x] = soldier
                counter += 1

    async def truly_random(self):
        print("[{}] Randomized coordinates:".format(self.agent.name))
        for team in self.agent.registered_teams_dic.keys():
            for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                while True:
                    new_x = randrange(0, self.agent.x_max)
                    new_y = randrange(0, self.agent.y_max)
                    if self.agent.board.matrix[new_y][new_x] is None:
                        self.agent.board.matrix[new_y][new_x] = soldier
                        break
                soldier.setCoordinates(new_x, new_y)
                print(soldier.toString())

    async def run(self):
        if EXAMPLE in [4, 5, 6]:
            await self.not_random_at_all()
        else:
            await self.truly_random()
        self.set_next_state(RANDOM_TEAM)


class RandomTeam(State):
    async def on_end(self):
        print("[{}] Starting team is: {}".format(self.agent.name, self.agent.registered_teams_list[self.agent.playing_team]))

    async def run(self):
        self.agent.playing_team = randrange(0, len(self.agent.registered_teams_list))
