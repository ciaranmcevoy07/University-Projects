class InfoCommander:
    def __init__(self, agent_jid: str, team: str):
        self.agent_jid = agent_jid
        self.team = team

    def getAgent(self):
        return self.agent_jid

    def getTeam(self):
        return self.team

    def toString(self):
        return "[agent_jid=" + str(self.agent_jid) + ", team=" + self.team + "]"
