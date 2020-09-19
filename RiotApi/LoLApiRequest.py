import os
from riotwatcher import LolWatcher, ApiError


# https://developer.riotgames.com/docs/lol

class ApiRequest:
    def __init__(self, nick: str):
        self.lol = LolWatcher(os.getenv("RIOT_API"))
        self.region = "EUW1"
        self.username = nick

    def get_summoner_data(self) -> dict:
        summoner_data = self.lol.summoner.by_name(self.region, self.username)
        return summoner_data

    def get_league(self) -> dict:
        return self.lol.league.by_summoner(self.region, self.get_summoner_data()['id'])

    def get_best_champions(self) -> dict:
        return self.lol.champion_mastery.by_summoner(self.region, self.get_summoner_data()['id'])[:3]

    def get_match_list(self, end_index: int = 5) -> dict:
        return self.lol.match.matchlist_by_account(self.region, self.get_summoner_data()['accountId'],
                                                   end_index=end_index)['matches']

    def get_match_detail(self, match_id: int) -> dict:
        return self.lol.match.by_id(self.region, match_id)
