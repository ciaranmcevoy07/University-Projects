from spade.behaviour import CyclicBehaviour
import jsonpickle


class ModeratorRegister(CyclicBehaviour):
    async def on_end(self):
        self.agent.add_behaviour(self.agent.sg)

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            if performative == "register":
                soldier = jsonpickle.decode(msg.body)
                if soldier.getTeam() not in self.agent.registered_teams_dic.keys():
                    self.agent.registered_teams_list.append(soldier.getTeam())
                    self.agent.board.teams[soldier.getTeam()] = len(self.agent.registered_teams_dic.keys())
                    self.agent.registered_teams_dic[soldier.getTeam()] = len(self.agent.registered_teams_dic.keys())
                    self.agent.registered_soldiers_info.append([])
                self.agent.registered_soldiers_info[self.agent.registered_teams_dic[soldier.getTeam()]].append(soldier)
                print("[{}] {} added to the {} team".format(self.agent.name, str(soldier.getAgent()), soldier.getTeam()))
            else:
                print("Agent {}: Message not understood!".format(str(self.agent.jid)))
        else:
            print("[{}] Register time ended".format(self.agent.name))
            self.kill()
