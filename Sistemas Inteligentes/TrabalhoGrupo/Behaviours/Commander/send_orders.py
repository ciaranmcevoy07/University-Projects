from spade.behaviour import OneShotBehaviour
from spade.message import Message
import jsonpickle


class SendOrder(OneShotBehaviour):
    async def on_end(self) -> None:
        self.agent.orders = {}

    async def run(self):
        for soldier_jid in self.agent.orders.keys():
            order = self.agent.orders[soldier_jid]
            msg = Message(to=soldier_jid)
            msg.body = jsonpickle.encode(order)
            msg.set_metadata("performative", "movement_order")
            await self.send(msg)
        self.kill()
