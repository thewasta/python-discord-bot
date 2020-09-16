from RiotApi.LoLApiRequest import ApiRequest
import json
from utils.Emojis import get_tier_rank_emoji_id, get_mastery_emoji_id, get_champion_emoji_id


def get_profile_details_for_embed(username):
    api = ApiRequest(username)
    champions_list = api.get_best_champions()
    best_champs_info = []
    for champions in champions_list:
        best_champs_info.append({
            "id": champions['championId'],
            "level": champions['championLevel'],
            "points": champions['championPoints'],
        })
    embed_message = []
    with open('./source/data/es_ES/champion.json') as json_file:
        for name, info in json.load(json_file)['data'].items():
            for best_champ in best_champs_info:
                if info['key'] == str(best_champ['id']):
                    embed_message.append({
                        "name": name,
                        "level": best_champ['level'],
                        "points": best_champ['points']
                    })
    return get_text_player(embed_message)


def get_text_player(data_champions):
    final_text = ""
    for champion in data_champions:
        if champion['points'] >= 1000:
            champion['points'] = int(str(champion['points'])[:3])
        final_text += "{}{} - {}K {} \n".format(get_champion_emoji_id(champion['name']), champion['name'],
                                                str(champion['points'])[:3],
                                                get_mastery_emoji_id(champion['level']),
                                                champion['level']
                                                )
    return final_text


def get_player_queue_details_for_embed(user_name):
    # SoloQ: EMOJITIER TIERRANK TIERLP PERCENTWINS TOTALGAMES \n
    # FlexQ: EMOJITIER TIERRANK TIERLP PERCENTWINS TOTALGAMES \n
    player_info_solo = find_solo_tier(player_elo(user_name))
    player_info_flex = find_flex_tier(player_elo(user_name))
    wins_percent_solo = round(percent_wins(player_info_solo['wins'], player_info_solo['losses']), 2)
    wins_percent_flex = round(percent_wins(player_info_flex['wins'], player_info_flex['losses']), 2)
    total_games_solo = player_info_solo['wins'] + player_info_solo['losses']
    total_games_flex = player_info_flex['wins'] + player_info_flex['losses']

    return [
        f"""SoloQ: {get_tier_rank_emoji_id(player_info_solo['tier'])} {player_info_solo['rank']} {player_info_solo['leaguePoints']}PL {wins_percent_solo}% {total_games_solo}
                    FlexQ: {get_tier_rank_emoji_id(player_info_flex['tier'])} {player_info_flex['rank']} {player_info_flex['leaguePoints']}PL {wins_percent_flex}% {total_games_flex}""",
        player_info_solo['summonerName']]


def get_matches_list(user_name, end_index):
    match_list = get_player_match_list(user_name, end_index)
    final_text = ""
    for match in match_list:
        final_text += f"{get_champion_emoji_id(match['champion'])}"

def player_elo(user_name):
    api = ApiRequest(user_name)
    return api.get_league()


def player_level(user_name):
    api = ApiRequest(user_name)
    return api.get_summoner_data()['summonerLevel']


def player_icon(user_name):
    api = ApiRequest(user_name)
    return api.get_summoner_data()['profileIconId']


def get_player_match_list(user_name, end_index):
    api = ApiRequest(user_name)
    return api.get_match_list(end_index)


def find_solo_tier(tier_list):
    for tier in tier_list:
        if tier['queueType'] == "RANKED_SOLO_5x5":
            return tier


def find_flex_tier(tier_list):
    for tier in tier_list:
        if tier['queueType'] == "RANKED_FLEX_SR":
            return tier


def percent_wins(wins, losses):
    return (wins * 100) / (wins + losses)


def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()
