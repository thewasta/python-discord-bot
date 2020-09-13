from riotwatcher import LolWatcher, ApiError


class LolApi:
    def __init__(self, nick):
        self.lol = LolWatcher("RIOT_API")
        self.region = "EUW1"
        self.username = nick

    async def get_summoner_data(self):
        summoner_data = await self.lol.summoner.by_name(self.region, self.username)
        # self.lol.match.matchlist_by_account(region=self.region,encrypted_account_id=summoner_data['id'],queue=)
        return summoner_data


api = LolApi('tms thewasta')
api.get_summoner_data()
