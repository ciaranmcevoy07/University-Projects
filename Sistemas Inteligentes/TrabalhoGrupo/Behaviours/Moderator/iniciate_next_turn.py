from spade.behaviour import FSMBehaviour, State
from spade.message import Message
from Classes.infosoldado import InfoSoldado
import jsonpickle


SEARCH_SURROUNDED = "initial state SEARCH_SURROUNDED"
VERIFY_END = "2nd state VERIFY_END"
SEND_INFO = "3rd state SEND_INFO"
PLAY = "final state PLAY"


class IniciateNextTurn(FSMBehaviour):
    async def on_start(self):
        self.agent.turn += 1
        print("------------------------------------------------------------------------------------------------------------")
        print("[{}] IniciateNextTurn (turn {}) starting at {}".format(self.agent.name, self.agent.turn, self.current_state))

    async def on_end(self):
        print("[{}] IniciateNextTurn finished at {}".format(self.agent.name, self.current_state))


class SearchSurrounded(State):
    def surrounded(self, soldier: InfoSoldado):
        x = soldier.getCoordinates().getX()
        y = soldier.getCoordinates().getY()

        left = False
        if x == 0:
            left = True
        else:
            if self.agent.board.matrix[y][x - 1] is not None:
                left = True

        right = False
        if x == self.agent.x_max - 1:
            right = True
        else:
            if self.agent.board.matrix[y][x + 1] is not None:
                right = True

        down = False
        if y == 0:
            down = True
        else:
            if self.agent.board.matrix[y - 1][x] is not None:
                down = True

        up = False
        if y == self.agent.y_max - 1:
            up = True
        else:
            if self.agent.board.matrix[y + 1][x] is not None:
                up = True

        return up and down and right and left

    async def order_kill(self, soldier):
        msg = Message(to=str(soldier.getAgent()))
        msg.set_metadata("performative", "order_kill")
        await self.send(msg)

        x = soldier.getCoordinates().getX()
        y = soldier.getCoordinates().getY()
        self.agent.board.matrix[y][x] = None
        self.agent.registered_soldiers_info[self.agent.registered_teams_dic[soldier.getTeam()]].remove(soldier)

    async def run(self):
        for team in list(self.agent.registered_teams_dic):
            for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                if self.surrounded(soldier):
                    await self.order_kill(soldier)
            if len(self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]) < 2:
                if len(self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]) == 1:
                    for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                        await self.order_kill(soldier)
                self.agent.registered_teams_dic.pop(team)
        self.set_next_state(VERIFY_END)


class VerifyEnd(State):
    async def run(self):
        if len(self.agent.registered_teams_dic.keys()) < 2:
            if len(self.agent.registered_teams_dic.keys()) == 1:
                for team in self.agent.registered_teams_dic.keys():
                    print("[{}] Game ended, team {} won!".format(self.agent.name, team))
            else:
                print("[{}] The game ended in a tie".format(self.agent.name))
            await self.agent.stop()
            self.kill()
        self.set_next_state(SEND_INFO)


class SendInfo(State):
    def vision_search(self, soldier: InfoSoldado):
        x = soldier.getCoordinates().getX()
        y = soldier.getCoordinates().getY()

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

        vision = []
        for i in range(y_inf, y_sup):
            for j in range(x_inf, x_sup):
                if self.agent.board.matrix[i][j] is not None:
                    vision.append(self.agent.board.matrix[i][j])
        return vision

    async def run(self):
        for team in self.agent.registered_teams_dic.keys():
            for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                vision = self.vision_search(soldier)
                msg = Message(to=str(soldier.getAgent()))
                msg.body = jsonpickle.encode(vision)
                msg.set_metadata("performative", "inform")
                await self.send(msg)
        self.set_next_state(PLAY)


class Play(State):
    async def run(self):
        for team in self.agent.registered_teams_dic.keys():
            for soldier in self.agent.registered_soldiers_info[self.agent.registered_teams_dic[team]]:
                if soldier.getTeam() == self.agent.registered_teams_list[self.agent.playing_team]:
                    msg = Message(to=str(soldier.getAgent()))
                    msg.body = jsonpickle.encode("go")
                    msg.set_metadata("performative", "your_turn")
                    await self.send(msg)
