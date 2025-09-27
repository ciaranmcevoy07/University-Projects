from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle


class SoldierReceive(CyclicBehaviour):
    def __init__(self):
        super().__init__()
        self.server = None

    async def on_start(self):
        self.server = str(self.agent.jid).split("@")[1]

    async def run(self):
        msg = await self.receive(timeout=60)
        if msg:
            performative = msg.get_metadata("performative")

            if performative == "inform":
                self.agent.vision = []
                body = jsonpickle.decode(msg.body)
                for soldier in body:
                    if soldier.getAgent() == self.agent.info.getAgent():
                        self.agent.info.setCoordinates2(soldier.getCoordinates())
                    if soldier.getTeam() != self.agent.info.getTeam():
                        self.agent.vision.append(soldier)

            elif performative == "your_turn":
                new_msg = Message(to="commander_{}@{}".format(self.agent.info.getTeam(), self.server))
                intel = [self.agent.info, self.agent.vision]
                new_msg.body = jsonpickle.encode(intel)
                new_msg.set_metadata("performative", "soldier_intel")
                await self.send(new_msg)

            elif performative == "movement_order":
                new_msg = Message(to="moderator@{}".format(self.server))
                direction = jsonpickle.decode(msg.body)
                ask_move = [self.agent.info.getAgent(), direction]
                new_msg.body = jsonpickle.encode(ask_move)
                new_msg.set_metadata("performative", "ask_move")
                await self.send(new_msg)

            elif performative == "order_kill":
                print("[{}] Died!".format(self.agent.name))
                new_msg = Message(to="commander_{}@{}".format(self.agent.info.getTeam(), self.server))
                new_msg.body = jsonpickle.encode(self.agent.info)
                new_msg.set_metadata("performative", "died")
                await self.send(new_msg)
                await self.agent.stop()

            else:
                print("Agent {}: Message not understood!".format(str(self.agent.jid)))
        else:
            print("Agent {}: did not receive any message in 60 seconds".format(str(self.agent.jid)))
