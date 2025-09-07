import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import json
    import random
    import marimo as mo

    from openai import OpenAI
    return OpenAI, json, mo, random


@app.cell
def _(OpenAI):
    client = OpenAI(
        base_url="http://localhost:12434/engines/v1",
        api_key="sk-no-key-required",
    )
    return (client,)


@app.cell
def _(client):
    def generate_commentary(match_stats):
        try:
            completion = client.chat.completions.create(
                model="ai/gemma3",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": """
                                You are a cricket commentary generator.

                                You will be given a match stats dictionary with the following keys:
                            
                                batting_team (str): name of the team that is batting
                                fielding_team (str): name of the team that is fielding
                                batter (str): Current batter’s name
                                partner (str): Non-striker’s name
                                batter_score (int): Runs scored by current batter
                                partner_score (int): Runs scored by partner
                                team_score (int): Total team runs
                                wickets (int): Total wickets down
                                overs_remaining (int): Overs left in the innings
                                runs_prev_over (int): Runs scored in the previous over
                                wickets_prev_over (int): Wickets fallen in the previous over

                                Your task:
                                Generate exactly 3 lines of natural-sounding cricket commentary.
                                Commentary should be dynamic, engaging, and contextual, not robotic.
                                Blend in match situation insights, e.g., runs/wickets in last over, strike rotation, pressure, or momentum.
                                Each line should add a new perspective.
                                Use a tone similar to live commentators—lively, descriptive, slightly dramatic if relevant.

                                In cricket scoring 50 runs, 100 runs etc are personal milestones.Likewise taking 5 wickets is a milestone.
                                If the bowler is nearing 5 wickets or batsman is nearing 50 or 100 runs make sure to include that in the                               comment 

                                NOTE: GIVE JUST THE COMMENTARY LINES. AVOID WRITING 
                                "Here's a commentary generated for the provided match stats:" etc.
                                """,
                            }
                        ],
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": match_stats
                            },
                        ],
                    },
                ],
            )

            return completion.choices[0].message.content
        except:
            return "No comments!!!"
    return (generate_commentary,)


@app.cell
def _():
    EVENTS = [0, 1, 2, 3, 4, 5, 6, "W", "WD", "NB"]
    WEIGHTS = [25, 25, 12, 8, 15, 1, 9, 2, 1, 2]

    DISMISSAL_TEMPLATES = {
        "b": "b {bowler}",
        "lbw": "lbw b {bowler}",
        "c": "c {fielder1} b {bowler}",
        "c&b": "c&b {bowler}",
        "st": "st {keeper} b {bowler}",
        "run out": "run out [{fielder1}/{fielder2}]",
    }
    DISMISSAL_MODE_WEIGHTS = [20, 25, 35, 8, 6, 6]
    return DISMISSAL_MODE_WEIGHTS, DISMISSAL_TEMPLATES, EVENTS, WEIGHTS


@app.cell
def _(
    DISMISSAL_MODE_WEIGHTS,
    DISMISSAL_TEMPLATES,
    EVENTS,
    WEIGHTS,
    generate_commentary,
    json,
    mo,
    random,
):

    class Innings:
        def __init__(self, batters, bowlers, fielders, keeper, max_overs):
            self.max_overs = max_overs
            self.max_over_per_bowler = {
                20: 4,
                50: 10,
            }.get(max_overs)

            self.batters = batters
            self.bowlers = bowlers
            self.fielders = fielders
            self.keeper = keeper

            self.total_runs = 0
            self.extras = 0
            self.total_wickets = 0
            self.all_out = False

            self.striker = 0
            self.partner = 1
            self.next_batter = 2

            self.batting_scorecard = {
                batter: {
                    "dismissed": False,
                    "dismissal": "",
                    "runs": 0,
                    "balls": 0,
                    "fours": 0,
                    "sixes": 0,
                }
                for batter in batters
            }
            self.bowling_scorecard = {
                bowler: {
                    "balls": 0,
                    "overs": 0,
                    "dots": 0,
                    "runs": 0,
                    "wickets": 0,
                    "wides": 0,
                    "no-balls": 0,
                }
                for bowler in bowlers
            }

            self.event_comment = ""
            self.overs_remaining = max_overs
            self.last_over_stats = {
                "runs": 0,
                "wickets": 0,
            }

        def set_striker(self, striker=0):
            self.striker = striker

        def get_striker(self):
            return self.striker

        def set_partner(self, partner=1):
            self.partner = partner

        def get_partner(self, partner=1):
            return self.partner

        def swap_striker(self):
            self.striker, self.partner = self.partner, self.striker

        def pick_bowler(self, previous_bowler=""):
            options = [
                bowler
                for bowler in self.bowling_scorecard
                if self.bowling_scorecard[bowler]["overs"]
                < self.max_over_per_bowler
                and bowler != previous_bowler
            ]

            if not options:
                part_timer = random.choice(self.fielders)
                options.append(part_timer)
                self.bowlers.append(part_timer)
                self.bowling_scorecard[part_timer] = {
                    "balls": 0,
                    "overs": 0,
                    "dots": 0,
                    "runs": 0,
                    "wickets": 0,
                    "wides": 0,
                    "no-balls": 0,
                }
                print(
                    f"Captain running out of options, bringing in {part_timer}"
                )

            return random.choice(options)

        def get_dismissal(self, bowler):
            fielders = (
                self.fielders
                + [fielder for fielder in self.bowlers if fielder != bowler]
                + [self.keeper]
            )
            fielder1, fielder2 = random.sample(fielders, 2)
            dismissal = random.choices(
                list(DISMISSAL_TEMPLATES.keys()), weights=DISMISSAL_MODE_WEIGHTS
            )[0]
            return DISMISSAL_TEMPLATES.get(dismissal).format(
                bowler=bowler,
                fielder1=fielder1,
                fielder2=fielder2,
                keeper=self.keeper,
            )

    
        def commentary(self):
            match_stats = {
                "batting_team": "India XI",
                "fielding_team": "England Lions",
                "batter": self.batters[self.get_striker()],
                "partner": self.batters[self.get_partner()],
                "batter_score": self.batting_scorecard.get(self.batters[self.get_striker()])["runs"] ,
                "partner_score": self.batting_scorecard.get(self.batters[self.get_partner()])["runs"] ,
                "team_score": self.total_runs,
                "wickets": self.total_wickets,
                "overs_remaining": self.overs_remaining,
                "runs_prev_over": self.last_over_stats["runs"],
                "wickets_prev_over": self.last_over_stats["wickets"]
            }

            comment = generate_commentary(json.dumps(match_stats))

            print("")
            print(comment)
            print("")


        def event(self):
            return random.choices(EVENTS, weights=WEIGHTS)[0]

        def display_batting_scorecard(self):
            formatted_scorecard = [
                {
                    "player": batter,
                    "dismissal": (
                        self.batting_scorecard.get(batter)["dismissal"]
                        if self.batting_scorecard.get(batter)["dismissed"]
                        else "NOT OUT"
                    ),
                    "runs": self.batting_scorecard.get(batter)["runs"],
                    "balls": self.batting_scorecard.get(batter)["balls"],
                    "4s": self.batting_scorecard.get(batter)["fours"],   
                    "6s": self.batting_scorecard.get(batter)["sixes"],

                }
                for batter in self.batters if self.batting_scorecard.get(batter)["balls"]
            ] + [
                {
                    "player": "EXTRAS",
                    "dismissal": "",
                    "runs": self.extras,
                    "balls": "",
                    "4s": "",
                    "6s": "",
                },
                {
                    "player": "TOTAL",
                    "dismissal": "",
                    "runs": f"{self.total_runs}/{self.total_wickets}",
                    "balls": "",
                    "4s": "",
                    "6s": "",
                },
            ]
            return mo.ui.table(data=formatted_scorecard, pagination=True, page_size=15)


        def display_bowling_scorecard(self):
            formatted_scorecard = [
                {
                    "player": bowler,
                    "overs": f"{self.bowling_scorecard.get(bowler)['balls'] // 6}.{self.bowling_scorecard.get(bowler)['balls'] % 6}",
                    "dots": self.bowling_scorecard.get(bowler)["dots"],
                    "runs": self.bowling_scorecard.get(bowler)["runs"],
                    "wickets": self.bowling_scorecard.get(bowler)["wickets"],
                    "wd": self.bowling_scorecard.get(bowler)["wides"],
                    "nb": self.bowling_scorecard.get(bowler)["no-balls"],
                }
                for bowler in self.bowlers if self.bowling_scorecard.get(bowler).get("balls")
            ]
            return mo.ui.table(data=formatted_scorecard, pagination=True)


        def over(self, over_index, previous_bowler):
            current_bowler = self.pick_bowler(previous_bowler)
            runs = 0
            wickets = 0
            ball_index = 1
            while ball_index < 7:
                striker = self.batters[self.get_striker()]
                event = self.event()
                if event == "W":
                    self.batting_scorecard.get(striker)["dismissed"] = True
                    self.batting_scorecard.get(striker)["dismissal"] = (
                        self.get_dismissal(current_bowler)
                    )
                    self.batting_scorecard.get(striker)["balls"] += 1

                    self.bowling_scorecard.get(current_bowler)["balls"] += 1
                    self.bowling_scorecard.get(current_bowler)["dots"] += 1
                    self.bowling_scorecard.get(current_bowler)["wickets"] += 1

                    wickets += 1
                    self.total_wickets += 1

                    self.set_striker(self.next_batter)
                    self.next_batter += 1

                    self.event_comment = "OUT"

                    if self.total_wickets == 10:
                        self.all_out = True
                        break
                elif event in ["WD", "NB"]:
                    self.bowling_scorecard.get(current_bowler)[
                        "wides" if event == "WD" else "no-balls"
                    ] += 1

                    runs += 1
                    self.total_runs += 1
                    self.extras += 1

                    self.event_comment = event
                else:
                    self.batting_scorecard.get(striker)["runs"] += event
                    self.batting_scorecard.get(striker)["balls"] += 1

                    self.bowling_scorecard.get(current_bowler)["balls"] += 1
                    self.bowling_scorecard.get(current_bowler)["runs"] += event

                    runs += event
                    self.total_runs += event

                    if event == 0:
                        self.bowling_scorecard.get(current_bowler)["dots"] += 1

                    if event in [1, 3, 5]:
                        self.swap_striker()

                    if event == 4:
                        self.batting_scorecard.get(striker)["fours"] += 1

                    if event == 6:
                        self.batting_scorecard.get(striker)["sixes"] += 1

                    self.event_comment = f"{event} RUNS"



                print(
                    f"{over_index}.{ball_index} "
                    f"{current_bowler} to {striker} {self.event_comment}, "
                    f"TEAM SCORE: {self.total_runs}/{self.total_wickets}"
                )
                if event not in ["WD", "NB"]:
                    ball_index += 1 


            return current_bowler, runs, wickets



        def innings(self):
            over_index = 0
            self.set_striker(0)
            self.set_partner(1)
            previous_bowler = ""
            while over_index < self.max_overs:
                if self.all_out:
                    break

                bowler, runs, wickets = self.over(over_index, previous_bowler)
                self.last_over_stats["runs"] = runs
                self.last_over_stats["wickets"] = wickets

                self.bowling_scorecard.get(bowler)["overs"] += 1
                previous_bowler = bowler

                over_index += 1
                self.overs_remaining -= 1

                self.swap_striker()

                self.commentary()
    return (Innings,)


@app.cell
def _():
    batters = [
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
    return (batters,)


@app.cell
def _():
    bowlers = [
        "Jofra Archer",
        "Mark Wood",
        "Jamie Overton",
        "Adil Rashid",
        "Joe Root",
    ]
    return (bowlers,)


@app.cell
def _():
    fielders = [
        "Ben Duckett",
        "Harry Brook",
        "Jacob Bethell",
        "Will Jacks",
        "Zach Crawley",
    ]
    return (fielders,)


@app.cell
def _():
    keeper = "Jos Buttler"
    return (keeper,)


@app.cell
def _(Innings, batters, bowlers, fielders, keeper):
    inn = Innings(batters, bowlers, fielders, keeper, max_overs=20)
    inn.innings()
    return (inn,)


@app.cell
def _(inn):
    inn.display_batting_scorecard()
    return


@app.cell
def _(inn):
    inn.display_bowling_scorecard()
    return


if __name__ == "__main__":
    app.run()
