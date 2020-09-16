import re


def get_champion_emoji_id(champ):
    file = open('./source/emojis_id.txt')
    for emoji in file:
        if re.search(champ, emoji):
            return emoji.replace('\n', " ")
    file.close()


def get_mastery_emoji_id(mastery):
    file = open('./source/emojis_id.txt')
    for emoji in file:
        if re.search(f'level{mastery}', emoji):
            return emoji.replace('\n', " ")
    file.close()


def get_tier_rank_emoji_id(rank):
    file = open('./source/emojis_id.txt')
    for emoji in file:
        if re.search(rank, emoji):
            return emoji.replace('\n', " ")
    file.close()
