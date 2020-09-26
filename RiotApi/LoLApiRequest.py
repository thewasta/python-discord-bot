import os
from pantheon import pantheon
from riotwatcher import LolWatcher, ApiError
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()

server = {
    "eun": "EUN1",
    "euw": "EUW1",
    "na": "NA1",
    "lan": "LA1",
    "la2": "LA2"
}

headers = {"X-Riot-Token": "RGAPI-e27b7c49-af4e-45e4-aff9-0a17d69639ec"}


# https://developer.riotgames.com/docs/lol
class ApiRequest:
    def __init__(self, nick: str):
        self.lol = LolWatcher(os.getenv("RIOT_API"))
        self.region = "EUW1"
        self.username = nick

    def get_summoner_data(self):
        return self.lol.summoner.by_name(self.region, self.username)

    def get_league(self):
        return self.lol.league.by_summoner(self.region, self.get_summoner_data()['id'])

    def get_best_champions(self):
        return self.lol.champion_mastery.by_summoner(self.region, self.get_summoner_data()['id'])[:3]

    def get_match_list(self, end_index: int = 5, champion=None, queue=None) -> dict:

        return self.lol.match.matchlist_by_account(self.region, self.get_summoner_data()['accountId'],
                                                   end_index=end_index, champion=champion, queue={"420", "440"})[
            'matches']

    def get_match_detail(self, match_id: int):
        return self.lol.match.by_id(self.region, match_id)

    def is_in_game(self):
        try:
            self.lol.spectator.by_summoner(region=self.region,
                                           encrypted_summoner_id=self.get_summoner_data()['id'])
            return '<:victory:755862932541407302>'
        except ApiError:
            return '<:defeat:755862932461584415>'
