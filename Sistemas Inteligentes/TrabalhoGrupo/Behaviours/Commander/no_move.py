from spade.behaviour import OneShotBehaviour


class NoMove(OneShotBehaviour):
    async def on_end(self):
        self.agent.new_so()

    async def run(self):
        for soldier_jid in self.agent.soldiers_alive.keys():
            self.agent.orders[soldier_jid] = "stay"
