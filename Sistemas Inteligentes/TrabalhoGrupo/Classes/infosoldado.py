from Classes.coordinates import Coordinates


class InfoSoldado:
    def __init__(self, agent_jid: str, team: str, coordinates: Coordinates):
        self.agent_jid = agent_jid
        self.coordinates = coordinates
        self.team = team

    def getAgent(self):
        return self.agent_jid

    def getTeam(self):
        return self.team

    def getCoordinates(self):
        return self.coordinates

    def setCoordinates(self, x: int, y: int):
        self.coordinates = Coordinates(x, y)

    def setCoordinates2(self, coordinates: Coordinates):
        self.coordinates = coordinates

    def toString(self):
        return "[agent_jid=" + str(self.agent_jid) + ", team=" + self.team + ", " + self.coordinates.toString() + "]"
