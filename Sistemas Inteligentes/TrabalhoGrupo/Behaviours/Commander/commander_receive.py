from spade.behaviour import CyclicBehaviour
import jsonpickle


class CommanderReceive(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=60)
        if msg:
            performative = msg.get_metadata("performative")

            if performative == "died":
                soldier = jsonpickle.decode(msg.body)
                self.agent.soldiers_alive.pop(str(soldier.getAgent()))

            elif performative == "soldier_intel":
                # Message is list[<info_soldado>, list[<info_enemy>]]
                intel = jsonpickle.decode(msg.body)

                soldier = intel[0]
                self.agent.soldiers_alive[str(soldier.getAgent())] = soldier

                for enemy in intel[1]:
                    if enemy not in self.agent.enemies.keys():
                        self.agent.enemies[str(enemy.getAgent())] = enemy
                self.agent.msg_counter += 1
                if self.agent.msg_counter == len(self.agent.soldiers_alive.keys()):
                    for soldier_jid in self.agent.soldiers_alive.keys():
                        soldier = self.agent.soldiers_alive[soldier_jid]
                        x = soldier.getCoordinates().getX()
                        y = soldier.getCoordinates().getY()
                    for enemy_jid in self.agent.enemies.keys():
                        enemy = self.agent.enemies[enemy_jid]
                        x = enemy.getCoordinates().getX()
                        y = enemy.getCoordinates().getY()
                    self.agent.msg_counter = 0
                    self.agent.new_hq()
            else:
                print("Agent {}:".format(str(self.agent.jid)) + " Message not understood!")
        else:
            print("Agent {}".format(str(self.agent.jid)) + " did not receive any message in 60 seconds")
