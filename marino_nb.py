import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _(team):
    import marimo as mo
    import random


    class Innings:
        def __init__(self, team):
            self.events = [0, 1, 2, 3, 4, 5, 6, "W", "WD", "NB"]
            self.weights = [25, 25, 12, 8, 15, 1, 9, 2, 1, 2]
            self.total_runs = 0
            self.total_wickets = 0
            self.team = team
            self.striker = 0
            self.partner = 1
            self.next_batter = 2
            self.scorecard = {
                team_member: {
                    "dismissed": False,
                    "runs": 0,
                    "balls": 0,
                    "fours": 0,
                    "sixes": 0,
                }
                for team_member in team
            }

        def set_striker(self, striker=0):
            self.striker = striker

        def get_striker(self):
            return self.striker

        def set_partner(self, partner=1):
            self.partner = partner

        def swap_striker(self):
            self.striker, self.partner = self.partner, self.striker

        def event(self):
            return random.choices(self.events, weights=self.weights)[0]

        def display_scorecard(self):
            formatted_scorecard = [
                {
                    "player": team_member,
                    "dismissal": (
                        "OUT"
                        if self.scorecard.get(team_member)["dismissed"]
                        else "NOT OUT"
                        if self.scorecard.get(team_member)["balls"]
                        else ""
                    ),
                    "runs": self.scorecard.get(team_member)["runs"]
                    if self.scorecard.get(team_member)["balls"]
                    else "",
                    "balls": self.scorecard.get(team_member)["balls"]
                    if self.scorecard.get(team_member)["balls"]
                    else "",
                    "4s": self.scorecard.get(team_member)["fours"]
                    if self.scorecard.get(team_member)["balls"]
                    else "",
                    "6s": self.scorecard.get(team_member)["sixes"]
                    if self.scorecard.get(team_member)["balls"]
                    else "",
                }
                for team_member in team
            ]
            return mo.ui.table(data=formatted_scorecard, pagination=True)

        def innings(self, overs):
            all_out = False
            over_index = 0
            self.set_striker(0)
            self.set_partner(1)
            while over_index < overs:
                ball_index = 1
                while ball_index < 7:
                    event = self.event()
                    if event == "W":
                        striker = self.team[self.striker]
                        self.scorecard.get(striker)["dismissed"] = True
                        self.scorecard.get(striker)["balls"] += 1
                        self.total_wickets += 1

                        print(
                            f"{over_index}.{ball_index} {striker} OUT, TEAM SCORE: {self.total_runs}/{self.total_wickets}"
                        )

                        self.set_striker(self.next_batter)
                        self.next_batter += 1
                        ball_index += 1
                        if self.total_wickets == 10:
                            all_out = True
                            break
                    elif event in ["WD", "NB"]:
                        self.total_runs += 1
                        print(
                            f"{over_index}.{ball_index} {event}, TEAM SCORE: {self.total_runs}/{self.total_wickets}"
                        )
                    else:
                        striker = self.team[self.striker]
                        self.scorecard.get(striker)["runs"] += event
                        self.total_runs += event
                        self.scorecard.get(striker)["balls"] += 1

                        print(
                            f"{over_index}.{ball_index} {striker}, {event} RUNS, TEAM SCORE: {self.total_runs}/{self.total_wickets}"
                        )

                        if event in [1, 3, 5]:
                            self.swap_striker()

                        if event == 4:
                            self.scorecard.get(striker)["fours"] += 1

                        if event == 6:
                            self.scorecard.get(striker)["sixes"] += 1

                        ball_index += 1

                if all_out:
                    break

                over_index += 1
                self.swap_striker()
    return (Innings,)


@app.cell
def _():
    team = [
        "Sanju Samson",
        "Abhishek Sharma",
        "Sreyas Iyer",
        "Tilak Varma",
        "Surya Kumar Yadav",
        "Hardik Pandya",
        "Axar Patel",  
        "Kuldeep Yadav",
        "Mohammed Shami",
        "Arshdeep Singh",
        "Varun Chakravarthy"
    ]
    return (team,)


@app.cell
def _(Innings, team):
    inn = Innings(team)
    inn.innings(20)
    return (inn,)


@app.cell
def _(inn):
    inn.display_scorecard()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
