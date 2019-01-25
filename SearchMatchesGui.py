from tkinter import *

from RefereeDataCollector import GameFinder

root = Tk()

def search(context):
    name = name_entry.get()
    surname = surname_entry.get()
    a = GameFinder(name, surname)


    for game_number in range(len(a.homeTeams)):
        print("Referees:", a.referee_terns[game_number])  # prints the referee tern for the match #0
        print("Home team:", a.homeTeams[game_number])
        print("Opponent team:", a.opponentTeams[game_number])
        print("Date:", a.match_dates[game_number])
        print("Time:", a.match_times[game_number])
        print("-----------------------------------------------")


name_label = Label(root, text="Nome")
name_label.grid(row=0, sticky=E)

name_entry = Entry(root)
name_entry.grid(row=0, column=1)

surname_label = Label(root, text="Cognome")
surname_label.grid(row=1, sticky=E)

surname_entry = Entry(root)
surname_entry.grid(row=1, column=1)


findButton = Button(root, text="Search")
findButton.grid(row=2, columnspan=2)
findButton.bind("<Button-1>", search)

root. mainloop()