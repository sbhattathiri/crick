import random

import pandas as pd

from batting import Batter, BattingPair


class Innings:
    @staticmethod
    def get_players(team, role="batters"):

        # read data from csv
        team_data = f"teams/{team}.csv"
        team_df = pd.read_csv(team_data)

        # sanitize
        columns = {col: col.strip() for col in team_df.columns}
        team_df = team_df.rename(columns=columns)

        if role == "bowlers":
            bowlers_df = team_df[(team_df["role"] == "bowler") | (team_df["role"] == "all-rounder")]
            bowlers_df["name"] = bowlers_df["first_name"] + " " + bowlers_df["last_name"]
            df = bowlers_df[["name", "bowl_avg", "economy", "best_figures"]]
        else:
            team_df["name"] = team_df["first_name"] + " " + team_df["last_name"]
            df = team_df[["name", "bat_avg", "strike_rate", "highscore"]]

        return df

    @staticmethod
    def isChadOrVirgin():
        random_three_digit_number = random.randint(100, 999)
        if random_three_digit_number % 7 == 0:
            return 1
        elif random_three_digit_number % 3 == 0:
            return -1
        else:
            return 0

    def __init__(
        self,
        batting_team,
        bowling_team,
        target=None,
        overs_per_innings=20,
        max_overs_per_bowler=4,
        weights={
            1: (60, 50, 30, 0, 5, 0, 40, 0, 0),
            -1: (0, 10, 30, 20, 40, 40, 2, 20, 20),
            0: (30, 40, 40, 30, 25, 15, 15, 5, 5),
        },
    ):
        self.batting_team = batting_team
        self.bowling_team = bowling_team
        self.target = target
        self.overs_per_innings = overs_per_innings
        self.max_overs_per_bowler = max_overs_per_bowler
        self.weights = weights
        self.extras = 0
        self.wides = 0
        self.no_balls = 0
        self.total_runs = 0
        self.total_wickets = 0
        self.overs_completed = 0
        self.batting_card = {}
        self.batters = self.get_players(self.batting_team, "batters")["name"].to_list()
        self.current_batters = BattingPair(striker=Batter(self.batters[0]), non_striker=Batter(self.batters[1]))
        self.current_batting_position = 1  # striker, non-striker
        self.bowling_card = {}
        self.bowlers = self.get_players(self.bowling_team, "bowlers")["name"].to_list()
        self.fielders = self.get_players(self.bowling_team)["name"].to_list()

    @property
    def striker(self):
        return self.current_batters.striker

    @property
    def non_striker(self):
        return self.current_batters.non_striker

    def get_mode_dismissal(self, bowler):
        possibilities = ["caught", "lbw", "bowled"]
        dismissal_mode = random.choice(possibilities)
        if dismissal_mode == "caught":
            catcher = random.choice(self.fielders)
            if catcher == bowler:
                dismissal = f"c & b {bowler}"
            else:
                dismissal = f"c {catcher} b {bowler}"
        elif dismissal_mode == "lbw":
            dismissal = f"lbw b {bowler}"
        else:
            dismissal = f"b {bowler}"

        return dismissal

    def update_batting_card(self, name, runs, balls_faced, dismissal):
        batting_card = self.batting_card
        batter_data = {"runs": runs, "balls": balls_faced, "dismissal": dismissal}
        batting_card.update({name: batter_data})

    def over(self, bowler, mode, runs_remaining, wickets_remaining):

        # define possibilities for a ball bowled
        possibilities = ["0", "1", "2", "3", "4", "6", "W", "Wd", "Nb"]

        # adjust weights depending on bowler's form
        _weights = self.weights[mode]

        balls_bowled = 0
        runs = 0
        wickets = 0

        ball_by_ball = []
        fow = []
        while balls_bowled < 6:
            event = random.choices(possibilities, weights=_weights, k=1)[0]
            ball_by_ball.append(event)

            balls_bowled += 1

            if event == "Wd":
                self.wides += 1
                self.extras += 1
                self.total_runs += 1

                balls_bowled -= 1
                runs += 1
            elif event == "Nb":
                self.no_balls += 1
                self.extras += 1
                self.total_runs += 1
                self.current_batters.striker.score(0)

                balls_bowled -= 1
                runs += 1
            elif event == "W":
                self.total_wickets += 1

                wickets += 1

                fow.append(f"{self.current_batters.striker.name: <30} {self.total_runs}/{self.total_wickets}")

                self.current_batters.striker.score(0)

                self.update_batting_card(
                    name=self.current_batters.striker.name,
                    runs=self.current_batters.striker.runs,
                    balls_faced=self.current_batters.striker.balls_faced,
                    dismissal=self.get_mode_dismissal(bowler),
                )

                del self.current_batters.striker

                if self.current_batting_position < 10:
                    self.current_batting_position += 1
                    self.current_batters.striker = Batter(self.batters[self.current_batting_position])
                else:
                    self.update_batting_card(
                        name=self.current_batters.non_striker.name,
                        runs=self.current_batters.non_striker.runs,
                        balls_faced=self.current_batters.non_striker.balls_faced,
                        dismissal="not out",
                    )
                    break

                if balls_bowled == 6:
                    self.current_batters.change_strike()

            else:
                self.total_runs += int(event)

                runs += int(event)

                self.current_batters.striker.score(int(event))

                if not (int(event) % 2 == 0 and balls_bowled != 6):
                    self.current_batters.change_strike()

                self.update_batting_card(
                    name=self.current_batters.striker.name,
                    runs=self.current_batters.striker.runs,
                    balls_faced=self.current_batters.striker.balls_faced,
                    dismissal="not out",
                )
                self.update_batting_card(
                    name=self.current_batters.non_striker.name,
                    runs=self.current_batters.non_striker.runs,
                    balls_faced=self.current_batters.non_striker.balls_faced,
                    dismissal="not out",
                )

                # end innings if all wickets lost
                # or target achieved
                if wickets >= wickets_remaining or runs >= runs_remaining:
                    print("innings over!")
                    break

        return balls_bowled, runs, wickets, ball_by_ball, fow

    def play(self):
        fall_of_wicket = []
        over_by_over = []
        previous_bowler = ""
        # assign target to chase or 450*36 if first inn
        target = self.target if self.target else 16200

        while self.overs_completed < self.overs_per_innings and self.total_wickets < 10 and self.total_runs <= target:
            # choose a bowler
            while True:
                bowler = random.choice(self.bowlers)
                if bowler != previous_bowler:
                    bowler_stats = self.bowling_card.get(bowler, {})
                    if bowler_stats.get("overs", 0) < self.max_overs_per_bowler:
                        break

            # get bowler's form
            mode = Innings.isChadOrVirgin()

            # bowl the over
            balls_bowled, runs, wickets, ball_by_ball, fow = self.over(
                bowler, mode, target - self.total_runs, 10 - self.total_wickets
            )
            fall_of_wicket += fow
            over_by_over.append(f"Over: {self.overs_completed + 1}, Bowler: {bowler},{ball_by_ball}, {runs}/{wickets}")

            # scoring
            self.overs_completed = (
                self.overs_completed + 1 if balls_bowled == 6 else self.overs_completed + balls_bowled / 10
            )

            # build bowler card
            bowler_overs = (
                bowler_stats.get("overs", 0) + 1
                if balls_bowled == 6
                else bowler_stats.get("overs", 0) + balls_bowled / 10
            )
            bowler_runs = bowler_stats.get("runs", 0) + runs
            bowler_wickets = bowler_stats.get("wickets", 0) + wickets
            bowler_stats["overs"] = bowler_overs
            bowler_stats["runs"] = bowler_runs
            bowler_stats["wickets"] = bowler_wickets

            self.bowling_card[bowler] = bowler_stats

            # set current bowler as previous
            previous_bowler = bowler

        self.update_batting_card(
            name="extras",
            runs=self.extras,
            balls_faced=(f"W : {self.wides}, Nb : {self.no_balls}"),
            dismissal="",
        )

        return over_by_over, self.batting_card, self.bowling_card, fall_of_wicket
