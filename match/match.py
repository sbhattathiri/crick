import random

import pandas as pd



class Innings:

    def __init__(self, team, target=None, overs=20):
        self.team = team
        self.opposition = 'team2' if team == 'team1' else 'team1'
        self.target = target
        self.overs = overs
        self.score = 0
        self.wickets = 0
        


    def get_bowlers(self, team):
        
        # read data from csv
        team_data = f'data/{team}.csv'
        team_df = pd.read_csv(team_data)

        # sanitize
        columns = {col: col.strip() for col in team_df.columns} 
        team_df = team_df.rename(columns=columns)

        # filter for role = [bowler, all-rounder]
        bowlers_df = team_df[(team_df['role'] == 'bowler') | (team_df['role'] == 'all-rounder')]
        bowlers_df['name'] = bowlers_df['first_name'] + ' ' + bowlers_df['last_name']
        bowlers_df = bowlers_df[['name', 'bowl_avg', 'economy', 'best_figures']]
        
        return bowlers_df
       


    def over(self, bowler_stats, runs_remaining, wickets_remaining):
        possibilities = ['0', '1', '2', '3', '4', '6', 'W']
        ball_by_ball = []
        runs = 0
        wickets = 0
        for _ in range(6):
            event = random.choice(possibilities)
            if event == 'W':
                wickets += 1
            else:
                runs += int(event)
            if wickets >= wickets_remaining or runs >= runs_remaining:
                print(f'Match over')
                break
        
        return runs, wickets

    
    def start(self):

        target = self.target if self.target else 720
        
        total_runs = 0
        total_wickets = 0
        overs_completed = 0

        bowling_card = {}
        opposition_bowlers_df = self.get_bowlers(self.opposition)
        opposition_bowlers = opposition_bowlers_df['name'].to_list()

        previous_bowler = ''
        while overs_completed < 20 and total_wickets < 10 and total_runs <= target:
  
            while True:
                bowler = random.choice(opposition_bowlers)
                if bowler != previous_bowler:
                    bowler_stats = bowling_card.get(bowler, {})
                    if bowler_stats.get('overs', 0) < 4:
                        break
                        
            
            # print(f'chosen {bowler}, previous {previous_bowler}, {bowler==previous_bowler}')
            # print(f'Over: {overs_completed + 1}, Bowler: {bowler}')
            
            runs, wickets = self.over(opposition_bowlers_df.loc[opposition_bowlers_df['name']==bowler], target-total_runs, 10-total_wickets)
            
            total_runs += runs
            total_wickets += wickets
            overs_completed += 1
            
            bowler_overs = bowler_stats.get('overs', 0) + 1
            bowler_runs = bowler_stats.get('runs', 0) + runs
            bowler_wickets = bowler_stats.get('wickets', 0) + wickets
            bowler_stats['overs'] = bowler_overs
            bowler_stats['runs'] = bowler_runs
            bowler_stats['wickets'] = bowler_wickets

            bowling_card[bowler] = bowler_stats

            previous_bowler = bowler

        print(bowling_card)

            







if __name__ == '__main__':
    innings = Innings('team1')
    innings.start()