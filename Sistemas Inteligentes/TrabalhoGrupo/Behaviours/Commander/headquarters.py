from spade.behaviour import OneShotBehaviour
from constants import EXAMPLE, TEAM_NAMES


class Headquarters(OneShotBehaviour):
    async def run(self):
        if EXAMPLE == 0:
            self.agent.new_nm()
        elif EXAMPLE == 1:
            self.agent.new_rm()
        elif EXAMPLE == 2:
            self.agent.new_sa()
        elif EXAMPLE in [3, 4, 5, 6]:
            self.agent.new_ss()
        elif EXAMPLE == 7:
            if self.agent.info.getTeam() == TEAM_NAMES[0]:
                self.agent.new_ss()
            else:
                self.agent.new_nm()
        elif EXAMPLE == 8:
            if self.agent.info.getTeam() == TEAM_NAMES[0]:
                self.agent.new_ss()
            else:
                self.agent.new_rm()
