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
        self.batting_card = {}
        self.batters = self.get_batters(self.team)['name'].to_list()
    
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
    
        # batters
        striker =  self.batters[0]
        non_striker = self.batters[1]
        latest_batting_position_in_crease = 1 #incase of wickets

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

        striker_runs = 0
        striker_balls = 0
        non_striker_runs = 0
        non_striker_balls = 0

        for _ in range(6):
            striker_stats = {}
            non_striker_stats = {}
            event = random.choices(possibilities, weights=weights, k=1)[0]
            balls_bowled += 1
            if event == 'W':
                wickets += 1
                striker_stats['runs'] = striker_stats.get('runs', 0)
                striker_stats['balls'] = striker_stats.get('balls', 0) + 1
                # batting_card[striker] = striker_stats
            else:
                runs += int(event)

            # end innings if all wickets lost
            # or target achieved    
            if wickets >= wickets_remaining or runs >= runs_remaining:
                print(f'Innings over')
                break

        print(f'{runs}, {wickets}, {balls_bowled/10}')
        return runs, wickets, balls_bowled

    
    def play(self):
        # assign target to chase or 20*36 if first inn
        target = self.target if self.target else 720
        
        total_runs = 0
        total_wickets = 0
        overs_completed = 0

        bowling_card = {}
        opposition_bowlers_df = self.get_bowlers(self.opposition)
        opposition_bowlers = opposition_bowlers_df['name'].to_list()

        previous_bowler = ''
        while overs_completed < 20 and total_wickets < 10 and total_runs <= target: 
            # choose a bowler
            while True:
                bowler = random.choice(opposition_bowlers)
                if bowler != previous_bowler:
                    bowler_stats = bowling_card.get(bowler, {})
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
            runs, wickets, balls_bowled = self.over(mode, target-total_runs, 10-total_wickets)

            print(f'Over: {overs_completed + 1}, Bowler: {bowler}, {bowlers_form}, {runs}-{wickets}')
            
            # scoring
            total_runs += runs
            total_wickets += wickets
            overs_completed = overs_completed + 1 if balls_bowled == 6 else overs_completed + (balls_bowled / 10)
            
            # build bowler card
            bowler_overs = bowler_stats.get('overs', 0) + 1 if balls_bowled == 6 else bowler_stats.get('overs', 0) + (balls_bowled / 10)
            bowler_runs = bowler_stats.get('runs', 0) + runs
            bowler_wickets = bowler_stats.get('wickets', 0) + wickets
            bowler_stats['overs'] = bowler_overs
            bowler_stats['runs'] = bowler_runs
            bowler_stats['wickets'] = bowler_wickets

            bowling_card[bowler] = bowler_stats

            previous_bowler = bowler
        
        return bowling_card

    
    def display_bowling_card(self, bowling_card):
        for bowler in bowling_card:    
            print(f'{bowler} {bowling_card[bowler]["overs"]} - {bowling_card[bowler]["runs"]} - {bowling_card[bowler]["wickets"]}')


            
if __name__ == '__main__':
    innings = Innings('team1')
    bowling_card = innings.play()
    innings.display_bowling_card(bowling_card=bowling_card)
