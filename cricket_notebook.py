import marimo

__generated_with = "0.15.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import random

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

    POSITIVE_BATTING_COMMENTS = [
        "Batters maintaining very good run rate.\n",
        "Amazing striking from the batters.\n",
        "Bowlers taking a serious thumping.\n"
    ]

    NEUTRAL_BATTING_COMMENTS = [
        "Batters playing it safe.\n"
    ]

    NEGATIVE_BATTING_COMMENTS = [
        "Batters struggling.\n",
        "Batters living out their luck.\n",
    ]

    POSITIVE_BOWLING_COMMENTS = [
        "Last over was fire.\n",
        "Terrific bowling.\n",
    ]

    NEUTRAL_BOWLING_COMMENTS = [
        "A rather uneventful over.\n"
    ]

    NEGATIVE_BOWLING_COMMENTS = [
        "Poor bowling there.\n",
        "Bowlers struggling to hit the right areas.\n",
    ]


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

            # for generating commentary
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
                    f"captain running out of options, bringing in {part_timer}"
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
            commentary_line = ""
            runs_in_previous_over = self.last_over_stats["runs"]
            wickets_in_previous_over = self.last_over_stats["wickets"]

            striker_near_50 = 0 < 50 - self.batting_scorecard.get(self.batters[self.get_striker()])["runs"] < 10
            partner_near_50 = 0 < 50 - self.batting_scorecard.get(self.batters[self.get_partner()])["runs"] < 10
            striker_near_100 = 0 < 100 - self.batting_scorecard.get(self.batters[self.get_striker()])["runs"]  < 10
            partner_near_100 = 0 < 100 - self.batting_scorecard.get(self.batters[self.get_partner()])["runs"]  < 10
            if striker_near_50 and partner_near_50:
                commentary_line += "Both batters nearing fifty \n"
            elif striker_near_100 and partner_near_100:
                commentary_line += "Both batters nearing hundred \n"
            elif striker_near_100:
                commentary_line += f"{self.batters[self.get_striker()]} nearing hundred \n"
            elif partner_near_100:
                commentary_line += f"{self.batters[self.get_partner()]} nearing hundred \n"
            elif striker_near_50:
                commentary_line += f"{self.batters[self.get_striker()]} nearing fifty \n"
            elif partner_near_50:
                commentary_line += f"{self.batters[self.get_partner()]} nearing fifty \n"
        
            if runs_in_previous_over >= 12:
                commentary_line += " " + random.choice(POSITIVE_BATTING_COMMENTS)
                if wickets_in_previous_over == 0:
                    commentary_line += " " + random.choice(NEGATIVE_BOWLING_COMMENTS)
            elif 6 < runs_in_previous_over < 12:
                commentary_line += " " + random.choice(NEUTRAL_BATTING_COMMENTS)
                if wickets_in_previous_over >= 3:
                    commentary_line += " " + random.choice(POSITIVE_BOWLING_COMMENTS)
            else:
                commentary_line += " " + random.choice(NEGATIVE_BATTING_COMMENTS)
                if wickets_in_previous_over >= 1:
                    commentary_line += " " + random.choice(POSITIVE_BOWLING_COMMENTS)
                else:
                    commentary_line += " " + random.choice(NEUTRAL_BOWLING_COMMENTS)

            if self.overs_remaining == 2:
                commentary_line += f"{self.overs_remaining} overs remain - can they get to {self.total_runs + 30}? \n"
            elif self.overs_remaining == 1:
                commentary_line += f"last over of the innings - can they finish it off in style? \n"

            print("")
            print(commentary_line)
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

        # def display_batting_scorecard(self):
        #     formatted_scorecard = [
        #         {
        #             "player": batter,
        #             "dismissal": (
        #                 self.batting_scorecard.get(batter)["dismissal"]
        #                 if self.batting_scorecard.get(batter)["dismissed"]
        #                 else "NOT OUT"
        #                 if self.batting_scorecard.get(batter)["balls"]
        #                 else ""
        #             ),
        #             "runs": self.batting_scorecard.get(batter)["runs"]
        #             if self.batting_scorecard.get(batter)["balls"]
        #             else "",
        #             "balls": self.batting_scorecard.get(batter)["balls"]
        #             if self.batting_scorecard.get(batter)["balls"]
        #             else "",
        #             "4s": self.batting_scorecard.get(batter)["fours"]
        #             if self.batting_scorecard.get(batter)["balls"]
        #             else "",
        #             "6s": self.batting_scorecard.get(batter)["sixes"]
        #             if self.batting_scorecard.get(batter)["balls"]
        #             else "",
        #         }
        #         for batter in self.batters
        #     ] + [
        #         {
        #             "player": "EXTRAS",
        #             "dismissal": "",
        #             "runs": self.extras,
        #             "balls": "",
        #             "4s": "",
        #             "6s": "",
        #         },
        #         {
        #             "player": "TOTAL",
        #             "dismissal": "",
        #             "runs": f"{self.total_runs}/{self.total_wickets}",
        #             "balls": "",
        #             "4s": "",
        #             "6s": "",
        #         },
        #     ]
        #     return mo.ui.table(data=formatted_scorecard, pagination=True, page_size=15)

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
                for bowler in self.bowlers if self.bowling_scorecard.get(bowler)["balls"]
            ]
            return mo.ui.table(data=formatted_scorecard, pagination=True)

        # def display_bowling_scorecard(self):
        #     formatted_scorecard = [
        #         {
        #             "player": bowler,
        #             "overs": f"{self.bowling_scorecard.get(bowler)['balls'] // 6}.{self.bowling_scorecard.get(bowler)['balls'] % 6}"
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "balls": f"{self.bowling_scorecard.get(bowler)['balls']}"
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "dots": self.bowling_scorecard.get(bowler)["dots"]
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "runs": self.bowling_scorecard.get(bowler)["runs"]
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "wickets": self.bowling_scorecard.get(bowler)["wickets"]
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "wd": self.bowling_scorecard.get(bowler)["wides"]
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #             "nb": self.bowling_scorecard.get(bowler)["no-balls"]
        #             if self.bowling_scorecard.get(bowler)["balls"]
        #             else "",
        #         }
        #         for bowler in self.bowlers 
        #     ]
        #     return mo.ui.table(data=formatted_scorecard, pagination=True)


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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
