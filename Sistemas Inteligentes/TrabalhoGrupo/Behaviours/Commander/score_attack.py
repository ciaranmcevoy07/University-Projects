import random
from spade.behaviour import OneShotBehaviour


def manhattan_distance(x, y, targetx, targety):
    return abs(targetx - x) + abs(targety - y)


def choose_one_best_move(scores):
    best_score = -999
    best_moves = []
    for move in scores.keys():
        score = scores[move]
        if score > best_score:
            best_score = score
            best_moves.clear()
            best_moves.append(move)
        elif score == best_score:
            best_moves.append(move)
    return random.choice(best_moves)


class ScoreAttack(OneShotBehaviour):
    def __init__(self):
        super().__init__()
        self.sum = None
        self.min = None
        self.max_score = None
        self.tmp_matrix = []
        self.score_matrix = []
        self.coords = []
        self.next_coords = []
        self.deployed_allies = []

    async def on_end(self):
        self.agent.new_so()
        self.agent.enemies = {}

    async def on_start(self):
        self.min = 9999999999
        self.sum = 0
        self.max_score = self.agent.x_max + self.agent.y_max
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

    async def calculate_view_coords(self):
        for soldado in self.agent.soldiers_alive:
            x = self.agent.soldiers_alive[soldado].getCoordinates().getX()
            y = self.agent.soldiers_alive[soldado].getCoordinates().getY()
            x_inf = x - 3
            if x_inf < 0:
                x_inf = 0
            x_sup = x + 4
            if x_sup > self.agent.x_max:
                x_sup = self.agent.x_max
            y_inf = y - 3
            if y_inf < 0:
                y_inf = 0
            y_sup = y + 4
            if y_sup > self.agent.y_max:
                y_sup = self.agent.y_max
            for yy in range(y_inf, y_sup):
                for xx in range(x_inf, x_sup):
                    if [xx, yy] not in self.coords:
                        self.coords.append([xx, yy])

    async def reset_score_matrix(self, targetx, targety):
        self.score_matrix = []
        for yn in range(self.agent.y_max):
            line = []
            for xn in range(self.agent.x_max):
                line.append(None)
            self.score_matrix.append(line)

        for ally in self.deployed_allies:
            self.score_matrix[ally[1]][ally[0]] = "a"

        for enemy in self.agent.enemies:
            ex = self.agent.enemies[enemy].getCoordinates().getX()
            ey = self.agent.enemies[enemy].getCoordinates().getY()
            self.score_matrix[ey][ex] = "e"

        self.score_matrix[targety][targetx] = "t"

    async def calculate_score_matrix(self, x, y):
        if self.score_matrix[y][x] == "t":
            current_score = self.max_score + 1
        else:
            current_score = self.score_matrix[y][x]

        up = y + 1
        if [x, up] in self.coords and [x, up] not in self.next_coords and self.score_matrix[up][x] is None:
            self.score_matrix[up][x] = current_score - 1
            self.next_coords.append([x, up])

        down = y - 1
        if [x, down] in self.coords and [x, down] not in self.next_coords and self.score_matrix[down][x] is None:
            self.score_matrix[down][x] = current_score - 1
            self.next_coords.append([x, down])

        right = x + 1
        if [right, y] in self.coords and [right, y] not in self.next_coords and self.score_matrix[y][right] is None:
            self.score_matrix[y][right] = current_score - 1
            self.next_coords.append([right, y])

        left = x - 1
        if [left, y] in self.coords and [left, y] not in self.next_coords and self.score_matrix[y][left] is None:
            self.score_matrix[y][left] = current_score - 1
            self.next_coords.append([left, y])
        self.next_coords.remove([x, y])

    def verify_all_movements_scores(self, x, y, targetx, targety):
        movement_score = {}
        estimated = False

        # stay
        if self.score_matrix[y][x] is None:
            stay_score = self.max_score - manhattan_distance(x, y, targetx, targety)
            movement_score["stay"] = stay_score
            estimated = True
        elif type(self.score_matrix[y][x]) is int:
            movement_score["stay"] = self.score_matrix[y][x]
        else:
            movement_score["stay"] = 0

        # up
        if y < self.agent.y_max - 1 and self.score_matrix[y + 1][x] is None:
            up_score = self.max_score - manhattan_distance(x, y + 1, targetx, targety)
            movement_score["up"] = up_score
            estimated = True
        elif y < self.agent.y_max - 1 and type(self.score_matrix[y + 1][x]) is int:
            movement_score["up"] = self.score_matrix[y + 1][x]
        else:
            movement_score["up"] = 0

        # down
        if y > 0 and self.score_matrix[y - 1][x] is None:
            down_score = self.max_score - manhattan_distance(x, y - 1, targetx, targety)
            movement_score["down"] = down_score
            estimated = True
        elif y > 0 and type(self.score_matrix[y - 1][x]) is int:
            movement_score["down"] = self.score_matrix[y - 1][x]
        else:
            movement_score["down"] = 0

        # right
        if x < self.agent.x_max - 1 and self.score_matrix[y][x + 1] is None:
            right_score = self.max_score - manhattan_distance(x + 1, y, targetx, targety)
            movement_score["right"] = right_score
            estimated = True
        elif x < self.agent.x_max - 1 and type(self.score_matrix[y][x + 1]) is int:
            movement_score["right"] = self.score_matrix[y][x + 1]
        else:
            movement_score["right"] = 0

        # left
        if x > 0 and self.score_matrix[y][x - 1] is None:
            left_score = self.max_score - manhattan_distance(x - 1, y, targetx, targety)
            movement_score["left"] = left_score
            estimated = True
        elif x > 0 and type(self.score_matrix[y][x - 1]) is int:
            movement_score["left"] = self.score_matrix[y][x - 1]
        else:
            movement_score["left"] = 0

        if estimated:
            # up
            if y < self.agent.y_max - 1 and (self.score_matrix[y + 1][x] == "e" or self.score_matrix[y + 1][x] == "a"):
                if movement_score["down"] != 0:
                    movement_score["down"] += 2
                if movement_score["right"] != 0:
                    movement_score["right"] += 3
                if movement_score["left"] != 0:
                    movement_score["left"] += 3
            # down
            if y > 0 and (self.score_matrix[y - 1][x] == "e" or self.score_matrix[y - 1][x] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] += 2
                if movement_score["right"] != 0:
                    movement_score["right"] += 3
                if movement_score["left"] != 0:
                    movement_score["left"] += 3
            # right
            if x < self.agent.x_max - 1 and (self.score_matrix[y][x + 1] == "e" or self.score_matrix[y][x + 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] += 3
                if movement_score["down"] != 0:
                    movement_score["down"] += 3
                if movement_score["left"] != 0:
                    movement_score["left"] += 2
            # left
            if x > 0 and (self.score_matrix[y][x - 1] == "e" or self.score_matrix[y][x - 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] += 3
                if movement_score["down"] != 0:
                    movement_score["down"] += 3
                if movement_score["right"] != 0:
                    movement_score["right"] += 2

            # someone bottom-left
            if x > 1 and y > 1 and (self.score_matrix[y - 1][x - 1] == "e" or self.score_matrix[y - 1][x - 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] = self.max_score - manhattan_distance(x, y + 2, targetx, targety)
                if movement_score["down"] != 0:
                    movement_score["down"] = self.max_score - manhattan_distance(x, y - 2, targetx, targety)
                if movement_score["right"] != 0:
                    movement_score["right"] = self.max_score - manhattan_distance(x + 2, y, targetx, targety)
                if movement_score["left"] != 0:
                    movement_score["left"] = self.max_score - manhattan_distance(x - 2, y, targetx, targety)
            # someone bottom-right
            if x < self.agent.x_max - 2 and y > 1 and (self.score_matrix[y - 1][x + 1] == "e" or self.score_matrix[y - 1][x + 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] = self.max_score - manhattan_distance(x, y + 2, targetx, targety)
                if movement_score["down"] != 0:
                    movement_score["down"] = self.max_score - manhattan_distance(x, y - 2, targetx, targety)
                if movement_score["right"] != 0:
                    movement_score["right"] = self.max_score - manhattan_distance(x + 2, y, targetx, targety)
                if movement_score["left"] != 0:
                    movement_score["left"] = self.max_score - manhattan_distance(x - 2, y, targetx, targety)
            # someone top-left
            if x > 1 and y < self.agent.y_max - 2 and (self.score_matrix[y + 1][x - 1] == "e" or self.score_matrix[y + 1][x - 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] = self.max_score - manhattan_distance(x, y + 2, targetx, targety)
                if movement_score["down"] != 0:
                    movement_score["down"] = self.max_score - manhattan_distance(x, y - 2, targetx, targety)
                if movement_score["right"] != 0:
                    movement_score["right"] = self.max_score - manhattan_distance(x + 2, y, targetx, targety)
                if movement_score["left"] != 0:
                    movement_score["left"] = self.max_score - manhattan_distance(x - 2, y, targetx, targety)
            # someone top-right
            if x < self.agent.x_max - 2 and y < self.agent.y_max - 2 and (self.score_matrix[y + 1][x + 1] == "e" or self.score_matrix[y + 1][x + 1] == "a"):
                if movement_score["up"] != 0:
                    movement_score["up"] = self.max_score - manhattan_distance(x, y + 2, targetx, targety)
                if movement_score["down"] != 0:
                    movement_score["down"] = self.max_score - manhattan_distance(x, y - 2, targetx, targety)
                if movement_score["right"] != 0:
                    movement_score["right"] = self.max_score - manhattan_distance(x + 2, y, targetx, targety)
                if movement_score["left"] != 0:
                    movement_score["left"] = self.max_score - manhattan_distance(x - 2, y, targetx, targety)

        return movement_score

    async def update_deployment(self, ally, x, y, chosen_move):
        if chosen_move == "stay":
            self.tmp_matrix[y][x] = ally
            self.deployed_allies.append([x, y])
        if chosen_move == "up":
            self.tmp_matrix[y + 1][x] = ally
            self.deployed_allies.append([x, y + 1])
        if chosen_move == "down":
            self.tmp_matrix[y - 1][x] = ally
            self.deployed_allies.append([x, y - 1])
        if chosen_move == "right":
            self.tmp_matrix[y][x + 1] = ally
            self.deployed_allies.append([x + 1, y])
        if chosen_move == "left":
            self.tmp_matrix[y][x - 1] = ally
            self.deployed_allies.append([x - 1, y])

    async def run(self):
        # procura
        if len(self.agent.enemies) == 0:
            print("[{}] No enemies in sight. Going on recon mission.".format(self.agent.info.getTeam()))
            self.agent.new_rm()

        # ataque
        else:
            targetx = None
            targety = None

            for enemy in self.agent.enemies.keys():
                intel = self.agent.enemies[enemy]
                ex = int(intel.getCoordinates().getX())
                ey = int(intel.getCoordinates().getY())

                for ally in self.agent.soldiers_alive.keys():
                    stationed = self.agent.soldiers_alive[ally]
                    ax = int(stationed.getCoordinates().getX())
                    ay = int(stationed.getCoordinates().getY())
                    dist = manhattan_distance(ax, ay, ex, ey)
                    self.sum += dist

                if self.sum < self.min:
                    self.min = self.sum
                    targetx = ex
                    targety = ey

            print("[{}] Enemy in sight. Engaging enemy at x={}, y={}.".format(self.agent.info.getTeam(), targetx, targety))

            await self.calculate_view_coords()

            for ally in self.agent.soldiers_alive.keys():
                await self.reset_score_matrix(targetx, targety)

                self.next_coords = []
                self.next_coords.append([targetx, targety])
                while len(self.next_coords) > 0:
                    await self.calculate_score_matrix(self.next_coords[0][0], self.next_coords[0][1])

                x = self.agent.soldiers_alive[ally].getCoordinates().getX()
                y = self.agent.soldiers_alive[ally].getCoordinates().getY()
                scores = self.verify_all_movements_scores(x, y, targetx, targety)

                chosen_move = choose_one_best_move(scores)
                self.agent.orders[ally] = chosen_move

                await self.update_deployment(ally, x, y, chosen_move)

        self.kill()