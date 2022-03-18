import pandas as pd


class Innings:

    

    def __init__(self, team, target=None, overs=20):
        self.team = team
        self.opposition = 'team2' if team == 'team1' else 'team1'
        self.target = target
        self.overs = overs
        self.score = 0
        self.wickets = 0
        self.opposition_bowlers = get_bowlers(self.opposition)

    def get_bowlers(self, team):
        team_data = f'data/{team}.csv'
        team_df = pd.read_csv(team_data)
       


    def over(self, bowler):
        ball_by_ball = []





if __name__ == '__main__':
    pass