import random

import pandas as pd


class Innings:
    def __init__(self, batting_team, target=None, max_overs=20):
        self.batting_team = batting_team
        self.bowling_team = "team2" if self.batting_team == "team1" else "team1"
        self.target = target
        self.max_overs = max_overs
        self.total_runs = 0
        self.total_wickets = 0
        self.overs_completed = 0
        self.batting_card = {}
        self.batters = self.get_batters(self.batting_team)["name"].to_list()
        self.current_batters = {
            self.batters[0]: {"runs": 0, "balls": 0, "on_strike": True},
            self.batters[1]: {"runs": 0, "balls": 0, "on_strike": False},
        }
        self.current_batting_position = 1  # striker, non-striker
        self.bowling_card = {}
        self.bowlers = self.get_bowlers(self.bowling_team)["name"].to_list()
        self.fielders = self.get_batters(self.bowling_team)["name"].to_list()

    @staticmethod
    def isChadOrVirgin():
        random_three_digit_number = random.randint(100, 999)
        if random_three_digit_number % 7 == 0:
            return 1
        elif random_three_digit_number % 3 == 0:
            return -1
        else:
            return 0

    def get_batters(self, team):

        # read data from csv
        team_data = f"data/{team}.csv"
        team_df = pd.read_csv(team_data)

        # sanitize
        columns = {col: col.strip() for col in team_df.columns}
        team_df = team_df.rename(columns=columns)

        # filter for role = [bowler, all-rounder]
        team_df["name"] = team_df["first_name"] + " " + team_df["last_name"]
        team_df = team_df[["name", "bat_avg", "strike_rate", "highscore"]]

        return team_df

    def get_bowlers(self, team):

        # read data from csv
        team_data = f"data/{team}.csv"
        team_df = pd.read_csv(team_data)

        # sanitize
        columns = {col: col.strip() for col in team_df.columns}
        team_df = team_df.rename(columns=columns)

        # filter for role = [bowler, all-rounder]
        bowlers_df = team_df[
            (team_df["role"] == "bowler") | (team_df["role"] == "all-rounder")
        ]
        bowlers_df["name"] = bowlers_df["first_name"] + " " + bowlers_df["last_name"]
        bowlers_df = bowlers_df[["name", "bowl_avg", "economy", "best_figures"]]

        return bowlers_df

    def get_striker(self):
        for batsman in self.current_batters:
            if self.current_batters[batsman]["on_strike"]:
                return batsman

    def get_nonstriker(self):
        for batsman in self.current_batters:
            if not self.current_batters[batsman]["on_strike"]:
                return batsman

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

    def over(self, bowler, mode, runs_remaining, wickets_remaining):

        # define possibilities for a ball bowled
        possibilities = ["0", "1", "2", "3", "4", "6", "W"]

        # adjust weights depending on bowler's form
        if mode == 1:
            weights = (50, 40, 20, 10, 5, 0, 40)
        elif mode == -1:
            weights = (0, 10, 30, 20, 40, 40, 2)
        else:
            weights = (30, 40, 40, 30, 25, 15, 15)

        runs = 0
        wickets = 0
        balls_bowled = 0

        ball_by_ball = []

        for _ in range(6):
            current_striker = self.get_striker()
            current_nonstriker = self.get_nonstriker()

            event = random.choices(possibilities, weights=weights, k=1)[0]

            ball_by_ball.append(event)

            balls_bowled += 1

            if event == "W":
                wickets += 1

                self.current_batters[current_striker]["balls"] = (
                    self.current_batters[current_striker].get("balls", 0) + 1
                )
                self.batting_card[current_striker] = {
                    "runs": self.current_batters[current_striker]["runs"],
                    "balls": self.current_batters[current_striker]["balls"],
                    "out": self.get_mode_dismissal(bowler),
                }

                self.current_batters.pop(current_striker)

                if balls_bowled == 6:
                    on_strike = False
                    self.current_batters[current_nonstriker]["on_strike"] = True
                else:
                    on_strike = True

                # if all 10 wickets have not fallen, then update next batsman as current
                if self.current_batting_position < 10:
                    self.current_batting_position += 1
                    self.current_batters.update(
                        {
                            self.batters[self.current_batting_position]: {
                                "runs": 0,
                                "balls": 0,
                                "on_strike": on_strike,
                            }
                        }
                    )
                    current_striker = self.get_striker()
                    current_nonstriker = self.get_nonstriker()
                    print(f"{current_striker} in with {current_nonstriker}")
                else:
                    self.batting_card.update(
                        {
                            f"{current_nonstriker}": {
                                "runs": self.current_batters[current_nonstriker][
                                    "runs"
                                ],
                                "balls": self.current_batters[current_nonstriker][
                                    "balls"
                                ],
                                "out": "not out",
                            }
                        }
                    )
                    break
            else:
                runs += int(event)
                try:
                    self.current_batters[current_striker][
                        "runs"
                    ] = self.current_batters[current_striker].get("runs", 0) + int(
                        event
                    )
                    self.current_batters[current_striker]["balls"] = (
                        self.current_batters[current_striker].get("balls", 0) + 1
                    )

                    # change strike incase of singles
                    if int(event) % 2 == 0 and balls_bowled != 6:
                        pass
                    else:
                        self.current_batters[current_striker]["on_strike"] = False
                        self.current_batters[current_nonstriker]["on_strike"] = True

                    self.batting_card.update(
                        {
                            f"{current_striker}": {
                                "runs": self.current_batters[current_striker]["runs"],
                                "balls": self.current_batters[current_striker]["balls"],
                                "out": "not out",
                            },
                            f"{current_nonstriker}": {
                                "runs": self.current_batters[current_nonstriker][
                                    "runs"
                                ],
                                "balls": self.current_batters[current_nonstriker][
                                    "balls"
                                ],
                                "out": "not out",
                            },
                        }
                    )

                    # end innings if all wickets lost
                    # or target achieved
                    if wickets >= wickets_remaining or runs >= runs_remaining:
                        print("innings over!")
                        break

                except KeyError as ke:
                    print(f"key_error for {current_striker} / {current_nonstriker}")

        return runs, wickets, ball_by_ball

    def play(self):
        # init previous bowler so than end's change
        previous_bowler = ""

        # assign target to chase or 20*36 if first inn
        target = self.target if self.target else 720

        while (
            self.overs_completed < 20
            and self.total_wickets < 10
            and self.total_runs <= target
        ):
            # choose a bowler
            while True:
                bowler = random.choice(self.bowlers)
                if bowler != previous_bowler:
                    bowler_stats = self.bowling_card.get(bowler, {})
                    if bowler_stats.get("overs", 0) < 4:
                        break

            # get bowler's form
            mode = Innings.isChadOrVirgin()
            if mode == 1:
                bowlers_form = "chad"
            elif mode == -1:
                bowlers_form = "virgin"
            else:
                bowlers_form = "normal"

            # bowl the over
            runs, wickets, ball_by_ball = self.over(
                bowler, mode, target - self.total_runs, 10 - self.total_wickets
            )

            print(
                f"Over: {self.overs_completed + 1}, Bowler: {bowler}, {bowlers_form}, {ball_by_ball}, {runs}-{wickets}"
            )

            # scoring
            self.total_runs += runs
            self.total_wickets += wickets
            self.overs_completed = (
                self.overs_completed + 1
                if len(ball_by_ball) == 6
                else self.overs_completed + (len(ball_by_ball) / 10)
            )

            # build bowler card
            bowler_overs = (
                bowler_stats.get("overs", 0) + 1
                if len(ball_by_ball) == 6
                else bowler_stats.get("overs", 0) + (len(ball_by_ball) / 10)
            )
            bowler_runs = bowler_stats.get("runs", 0) + runs
            bowler_wickets = bowler_stats.get("wickets", 0) + wickets
            bowler_stats["overs"] = bowler_overs
            bowler_stats["runs"] = bowler_runs
            bowler_stats["wickets"] = bowler_wickets

            self.bowling_card[bowler] = bowler_stats

            # set current bowler as previous
            previous_bowler = bowler

    def display_bowling_card(self):
        for bowler in self.bowling_card:
            print(
                f'{bowler: <20} \t {self.bowling_card[bowler]["overs"]} - {self.bowling_card[bowler]["runs"]} - {self.bowling_card[bowler]["wickets"]}'
            )

    def display_batting_card(self):
        for batsman in self.batting_card:
            print(
                f'{batsman: <20} \t\t {self.batting_card[batsman]["out"]: <30} \t\t {self.batting_card[batsman]["runs"]: <5} ({self.batting_card[batsman]["balls"]})'
            )


if __name__ == "__main__":
    innings = Innings("team1")
    innings.play()
    innings.display_batting_card()
    innings.display_bowling_card()
