class Batter:
    def __init__(self, name) -> None:
        self._name = name
        self._runs = 0
        self._balls_faced = 0
        self._dismissal = "not out"

    @property
    def name(self):
        return self._name

    @property
    def runs(self):
        return self._runs

    @property
    def balls_faced(self):
        return self._balls_faced

    def score(self, runs):
        self._runs += runs
        self._balls_faced += 1

    def dismissed(self):
        self._balls_faced += 1


class BattingPair:
    def __init__(self, striker, non_striker):
        self._striker = striker
        self._non_striker = non_striker

    @property
    def striker(self):
        return self._striker

    @striker.setter
    def striker(self, striker):
        self._striker = striker

    @striker.deleter
    def striker(self):
        del self._striker

    @property
    def non_striker(self):
        return self._non_striker

    @non_striker.setter
    def non_striker(self, non_striker):
        self._non_striker = non_striker

    def change_strike(self):
        self.striker, self.non_striker = self.non_striker, self.striker
