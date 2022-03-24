from curses import window
import tkinter as tk


class RegisterTeam:
    def __init__(self):
        self.team_name = ""
        self.team_xi = []

        # gui
        self.window = tk.Tk()
        self.window.title("Create Team")
        self.window.geometry("800x600")
        self.window.configure(background="grey")

        self.frame = tk.Frame(master=self.window, relief=tk.RAISED, bg="grey", borderwidth=1)
        self.frame.pack()

        self.team_name_label = tk.Label(master=self.frame, text="Team Name", font="JetBrainsMono", bg="grey")
        self.team_name_label.grid(row=0, column=0)
        self.team_name_var = tk.StringVar()
        self.team_name_entry = tk.Entry(master=self.frame, textvariable=self.team_name_var, fg="black", bg="white")
        self.team_name_entry.grid(row=0, column=1)

        # space-ing
        tk.Label(master=self.frame, text="", bg="grey").grid(row=1, column=0)
        tk.Label(master=self.frame, text="", bg="grey").grid(row=2, column=0)

        # header
        tk.Label(master=self.frame, text="Position", font="JetBrainsMono", bg="grey").grid(row=3, column=0)
        tk.Label(master=self.frame, text="First Name", font="JetBrainsMono", bg="grey").grid(row=3, column=1)
        tk.Label(master=self.frame, text="Last Name", font="JetBrainsMono", bg="grey").grid(row=3, column=2)
        tk.Label(master=self.frame, text="Role", font="JetBrainsMono", bg="grey").grid(row=3, column=3)

        self.player_first_name_entries = []
        self.player_last_name_entries = []
        self.player_role_entries = []
        player_roles = ["Batter", "All-rounder", "Bowler"]
        for bat_pos in range(4, 15):
            player_pos_label = tk.Label(master=self.frame, text=f"Player {bat_pos-3}", bg="grey")

            player_pos_label.grid(row=bat_pos, column=0)
            player_first_name_entry = tk.Entry(master=self.frame, fg="black", bg="white")
            self.player_first_name_entries.append(player_first_name_entry)
            player_first_name_entry.grid(row=bat_pos, column=1)

            player_last_name_entry = tk.Entry(master=self.frame, fg="black", bg="white")
            self.player_last_name_entries.append(player_last_name_entry)
            player_last_name_entry.grid(row=bat_pos, column=2)

            role = tk.StringVar(self.frame)
            player_role_entry = tk.OptionMenu(self.frame, role, *player_roles)
            self.player_role_entries.append(role)
            player_role_entry.grid(row=bat_pos, column=3)

        # space-ing
        tk.Label(master=self.frame, text="", bg="grey").grid(row=15, column=0)
        tk.Label(master=self.frame, text="", bg="grey").grid(row=16, column=0)

        self.register_button = tk.Button(master=self.frame, text="Register", font="JetBrainsMono")
        self.register_button.bind("<Button-1>", self.register)
        self.register_button.grid(row=17, column=0)

        self.window.mainloop()

    # click-handler
    def register(self, event):
        self.team_name = self.team_name_entry.get()

        for f_n, l_n, role in zip(
            self.player_first_name_entries, self.player_last_name_entries, self.player_role_entries
        ):
            print(f"{f_n.get()} {l_n.get()} {role.get()}")


if __name__ == "__main__":
    RegisterTeam()
