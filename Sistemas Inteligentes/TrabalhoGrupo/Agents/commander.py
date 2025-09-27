from spade import agent
from Behaviours.Commander.commander_receive import CommanderReceive
from Behaviours.Commander.headquarters import Headquarters
from Behaviours.Commander.no_move import NoMove
from Behaviours.Commander.random_move import RandomMove
from Behaviours.Commander.score_attack import ScoreAttack
from Behaviours.Commander.score_strategy import ScoreStrategy
from Behaviours.Commander.send_orders import SendOrder
from Classes.infocommander import InfoCommander


class CommanderAgent(agent.Agent):
    info = InfoCommander
    soldiers_alive = {}  # dicionário dos soldados vivos: key = JID; value = InfoSoldado
    enemies = {}  # dicionário dos enemivos à vista: key = JID; value = InfoSoldado
    orders = {}  # dicionário dos movimentos que soldados vivos têm de fazer: key = JID; value = move: str ("stay", "up", "down", "left", "right")
    msg_counter = None

    def __init__(self, jid: str, password: str, x_max: int, y_max: int, verify_security: bool = False):
        super().__init__(jid, password, verify_security)

        self.x_max = x_max
        self.y_max = y_max
        self.msg_counter = 0
        self.search_routes = {}  # dicionário dos percursos de procura dos soldados vivos: key = JID; value = list

        self.cr = CommanderReceive()

    def new_hq(self):
        hq = Headquarters()
        self.add_behaviour(hq)

    def new_nm(self):
        nm = NoMove()
        self.add_behaviour(nm)

    def new_rm(self):
        rm = RandomMove()
        self.add_behaviour(rm)

    def new_sa(self):
        sa = ScoreAttack()
        self.add_behaviour(sa)

    def new_ss(self):
        ss = ScoreStrategy()
        self.add_behaviour(ss)

    def new_so(self):
        so = SendOrder()
        self.add_behaviour(so)



    async def setup(self):
        print("Agent {}".format(str(self.jid)) + " starting...")
        self.add_behaviour(self.cr)
