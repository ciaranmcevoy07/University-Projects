from spade.behaviour import CyclicBehaviour
import jsonpickle


class PrepareNextTurn(CyclicBehaviour):
    def __init__(self):
        super().__init__()
        self.counter = None
        self.consistency = True
        self.soldiers_movement = {}
        self.number = None
        self.tmp_matrix = []
        self.valid_soldiers = []
        self.possible_movements = ["stay", "up", "down", "left", "right"]

    async def restore_variables(self):
        self.counter = 0
        self.consistency = True
        self.soldiers_movement = {}
        self.valid_soldiers = []
        for soldier in self.agent.registered_soldiers_info[self.agent.playing_team]:
            self.valid_soldiers.append(soldier.getAgent())

    async def restore_tmp_matrix(self):
        self.tmp_matrix = []
        for y in range(self.agent.y_max):
            line = []
            for x in range(self.agent.x_max):
                line.append(None)
            self.tmp_matrix.append(line)
        for line in self.agent.board.matrix:
            for el in line:
                if el is not None:
                    if el.getTeam() != self.agent.registered_teams_list[self.agent.playing_team]:
                        x = el.getCoordinates().getX()
                        y = el.getCoordinates().getY()
                        self.tmp_matrix[y][x] = el

    async def restore_number(self):
        self.number = len(self.agent.registered_soldiers_info[self.agent.playing_team])

    async def on_start(self):
        await self.restore_variables()
        await self.restore_tmp_matrix()
        await self.restore_number()

    async def make_next_moves(self):
        await self.restore_tmp_matrix()

        # Primeiro, certifica-se que os movimentos são válidos
        for soldier in self.agent.registered_soldiers_info[self.agent.playing_team]:
            x = soldier.getCoordinates().getX()
            y = soldier.getCoordinates().getY()
            if self.soldiers_movement[soldier.getAgent()] == "up":
                if y < self.agent.y_max - 1 and self.tmp_matrix[y + 1][x] is None:
                    self.tmp_matrix[y + 1][x] = soldier
                else:
                    self.consistency = False
            elif self.soldiers_movement[soldier.getAgent()] == "down":
                if y > 0 and self.tmp_matrix[y - 1][x] is None:
                    self.tmp_matrix[y - 1][x] = soldier
                else:
                    self.consistency = False
            elif self.soldiers_movement[soldier.getAgent()] == "left":
                if x > 0 and self.tmp_matrix[y][x - 1] is None:
                    self.tmp_matrix[y][x - 1] = soldier
                else:
                    self.consistency = False
            elif self.soldiers_movement[soldier.getAgent()] == "right":
                if x < self.agent.x_max - 1 and self.tmp_matrix[y][x + 1] is None:
                    self.tmp_matrix[y][x + 1] = soldier
                else:
                    self.consistency = False
            else:  # self.soldiers_movement[soldier.getAgent()] == "stay"
                if self.tmp_matrix[y][x] is None:
                    self.tmp_matrix[y][x] = soldier
                else:
                    self.consistency = False

        # Só se todos os movimentos forem válidos (self.consistency == True) é que os realiza
        if self.consistency:
            for soldier in self.agent.registered_soldiers_info[self.agent.playing_team]:
                x = soldier.getCoordinates().getX()
                y = soldier.getCoordinates().getY()
                if self.soldiers_movement[soldier.getAgent()] == "up":
                    if self.agent.board.matrix[y][x] == soldier:
                        self.agent.board.matrix[y][x] = None
                    self.agent.board.matrix[y + 1][x] = soldier
                    soldier.setCoordinates(x, y + 1)
                elif self.soldiers_movement[soldier.getAgent()] == "down":
                    if self.agent.board.matrix[y][x] == soldier:
                        self.agent.board.matrix[y][x] = None
                    self.agent.board.matrix[y - 1][x] = soldier
                    soldier.setCoordinates(x, y - 1)
                elif self.soldiers_movement[soldier.getAgent()] == "left":
                    if self.agent.board.matrix[y][x] == soldier:
                        self.agent.board.matrix[y][x] = None
                    self.agent.board.matrix[y][x - 1] = soldier
                    soldier.setCoordinates(x - 1, y)
                elif self.soldiers_movement[soldier.getAgent()] == "right":
                    if self.agent.board.matrix[y][x] == soldier:
                        self.agent.board.matrix[y][x] = None
                    self.agent.board.matrix[y][x + 1] = soldier
                    soldier.setCoordinates(x + 1, y)
                # else self.soldiers_movement[soldier] == "stay"
                # se o movimento "stay" é válido não é preciso alterar nada
        else:
            print("[{}] Plays were inconsistent with the rules, skiping this turn".format(self.agent.name))

    async def calculate_next_team(self):
        found = False
        while not found:
            if self.agent.playing_team == len(self.agent.registered_teams_list) - 1:
                self.agent.playing_team = 0
            else:
                self.agent.playing_team += 1
            if self.agent.registered_teams_list[self.agent.playing_team] in self.agent.registered_teams_dic.keys():
                found = True

    async def run(self):
        while self.counter < self.number:
            msg = await self.receive(timeout=60)
            if msg:
                performative = msg.get_metadata("performative")
                if performative == "ask_move":
                    # msg.body = [agent_jid: JID, movement: str]
                    request = jsonpickle.decode(msg.body)
                    if request[0] in self.valid_soldiers:
                        if request[1] in self.possible_movements:
                            self.soldiers_movement[request[0]] = request[1]
                            self.counter = len(self.soldiers_movement.keys())
                            await self.restore_number()
                else:
                    print("Agent {}: Message not understood!".format(str(self.agent.jid)))
            else:
                print("Agent {} did not receive any message in 60 seconds".format(str(self.agent.jid)))
        await self.make_next_moves()
        await self.calculate_next_team()
        self.agent.new_inturn()
        await self.restore_variables()

