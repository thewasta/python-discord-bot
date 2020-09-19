from RiotApi.LoLApiRequest import ApiRequest
import json
from utils.Emojis import get_tier_rank_emoji_id, get_mastery_emoji_id, get_champion_emoji_by_name

league_graph_url = "https://www.leagueofgraphs.com/match/euw/"


def get_profile_details_for_embed(username):
    api = ApiRequest(username)
    champions_list: dict = api.get_best_champions()
    best_champs_info = []
    for champions in champions_list:
        best_champs_info.append({
            "id": champions['championId'],
            "level": champions['championLevel'],
            "points": champions['championPoints'],
        })
    top_champ_list = []
    with open('./source/data/es_ES/champion.json') as json_file:
        for name, info in json.load(json_file)['data'].items():
            for best_champ in best_champs_info:
                if info['key'] == str(best_champ['id']):
                    top_champ_list.append({
                        "name": name,
                        "level": best_champ['level'],
                        "points": best_champ['points']
                    })
                    break

    return get_text_player(sorted(top_champ_list, key=lambda x: x['points'], reverse=True))


def get_champion_name(champion_id: str) -> str:
    with open('./source/data/es_ES/champion.json') as json_file:
        for name, info in json.load(json_file)['data'].items():
            if info['key'] == str(champion_id):
                return name


def get_text_player(data_champions):
    final_text = ""
    for champion in data_champions:
        if champion['points'] >= 1000:
            champion['points'] = int(str(champion['points'])[:3])
        final_text += "{}{} - {}K {} \n".format(get_champion_emoji_by_name(champion['name']), champion['name'],
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
        f"""SoloQ: {get_tier_rank_emoji_id(player_info_solo['tier'])} {player_info_solo['rank']} {player_info_solo['leaguePoints']}PL {wins_percent_solo}% - {total_games_solo}
                    FlexQ: {get_tier_rank_emoji_id(player_info_flex['tier'])} {player_info_flex['rank']} {player_info_flex['leaguePoints']}PL {wins_percent_flex}% - {total_games_flex}""",
        player_info_solo['summonerName']]


def get_string_match_embed(user_name, end_index):
    # _CHAMPIONEMOJI_ _5/5/5_ _WIN_
    match_list = get_matches_list(user_name, end_index)
    match_list_details = get_list_match_details(user_name, match_list)
    final_text = ''
    for match_details in match_list_details:
        print(match_details['champion'])
        print(get_champion_name(match_details['champion']))
        champ_emoji = get_champion_emoji_by_name(get_champion_name(match_details['champion']))
        kda_result = "{}/{}/{}".format(match_details['kills'], match_details['deaths'], match_details['assists'])
        final_text += """{} {} {match_result} [LeagueGraph]({link_match} 'Datos de la partida')\n""".format(champ_emoji,
                                                                                                            kda_result,
                                                                                                            match_result="<:victory:755862932541407302>" if
                                                                                                            match_details[
                                                                                                                'win'] else "<:defeat:755862932461584415>",
                                                                                                            link_match=league_graph_url + f"{match_details['gameId']}")
    return final_text


def get_matches_list(user_name, end_index):
    match_list = get_player_match_list(user_name, end_index)
    list_match = []
    for match in match_list:
        list_match.append({
            "gameId": match['gameId'],
            "champion": match['champion']
        })

    return list_match


def get_list_match_details(user_name, match_id_list):
    api = ApiRequest(user_name)
    result = []
    for match in match_id_list:
        details = api.get_match_detail(match['gameId'])
        participants = details['participants']
        for participant in participants:
            if participant['championId'] == match['champion']:
                result.append({
                    "gameId": match['gameId'],
                    "champion": match['champion'],
                    "win": participant['stats']['win'],
                    "kills": participant['stats']['kills'],
                    "deaths": participant['stats']['deaths'],
                    "assists": participant['stats']['assists']
                })
            break

    return result


def player_elo(user_name):
    api = ApiRequest(user_name)
    return api.get_league()


def player_level(user_name):
    api = ApiRequest(user_name)
    return api.get_summoner_data()['summonerLevel']


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
