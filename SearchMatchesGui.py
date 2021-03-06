from tkinter import *

from RefereeDataCollector import GameFinder


class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


class SearchView():
    def __init__(self, master):
        self.master = master

        self.name_label = Label(root, text="Nome:", pady=10, padx=5)
        self.name_label.grid(row=0, sticky=W)

        self.name_entry = Entry(root)
        self.name_entry.grid(row=0, column=1, sticky=W, padx=5)

        self.surname_label = Label(root, text="Cognome:", padx=5)
        self.surname_label.grid(row=1, sticky=W)

        self.surname_entry = Entry(root)
        self.surname_entry.grid(row=1, column=1, sticky=W, padx=5)

        self.findButton = HoverButton(root, text="Search", activebackground='grey')
        self.findButton.grid(row=1, column=2, sticky=W)
        self.findButton.bind("<Button-1>", self.search)
        self.master.bind('<Return>', self.search)

    def search(self, event):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        a = GameFinder(name, surname)

        result_str = ""
        for game_number in range(len(a.homeTeams)):
            result_str += "Referees:" + str(a.referee_terns[game_number]) + "\nHome team:" + a.homeTeams[
                game_number] + "\nOpponent team:" + str(a.opponentTeams[game_number]) + "\nDate:" + str(
                a.match_dates[game_number]) + "\nTime:" + str(
                a.match_times[game_number]) + "\n-----------------------------------------------\n"

        self.search_text_box(result_str)

    def search_text_box(self, result_str):
        self.textBox = Text(self.master, height=10, width=80)
        self.textBox.grid(row=0, column=3, rowspan=112, columnspan=1, pady=10, padx=5)

        self.textBox.config(state=NORMAL)
        self.textBox.insert(END, result_str)
        self.textBox.config(state=DISABLED)


if __name__ == '__main__':
    root = Tk()
    root.resizable(False, False)
    root.geometry("940x600")
    root.title("My Referees Observer")
    a = SearchView(root)
    root.mainloop()
