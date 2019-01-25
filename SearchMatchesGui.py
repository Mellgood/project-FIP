from tkinter import *

from RefereeDataCollector import GameFinder

root = Tk()
text = ""

def search(event):
    name = name_entry.get()
    surname = surname_entry.get()
    a = GameFinder(name, surname)

    result_str = ""
    for game_number in range(len(a.homeTeams)):
        result_str += "Referees:" + str(a.referee_terns[game_number]) + "\nHome team:" + a.homeTeams[game_number] + "\nOpponent team:" + str(a.opponentTeams[game_number]) + "\nDate:" + str(a.match_dates[game_number]) + "\nTime:" + str(a.match_times[game_number]) + "\n-----------------------------------------------\n"

    global textBox

    textBox.config(state=NORMAL)
    textBox.insert(END, result_str)
    textBox.config(state=DISABLED)



name_label = Label(root, text="Nome")
name_label.grid(row=0, sticky=W)

name_entry = Entry(root)
name_entry.grid(row=0, column=1, sticky=W)

surname_label = Label(root, text="Cognome")
surname_label.grid(row=1, sticky=W)

surname_entry = Entry(root)
surname_entry.grid(row=1, column=1, sticky=W)


findButton = Button(root, text="Search")
findButton.grid(row=2, column=1, sticky=E)
findButton.bind("<Button-1>", search)

textBox = Text(root, height=10, width=60)
textBox.grid(row=3, column=1, columnspan=2)

root. mainloop()