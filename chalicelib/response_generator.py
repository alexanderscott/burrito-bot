import random
from typing import List

from chalicelib.global_constants import EMOJI, EMOJI_PLURAL, MAX_POINTS_PER_SENDER_PER_DAY


def count_with_emoji_text(count: int) -> str:
    if count == 1:
        return f"1 {EMOJI}"
    else:
        return f"{count} {EMOJI_PLURAL}"


def _recipients_text(recipients: List[str]) -> str:
    if len(recipients) == 1:
        return f"<@{recipients[0]}>"
    else:
        return f"{len(recipients)} recipients"


def generate_random_response(points: int, recipients: List[str], remaining_points_today: int) -> str:
    secondary_txt_choices = [
        f"Order up!",
        f"Rock on!",
        f"Hope they're hungry!",
        f"Bon apetite!",
    ]

    multiple_recipient_responses = [
        f"Gifted {points if points > 1 else 'a'} :{EMOJI}:{'s' if points > 1 else ''} to {_recipients_text(recipients)}.",
    ]

    single_recipient_responses = [
        f"Gifted <@{recipients[0]}> a :{EMOJI}:.",
    ]

    remaining_text = f"You have {count_with_emoji_text(remaining_points_today)} left to gift today."

    if len(recipients) > 1:
        txt = f"{random.choice(multiple_recipient_responses)}  {random.choice(secondary_txt_choices)}\n{remaining_text}"
    else:
        txt = f"{random.choice(single_recipient_responses)}  {random.choice(secondary_txt_choices)}\n{remaining_text}"

    return txt


def recipient_direct_message(points: int, sender: str) -> str:
    if points == 1:
        primary_txt = f"<@{sender}> has gifted you a :{EMOJI}:!"
    else:
        primary_txt = f"<@{sender}> has gifted you {points} :{EMOJI}:s!"

    secondary_txt_choices = [
        f"Way to go!",
        f"You're doing great!",
        f"Awesome job!",
        f"Fantastic!",
        f"Lucky you!",
        f"Mmmm delicious!",
    ]

    return f"{primary_txt}  {random.choice(secondary_txt_choices)}"


def sender_point_limit_response(points_attempted: int) -> str:
    txt = f"Cannot send {count_with_emoji_text(points_attempted)} - max per day is {MAX_POINTS_PER_SENDER_PER_DAY}!"
    return txt


def sender_in_recipients() -> str:
    txt = f"Cannot send yourself a {EMOJI}! Send to a deserving teammate!"
    return txt
