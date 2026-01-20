import random
from django.db import transaction


def calculate_game_result(game):
    attacker_card = game.attacker_card
    defender_card = game.defender_card

    # 무승부 처리
    if attacker_card == defender_card:
        game.attacker_result = 'draw'
        game.defender_result = 'draw'
        game.attacker_score_change = 0
        game.defender_score_change = 0
        return

    # 승패 판정
    if game.win_rule == 'HIGH':
        attacker_wins = attacker_card > defender_card
    else:  # LOW
        attacker_wins = attacker_card < defender_card

    # 결과 및 점수 변동 계산
    if attacker_wins:
        game.attacker_result = 'win'
        game.defender_result = 'lose'
        game.attacker_score_change = attacker_card
        game.defender_score_change = -defender_card
    else:
        game.attacker_result = 'lose'
        game.defender_result = 'win'
        game.attacker_score_change = -attacker_card
        game.defender_score_change = defender_card

    # 유저 점수 업데이트
    with transaction.atomic():
        attacker_profile = game.attacker.profile
        defender_profile = game.defender.profile

        attacker_profile.score += game.attacker_score_change
        defender_profile.score += game.defender_score_change

        attacker_profile.save()
        defender_profile.save()


def generate_random_cards(count=5):
    return random.sample(range(1, 11), count)


def is_valid_card_number(card_number):
    try:
        card = int(card_number)
        return 1 <= card <= 10
    except (ValueError, TypeError):
        return False