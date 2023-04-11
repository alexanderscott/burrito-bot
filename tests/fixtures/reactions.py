import json


# @pytest.fixture
def reaction_added_emoji():
    return json.loads("""
    {
        "type": "reaction_added",
        "user": "U01AP4BM8SD",
        "reaction": "burrito",
        "item": {
            "type": "message",
            "channel": "C03LK81TUBB",
            "ts": "1656017324.023839"
        },
        "item_user": "U025RUT3QQM",
        "event_ts": "1656048972.000100"
    }
    """)


def reaction_removed_emoji():
    return json.loads("""
    {
      "type": "reaction_removed",
      "user": "U01AP4BM8SD",
      "reaction": "burrito",
      "item": {
        "type": "message",
        "channel": "G01Q4U75KAP",
        "ts": "1656054184.703169"
      },
      "item_user": "U01AP4BM8SD",
      "event_ts": "1656055991.003400"
    }
    """)
