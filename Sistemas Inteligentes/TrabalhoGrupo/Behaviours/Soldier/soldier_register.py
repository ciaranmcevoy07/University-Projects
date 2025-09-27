from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle


class SoldierRegister(OneShotBehaviour):
    async def run(self):
        msg = Message(to="moderator@{}".format(str(self.agent.jid).split("@")[1]))
        msg.body = jsonpickle.encode(self.agent.info)
        msg.set_metadata("performative", "register")
        await self.send(msg)
