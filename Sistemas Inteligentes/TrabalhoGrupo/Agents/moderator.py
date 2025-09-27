from spade import agent
from Behaviours.Moderator.moderator_register import ModeratorRegister
from Behaviours.Moderator.setup_game import *
from Behaviours.Moderator.iniciate_next_turn import *
from Behaviours.Moderator.prepare_next_turn import PrepareNextTurn
from Classes.board import Board


class ModeratorAgent(agent.Agent):
    registered_soldiers_info = []  # matriz dos soldados vivos por equipa [número de equipa: int] [num: int] = info: InfoSoldado
    registered_teams_dic = {}  # dicionário das equipas em jogo (com soldados vivos) key = nome da equipa: str; value = número de equipa: int
    registered_teams_list = []  # lista das equipas registradas [número de equipa: int] = nome da equipa: str
    playing_team = None  # equipa a jogar no momento = número de equipa: int

    def __init__(self, jid: str, password: str, x_max: int, y_max: int, verify_security: bool = False):
        super().__init__(jid, password, verify_security)
        self.x_max = x_max
        self.y_max = y_max
        self.turn = 0
        self.board = Board(self.y_max, self.x_max)

        # Behabiours
        self.mr = ModeratorRegister()

        self.sg = SetupGame()
        self.sg.add_state(name=STARTING_POSITIONS, state=StartingPositions(), initial=True)
        self.sg.add_state(name=RANDOM_TEAM, state=RandomTeam())
        self.sg.add_transition(source=STARTING_POSITIONS, dest=RANDOM_TEAM)

        self.pnt = PrepareNextTurn()

    def new_inturn(self):
        inturn = IniciateNextTurn()
        inturn.add_state(name=SEARCH_SURROUNDED, state=SearchSurrounded(), initial=True)
        inturn.add_state(name=VERIFY_END, state=VerifyEnd())
        inturn.add_state(name=SEND_INFO, state=SendInfo())
        inturn.add_state(name=PLAY, state=Play())
        inturn.add_transition(source=SEARCH_SURROUNDED, dest=VERIFY_END)
        inturn.add_transition(source=VERIFY_END, dest=SEND_INFO)
        inturn.add_transition(source=SEND_INFO, dest=PLAY)
        self.add_behaviour(inturn)

    async def setup(self):
        print("Agent {} starting...".format(str(self.jid)))
        self.add_behaviour(self.mr)
