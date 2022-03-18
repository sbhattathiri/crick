import random

import pandas as pd



class Innings:

    def __init__(self, batting_team, target=None, max_overs=20):
        self.batting_team = batting_team
        self.bowling_team = 'team2' if self.batting_team == 'team1' else 'team1'
        self.target = target
        self.max_overs = max_overs
        self.total_runs = 0
        self.total_wickets = 0
        self.overs_completed = 0
        self.batting_card = {}
        self.batters = self.get_batters(self.batting_team)['name'].to_list()
        self.bowling_card = {}
        self.opposition_bowlers = self.get_bowlers(self.bowling_team)['name'].to_list()

    
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
        team_data = f'data/{team}.csv'
        team_df = pd.read_csv(team_data)

        # sanitize
        columns = {col: col.strip() for col in team_df.columns} 
        team_df = team_df.rename(columns=columns)

        # filter for role = [bowler, all-rounder]
        team_df['name'] = team_df['first_name'] + ' ' + team_df['last_name']
        team_df = team_df[['name', 'bat_avg', 'strike_rate', 'highscore']]
        
        return team_df
        

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
       


    def over(self, mode, runs_remaining, wickets_remaining):
    
        # define possibilities for a ball bowled      
        possibilities = ['0', '1', '2', '3', '4', '6', 'W']

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

        for _ in range(6):
            event = random.choices(possibilities, weights=weights, k=1)[0]
            balls_bowled += 1
            if event == 'W':
                wickets += 1
            else:
                runs += int(event)

            # end innings if all wickets lost
            # or target achieved    
            if wickets >= wickets_remaining or runs >= runs_remaining:
                break

        return runs, wickets, balls_bowled

    
    def play(self):
        # init previous bowler so than end's change
        previous_bowler = ''

        # assign target to chase or 20*36 if first inn
        target = self.target if self.target else 720
    
        while self.overs_completed < 20 and self.total_wickets < 10 and self.total_runs <= target: 
            # choose a bowler
            while True:
                bowler = random.choice(self.opposition_bowlers)
                if bowler != previous_bowler:
                    bowler_stats = self.bowling_card.get(bowler, {})
                    if bowler_stats.get('overs', 0) < 4:
                        break
                        
            # get bowler's form
            mode = Innings.isChadOrVirgin()
            if mode == 1:
                bowlers_form = 'chad' 
            elif mode == -1:
                bowlers_form = 'virgin'
            else:
                bowlers_form = 'normal'

            # bowl the over
            runs, wickets, balls_bowled = self.over(mode, target-self.total_runs, 10-self.total_wickets)

            print(f'Over: {self.overs_completed + 1}, Bowler: {bowler}, {bowlers_form}, {runs}-{wickets}')
            
            # scoring
            self.total_runs += runs
            self.total_wickets += wickets
            self.overs_completed = self.overs_completed + 1 if balls_bowled == 6 else self.overs_completed + (balls_bowled / 10)
            
            # build bowler card
            bowler_overs = bowler_stats.get('overs', 0) + 1 if balls_bowled == 6 else bowler_stats.get('overs', 0) + (balls_bowled / 10)
            bowler_runs = bowler_stats.get('runs', 0) + runs
            bowler_wickets = bowler_stats.get('wickets', 0) + wickets
            bowler_stats['overs'] = bowler_overs
            bowler_stats['runs'] = bowler_runs
            bowler_stats['wickets'] = bowler_wickets

            self.bowling_card[bowler] = bowler_stats

            # set current bowler as previous
            previous_bowler = bowler

    
    def display_bowling_card(self):
        for bowler in self.bowling_card:    
            print(f'{bowler} \t {self.bowling_card[bowler]["overs"]} - {self.bowling_card[bowler]["runs"]} - {self.bowling_card[bowler]["wickets"]}')


            
if __name__ == '__main__':
    innings = Innings('team1')
    innings.play()
    innings.display_bowling_card()
