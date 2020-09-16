import os
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv

load_dotenv()


# https://developer.riotgames.com/docs/lol

class ApiRequest:
    def __init__(self, nick):
        self.lol = LolWatcher(os.getenv("RIOT_API"))
        self.region = "EUW1"
        self.username = nick

    def get_summoner_data(self):
        summoner_data = self.lol.summoner.by_name(self.region, self.username)
        return summoner_data

    def get_league(self):
        return self.lol.league.by_summoner(self.region, self.get_summoner_data()['id'])

    def get_summoner_league_icon(self):
        return self.lol.data_dragon.profile_icons(version="10.18.1", locale="")

    def get_best_champions(self):
        return self.lol.champion_mastery.by_summoner(self.region, self.get_summoner_data()['id'])[:5]

    def get_match_list(self, end_index=5):
        return self.lol.match.matchlist_by_account(self.region, self.get_summoner_data()['accountId'],
                                                   end_index=int(end_index))['matches']
