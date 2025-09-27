from spade import agent
from Behaviours.Soldier.soldier_register import SoldierRegister
from Behaviours.Soldier.soldier_receive import SoldierReceive
from Classes.infosoldado import InfoSoldado


class SoldierAgent(agent.Agent):
    info = InfoSoldado
    vision = []

    def __init__(self, jid: str, password: str, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.srg = SoldierRegister()
        self.src = SoldierReceive()

    async def setup(self):
        self.add_behaviour(self.srg)
        self.add_behaviour(self.src)
