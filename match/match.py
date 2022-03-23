import argparse
import uuid
from pathlib import Path

from innings import Innings

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument(
    "-f", "--format", type=str, choices=["T20", "ODI", "Test"], help="The format. Can be one of [T20, ODI, Test]"
)


class Match:
    @staticmethod
    def create_simulations_dump_folder(format, match_id):
        curr_dir = Path.cwd()
        simulations_dump_folder = curr_dir / "simulations" / format / match_id
        simulations_dump_folder_path = Path(simulations_dump_folder)
        simulations_dump_folder_path.mkdir(parents=True)
        return simulations_dump_folder_path

    @staticmethod
    def display(simuations_path, l, card_type, innings):
        dump_file = simuations_path / f"{innings}_{card_type}.txt"
        with dump_file.open("w") as f:
            for entry in l:
                print(f"{entry}")
                f.write(f"{entry}\n")

    @staticmethod
    def display_bowling_card(simuations_path, bowling_card, innings):
        dump_file = simuations_path / f"{innings}_bowling.txt"
        with dump_file.open("w") as f:
            for bowler in bowling_card:
                print(
                    f'{bowler: <20} \t {bowling_card[bowler]["overs"]} - {bowling_card[bowler]["runs"]} - {bowling_card[bowler]["wickets"]}'
                )
                f.write(
                    f'{bowler: <20} \t {bowling_card[bowler]["overs"]} - {bowling_card[bowler]["runs"]} - {bowling_card[bowler]["wickets"]}\n'
                )

    @staticmethod
    def display_batting_card(simuations_path, batting_card, innings):
        dump_file = simuations_path / f"{innings}_batting.txt"
        with dump_file.open("w") as f:
            for batsman in batting_card:
                balls_faced = f'({batting_card[batsman]["balls"]})' if batting_card[batsman]["balls"] else ""
                print(
                    f'{batsman: <20} \t\t {batting_card[batsman]["dismissal"]: <40} \t\t {batting_card[batsman]["runs"]: <3} {balls_faced}'
                )
                f.write(
                    f'{batsman: <20} \t\t {batting_card[batsman]["dismissal"]: <40} \t\t {batting_card[batsman]["runs"]: <3} {balls_faced}\n'
                )

    def __init__(self, format, home_team, opposition_team):
        self.format = format
        self.home_team = home_team
        self.opposition_team = opposition_team
        self.match_id = str(uuid.uuid4()).replace("-", "")

        # create folder to dump simulation data
        self.simulations_path = Match.create_simulations_dump_folder(self.format, self.match_id)

    def play(self):
        if self.format == "T20":
            total_match_overs = 40
            no_of_innings = 2
            overs_per_innings = 20
            max_overs_per_bowler = 4
            weights = {
                1: (30, 30, 10, 5, 5, 0, 20, 0, 0),
                -1: (0, 5, 10, 10, 25, 40, 2, 6, 2),
                0: (30, 35, 15, 5, 10, 3, 2, 0, 0),
            }
        elif self.format == "ODI":
            total_match_overs = 100
            no_of_innings = 2
            overs_per_innings = 50
            max_overs_per_bowler = 10
            weights = {
                1: (40, 30, 5, 5, 0, 0, 20, 0, 0),
                -1: (0, 5, 10, 5, 45, 30, 1, 3, 1),
                0: (30, 35, 15, 5, 10, 3, 2, 0, 0),
            }
        else:
            total_match_overs = 450
            no_of_innings = 4
            overs_per_innings = 450
            max_overs_per_bowler = 225
            weights = {
                1: (60, 10, 5, 0, 0, 0, 25, 0, 0),
                -1: (0, 25, 25, 5, 25, 15, 1, 3, 1),
                0: (30, 35, 15, 5, 10, 3, 2, 0, 0),
            }

        innings_scores = {}
        innings_id = 1
        overs_completed = 0
        min_runs_reqd = None  # test 3rd innings

        while innings_id <= no_of_innings and overs_completed < total_match_overs:

            # innings conf
            if innings_id == 1:
                target = None
                batting_team = self.home_team
                bowling_team = self.opposition_team
            elif innings_id == 2:
                if self.format == "Test":
                    target = None
                else:
                    target = innings_scores[1] + 1
                batting_team = self.opposition_team
                bowling_team = self.home_team
            elif innings_id == 3:
                if innings_scores[1] - innings_scores[2] > 200:
                    # enforce follow-on
                    batting_team = self.opposition_team
                    bowling_team = self.home_team

                min_runs_reqd = abs(innings_scores[1] - innings_scores[2])
                batting_team = self.home_team
                bowling_team = self.opposition_team
            else:
                if innings_scores[1] - innings_scores[2] > 200:
                    # following-on scenario
                    target = (innings_scores[3] + innings_scores[2]) - innings_scores[1] + 1
                else:
                    target = (innings_scores[3] + innings_scores[1]) - innings_scores[2] + 1
                batting_team = self.opposition_team
                bowling_team = self.home_team

            # play
            innings = Innings(
                batting_team=batting_team,
                bowling_team=bowling_team,
                target=target,
                overs_per_innings=overs_per_innings,
                max_overs_per_bowler=max_overs_per_bowler,
                weights=weights,
            )
            over_by_over, batting_card, bowling_card, fall_of_wicket = innings.play()
            overs_completed += len(over_by_over)

            Match.display(
                simuations_path=self.simulations_path,
                l=over_by_over,
                card_type="over_by_over",
                innings=f"innings_{innings_id}",
            )
            Match.display_batting_card(
                simuations_path=self.simulations_path,
                batting_card=batting_card,
                innings=f"innings_{innings_id}",
            )
            Match.display_bowling_card(
                simuations_path=self.simulations_path,
                bowling_card=bowling_card,
                innings=f"innings_{innings_id}",
            )
            Match.display(
                simuations_path=self.simulations_path,
                l=fall_of_wicket,
                card_type="fow",
                innings=f"innings_{innings_id}",
            )

            innings_scores[innings_id] = innings.total_runs

            innings_id += 1

            if min_runs_reqd:
                if innings.total_runs < min_runs_reqd:
                    print("match over!")
                    break


if __name__ == "__main__":
    args = arg_parser.parse_args()
    match = Match(format=args.format, home_team="team1", opposition_team="team2")
    match.play()
