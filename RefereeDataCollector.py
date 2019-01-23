import time

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

    def __str__(self):
        return str(BeautifulSoup(self.page.text, "html.parser"))#.text


# temporary testing for this module
if __name__ == '__main__':
    a = GameFinder("", "")
    print(a)
