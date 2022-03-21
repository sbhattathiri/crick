import uuid
from pathlib import Path

from innings import Innings


class Match:
    @staticmethod
    def create_simulations_dump_folder(match_id):
        curr_dir = Path.cwd()
        simulations_dump_folder = curr_dir / "simulations" / match_id
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

    def __init__(self, home_team, opposition_team):
        self.home_team = home_team
        self.opposition_team = opposition_team
        self.match_id = str(uuid.uuid4()).replace("-", "")

        # create folder to dump simulation data
        self.simulations_path = Match.create_simulations_dump_folder(self.match_id)

    def play(self):
        first_innings = Innings(batting_team=self.home_team, bowling_team=self.opposition_team)
        over_by_over, batting_card, bowling_card, fall_of_wicket = first_innings.play()
        Match.display(
            simuations_path=self.simulations_path,
            l=over_by_over,
            card_type="over_by_over",
            innings="first_innings",
        )
        Match.display_batting_card(
            simuations_path=self.simulations_path,
            batting_card=batting_card,
            innings="first_innings",
        )
        Match.display_bowling_card(
            simuations_path=self.simulations_path,
            bowling_card=bowling_card,
            innings="first_innings",
        )
        Match.display(
            simuations_path=self.simulations_path,
            l=fall_of_wicket,
            card_type="fow",
            innings="first_innings",
        )

        target = first_innings.total_runs + 1

        second_innings = Innings(
            batting_team=self.opposition_team,
            bowling_team=self.home_team,
            target=target,
        )
        over_by_over, batting_card, bowling_card, fall_of_wicket = second_innings.play()
        Match.display(
            simuations_path=self.simulations_path,
            l=over_by_over,
            card_type="over_by_over",
            innings="second_innings",
        )
        Match.display_batting_card(
            simuations_path=self.simulations_path,
            batting_card=batting_card,
            innings="second_innings",
        )
        Match.display_bowling_card(
            simuations_path=self.simulations_path,
            bowling_card=bowling_card,
            innings="second_innings",
        )
        Match.display(
            simuations_path=self.simulations_path,
            l=fall_of_wicket,
            card_type="fow",
            innings="second_innings",
        )


if __name__ == "__main__":
    match = Match(home_team="team1", opposition_team="team2")
    match.play()
