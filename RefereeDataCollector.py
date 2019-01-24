import time
from operator import methodcaller

import requests
from bs4 import BeautifulSoup

class GameFinder():
    """
    This class is able to find game data for a specific research..
    """
    def __init__(self, name="", surname=""):
        now = int(time.time()) * 1000  # FIP needs timestamp in ms (13 digits)
        url = "http://www.fip.it/ajax-risultati-cerca-gara-risultati.aspx?" + str(now)
        dataRequest = {'Order': 'data', 'Ds': '', 'Dd': '', 'Da': '', 'PROV': '', 'REG': '', 'COMSearch': '',
                       'Numero': '', 'Soc': '', 'CodiceCampo': '', 'Arbitro': surname, 'NomeArbitro': name,
                       'ArbitroCodice': '', 'NomeSquadra': '', 'cercagara': 1}
        self.page = a = requests.post(url, dataRequest)
        self.soup = BeautifulSoup(self.page.text, "html.parser")

    def __str__(self):
        return str(self.soup)

    def find_all_matches(self):
        #TODO: create model for matches to persist them
        self.find_all_referees()
        self.find_all_home_teams()
        self.find_all_opponent_teams()

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


    def find_all_referees(self):
        self.find_all_game_recaps()
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
        #self.referee_terns = list(map(methodcaller("split"self.game_recap.split("\n")[1].strip()



    def find_all_home_teams(self):
        self.homeTeams = self.soup.find_all(class_="nome-squadra-1")
        self.homeTeams = self._textifyList(self.homeTeams)

    def find_all_opponent_teams(self):
        self.opponentTeams = self.soup.find_all(class_="nome-squadra-2")
        self.opponentTeams = self._textifyList(self.opponentTeams)

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




# temporary testing for this module
if __name__ == '__main__':
    a = GameFinder("Fabio", "Ferretti")

    a.find_all_matches()



    a.find_all_referees()
    game_number = 0
    print("Referees:", a.referee_terns[game_number]) # prints the referee tern for the match #0
    print("Home team:", a.homeTeams[game_number])
    print("Opponent team:", a.opponentTeams[game_number])