import time
from operator import methodcaller

import requests
from bs4 import BeautifulSoup

class GameFinder():
    """
    This class is able to find game data for a specific research..
    All list owned by this class have the same match at the same index
    """
    def __init__(self, name="", surname=""):
        now = int(time.time()) * 1000  # FIP needs timestamp in ms (13 digits)
        url = "http://www.fip.it/ajax-risultati-cerca-gara-risultati.aspx?" + str(now)
        dataRequest = {'Order': 'data', 'Ds': '', 'Dd': '', 'Da': '', 'PROV': '', 'REG': '', 'COMSearch': '',
                       'Numero': '', 'Soc': '', 'CodiceCampo': '', 'Arbitro': surname, 'NomeArbitro': name,
                       'ArbitroCodice': '', 'NomeSquadra': '', 'cercagara': 1}
        self.page = a = requests.post(url, dataRequest)
        self.soup = BeautifulSoup(self.page.text, "html.parser")

        # let's populate
        self.find_all_matches()
        self.find_all_game_recaps()
        self.find_all_referee_terns()
        self.find_all_home_teams()
        self.find_all_opponent_teams()
        self.find_all_datetimes()

    def __str__(self):
        return str(self.soup)

    def find_all_matches(self):
        #TODO: create model for matches to persist them?
        pass

    def find_all_game_recaps(self):
        if not hasattr(self, 'game_recap'):
            self.game_recaps = self.soup.find_all(class_="luogo-arbitri")
            self.game_recaps = self._textifyList(self.game_recaps)

            # let's purge data from useless chars
            self.game_recaps = list(map(str.strip, self.game_recaps))
            self.game_recaps = list(map(methodcaller("split", "\n"), self.game_recaps))
            temp_list = []
            for match in self.game_recaps:
                match = list(map(str.strip, match))
                temp_list.append(match)
            self.game_recaps = temp_list

        return self.game_recaps

    def find_all_datetimes(self):
        if not hasattr(self, 'match_dates'):
            self.find_all_game_recaps()  # it depends by find_all_game_recaps
            self.match_datetimes = []
            self.match_dates = []
            self.match_times = []
            for match_recap in self.game_recaps:
                self.match_datetimes.append(match_recap[1])
                self.match_dates.append(match_recap[1].split("-")[0][:-1])
                self.match_times.append(match_recap[1].split("-")[1][1:])

        return self.match_datetimes



    def find_all_referee_terns(self):
        if not hasattr(self, 'referee_terns'):
            self.find_all_game_recaps() #it depends by find_all_game_recaps
            self.referee_terns = []
            for match_recap in self.game_recaps:
                observer_index = str(match_recap[0]).rfind("[") # observer info starts here (ex: [D'Arielli F. (pe)])
                if observer_index > 0:
                    referee_tern = match_recap[0][:observer_index -3] # -3 to remove " - " at the end
                else:
                    referee_tern = match_recap[0]
                self.referee_terns.append(referee_tern.split("-"))
            temp_list = []
            for tern in self.referee_terns:
                temp_list.append(list(map(str.strip, tern)))
            self.referee_terns = temp_list
        return self.referee_terns



    def find_all_home_teams(self):
        if not hasattr(self, 'homeTeams'):
            self.homeTeams = self.soup.find_all(class_="nome-squadra-1")
            self.homeTeams = self._textifyList(self.homeTeams)
        return self.homeTeams

    def find_all_opponent_teams(self):
        if not hasattr(self, 'opponentTeams'):
            self.opponentTeams = self.soup.find_all(class_="nome-squadra-2")
            self.opponentTeams = self._textifyList(self.opponentTeams)
        return self.opponentTeams

    def _textifyList(self, team_list):
        """
        Converts a list of HTML in a list of human readable text
        :param team_list: The list containing HTML
        :return: The list purged from HTML
        """
        purged_list = []
        for t in team_list:
            purged_list.append(t.text)
        return purged_list


def my_print_test():
    a = GameFinder("Fabio", "Ferretti")

    for game_number in range(len(a.homeTeams)):
        print("Referees:", a.referee_terns[game_number])  # prints the referee tern for the match #0
        print("Home team:", a.homeTeams[game_number])
        print("Opponent team:", a.opponentTeams[game_number])
        print("Date:", a.match_dates[game_number])
        print("Time:", a.match_times[game_number])
        print("-----------------------------------------------")


# temporary testing for this module
if __name__ == '__main__':
    my_print_test()
    games = GameFinder("Fabio", "Ferretti")
    #print(games.match_datetimes)
    #print(games.find_all_game_recaps())