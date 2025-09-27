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


def random_orientation():
    return random.choice([True, False])


class ScoreStrategy(OneShotBehaviour):
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

    async def reset_score_matrix_attack(self, targetx, targety):
        await self.reset_score_matrix(targetx, targety, "t")

    async def reset_score_matrix_search(self, targetx, targety):
        target_score = self.max_score + 1
        await self.reset_score_matrix(targetx, targety, target_score)

    async def reset_score_matrix(self, targetx, targety, target_value):
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

        if self.score_matrix[targety][targetx] != "a":
            self.score_matrix[targety][targetx] = target_value

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

    def left_or_right(self):
        x_sum = 0
        for soldier_jid in self.agent.soldiers_alive.keys():
            soldier_info = self.agent.soldiers_alive[soldier_jid]
            x = soldier_info.getCoordinates().getX()
            x_sum += x
        x_avg = x_sum/len(self.agent.soldiers_alive)
        if x_avg <= self.agent.x_max/2:
            return True
        else:
            return False

    def bottom_or_up(self):
        y_sum = 0
        for soldier_jid in self.agent.soldiers_alive.keys():
            soldier_info = self.agent.soldiers_alive[soldier_jid]
            y = soldier_info.getCoordinates().getY()
            y_sum += y
        y_avg = y_sum / len(self.agent.soldiers_alive)
        if y_avg <= self.agent.y_max / 2:
            return True
        else:
            return False

    def create_search_routes(self, vertical, bottom, left):
        x_max = self.agent.x_max
        y_max = self.agent.y_max
        n_alive = len(self.agent.soldiers_alive.keys())

        route = []
        for num in range(n_alive):
            route.append([])

        end = False
        band = 0
        if vertical:
            if bottom:
                while not end:
                    if 3 + 7 * n_alive * band + 7 * n_alive < y_max - 4:
                        for num in range(n_alive):
                            if left:
                                route[num].append([3, 3 + 7 * num + 7 * n_alive * band])
                                route[num].append([x_max - 4, 3 + 7 * num + 7 * n_alive * band])
                            else:
                                route[num].append([x_max - 4, 3 + 7 * num + 7 * n_alive * band])
                                route[num].append([3, 3 + 7 * num + 7 * n_alive * band])
                    else:
                        for num in range(n_alive):
                            if left:
                                route[num].append([3, y_max - 4 - 7 * (n_alive - 1 - num)])
                                route[num].append([x_max - 4, y_max - 4 - 7 * (n_alive - 1 - num)])
                            else:
                                route[num].append([x_max - 4, y_max - 4 - 7 * (n_alive - 1 - num)])
                                route[num].append([3, y_max - 4 - 7 * (n_alive - 1 - num)])
                        end = True
                    left = not left
                    band += 1
                return route
            else:
                while not end:
                    if y_max - 4 - 7 * n_alive * band - 7 * n_alive > 3:
                        for num in range(n_alive):
                            if left:
                                route[num].append([3, y_max - 4 - 7 * num - 7 * n_alive * band])
                                route[num].append([x_max - 4, y_max - 4 - 7 * num - 7 * n_alive * band])
                            else:
                                route[num].append([x_max - 4, y_max - 4 - 7 * num - 7 * n_alive * band])
                                route[num].append([3, y_max - 4 - 7 * num - 7 * n_alive * band])
                    else:
                        for num in range(n_alive):
                            if left:
                                route[num].append([3, 3 + 7 * (n_alive - 1 - num)])
                                route[num].append([x_max - 4, 3 + 7 * (n_alive - 1 - num)])
                            else:
                                route[num].append([x_max - 4, 3 + 7 * (n_alive - 1 - num)])
                                route[num].append([3, 3 + 7 * (n_alive - 1 - num)])
                        end = True
                    left = not left
                    band += 1
                return route
        else:
            if left:
                while not end:
                    if 3 + 7 * n_alive * band + 7 * n_alive < x_max - 4:
                        for num in range(n_alive):
                            if bottom:
                                route[num].append([3 + 7 * num + 7 * n_alive * band, 3])
                                route[num].append([3 + 7 * num + 7 * n_alive * band, y_max - 4])
                            else:
                                route[num].append([3 + 7 * num + 7 * n_alive * band, y_max - 4])
                                route[num].append([3 + 7 * num + 7 * n_alive * band, 3])
                    else:
                        for num in range(n_alive):
                            if bottom:
                                route[num].append([y_max - 4 - 7 * (n_alive - 1 - num), 3])
                                route[num].append([y_max - 4 - 7 * (n_alive - 1 - num), y_max - 4])
                            else:
                                route[num].append([y_max - 4 - 7 * (n_alive - 1 - num), y_max - 4])
                                route[num].append([y_max - 4 - 7 * (n_alive - 1 - num), 3])
                        end = True
                    bottom = not bottom
                    band += 1
                return route
            else:
                while not end:
                    if x_max - 4 - 7 * n_alive * band - 7 * n_alive > 3:
                        for num in range(n_alive):
                            if bottom:
                                route[num].append([x_max - 4 - 7 * num - 7 * n_alive * band, 3])
                                route[num].append([x_max - 4 - 7 * num - 7 * n_alive * band, y_max - 4])
                            else:
                                route[num].append([x_max - 4 - 7 * num - 7 * n_alive * band, y_max - 4])
                                route[num].append([x_max - 4 - 7 * num - 7 * n_alive * band, 3])
                    else:
                        for num in range(n_alive):
                            if bottom:
                                route[num].append([3 + 7 * (n_alive - 1 - num), 3])
                                route[num].append([3 + 7 * (n_alive - 1 - num), y_max - 4])
                            else:
                                route[num].append([3 + 7 * (n_alive - 1 - num), y_max - 4])
                                route[num].append([3 + 7 * (n_alive - 1 - num), 3])
                        end = True
                    bottom = not bottom
                    band += 1
                return route

    async def assign_route_to_soldier(self, routes):
        available_soldiers = []
        for soldier_jid in self.agent.soldiers_alive.keys():
            available_soldiers.append(self.agent.soldiers_alive[soldier_jid])

        for route in routes:
            starting_point = route[0]
            starting_point_x = starting_point[0]
            starting_point_y = starting_point[1]

            distances = {}
            for soldier_info in available_soldiers:
                soldier_x = soldier_info.getCoordinates().getX()
                soldier_y = soldier_info.getCoordinates().getY()
                distances[soldier_info] = manhattan_distance(soldier_x, soldier_y, starting_point_x, starting_point_y)

            closest_soldier = None
            smaller_distance = 2 * (self.agent.x_max + self.agent.y_max)
            for soldier_info in distances.keys():
                if distances[soldier_info] < smaller_distance:
                    smaller_distance = distances[soldier_info]
                    closest_soldier = soldier_info

            self.agent.search_routes[str(closest_soldier.getAgent())] = route
            available_soldiers.remove(closest_soldier)

    def verify_formation(self):
        formation = True
        for soldier_jid in self.agent.soldiers_alive.keys():
            soldier_info = self.agent.soldiers_alive[soldier_jid]
            soldier_x = soldier_info.getCoordinates().getX()
            soldier_y = soldier_info.getCoordinates().getY()
            soldier_target_position = self.agent.search_routes[soldier_jid]
            soldier_target_x = soldier_target_position[0][0]
            soldier_target_y = soldier_target_position[0][1]
            if [soldier_x, soldier_y] != [soldier_target_x, soldier_target_y]:
                formation = False
        return formation

    async def run(self):
        # procura
        if len(self.agent.enemies) == 0:
            print("[{}] No enemies in sight. Going on recon mission.".format(self.agent.info.getTeam()))

            if len(self.agent.search_routes) != 0:
                if self.verify_formation():
                    for soldier_jid in self.agent.search_routes.keys():
                        self.agent.search_routes[soldier_jid].remove(self.agent.search_routes[soldier_jid][0])
                        if len(self.agent.search_routes[soldier_jid]) == 0:
                            self.agent.search_routes.pop(soldier_jid)

            if len(self.agent.search_routes) == 0:
                vertical = random_orientation()
                left = self.left_or_right()
                bottom = self.bottom_or_up()
                routes = self.create_search_routes(vertical, bottom, left)
                await self.assign_route_to_soldier(routes)

            for soldier_jid in self.agent.search_routes.keys():
                route = self.agent.search_routes[soldier_jid]
                targetx = route[0][0]
                targety = route[0][1]
                await self.reset_score_matrix_search(targetx, targety)

                x = self.agent.soldiers_alive[soldier_jid].getCoordinates().getX()
                y = self.agent.soldiers_alive[soldier_jid].getCoordinates().getY()
                scores = self.verify_all_movements_scores(x, y, targetx, targety)

                chosen_move = choose_one_best_move(scores)
                self.agent.orders[soldier_jid] = chosen_move

                await self.update_deployment(soldier_jid, x, y, chosen_move)

        # ataque
        else:
            self.agent.search_routes = {}

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
                await self.reset_score_matrix_attack(targetx, targety)

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
