import random

from spade.behaviour import OneShotBehaviour


class RandomMove(OneShotBehaviour):
    def __init__(self):
        super().__init__()
        self.tmp_matrix = []

    async def on_start(self):
        self.agent.orders = {}
        for y in range(self.agent.x_max):
            line = []
            for x in range(self.agent.y_max):
                line.append(None)
            self.tmp_matrix.append(line)
        for enemy_jid in self.agent.enemies.keys():
            enemy = self.agent.enemies[enemy_jid]
            x = enemy.getCoordinates().getX()
            y = enemy.getCoordinates().getY()
            self.tmp_matrix[y][x] = enemy

    async def on_end(self):
        self.agent.new_so()
        self.agent.enemies = {}

    def random_move(self, soldier):
        random_possible_moves = []
        x = soldier.getCoordinates().getX()
        y = soldier.getCoordinates().getY()

        if self.tmp_matrix[y][x] is None:  # stay
            random_possible_moves.append("stay")
        if x > 0 and self.tmp_matrix[y][x - 1] is None:  # left
            random_possible_moves.append("left")
        if x < self.agent.x_max - 1 and self.tmp_matrix[y][x + 1] is None:  # right
            random_possible_moves.append("right")
        if y > 0 and self.tmp_matrix[y - 1][x] is None:  # down
            random_possible_moves.append("down")
        if y < self.agent.y_max - 1 and self.tmp_matrix[y + 1][x] is None:  # up
            random_possible_moves.append("up")

        random_chosen_move = random.choice(random_possible_moves)

        if random_chosen_move == "left":
            self.tmp_matrix[y][x - 1] = soldier
        elif random_chosen_move == "right":
            self.tmp_matrix[y][x + 1] = soldier
        elif random_chosen_move == "down":
            self.tmp_matrix[y - 1][x] = soldier
        elif random_chosen_move == "up":
            self.tmp_matrix[y + 1][x] = soldier
        else:  # random_chosen_move == "stay"
            self.tmp_matrix[y][x] = soldier

        return random_chosen_move

    async def run(self):
        for soldier_jid in self.agent.soldiers_alive.keys():
            soldier = self.agent.soldiers_alive[soldier_jid]
            soldier_random_move = self.random_move(soldier)
            self.agent.orders[str(soldier.getAgent())] = soldier_random_move
        self.kill()
