import json


# @pytest.fixture
def message_added_single_emoji_single_recipient():
    return json.loads("""
    {
        "client_msg_id": "8114f141-b9d9-4c0a-b73e-004fb10b3721",
        "type": "message",
        "text": "<@U025RUT3QQM> :burrito:",
        "user": "U01AP4BM8SD",
        "ts": "1656021597.657979",
        "team": "T01929SP50C",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "EVBP",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U025RUT3QQM"
                            },
                            {
                                "type": "text",
                                "text": " "
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            }
                        ]
                    }
                ]
            }
        ],
        "channel": "G01Q4U75KAP",
        "event_ts": "1656021597.657979",
        "channel_type": "group"
    }
    """)


def thread_message_added_single_emoji_single_recipient():
    return json.loads("""
    {
      "client_msg_id": "edb5d552-3237-43bf-b984-e4e15ef8d57b",
      "type": "message",
      "text": "<@U025RUT3QQM> thread :burrito:",
      "user": "U01AP4BM8SD",
      "ts": "1656384418.460309",
      "team": "T01929SP50C",
      "blocks": [
        {
          "type": "rich_text",
          "block_id": "fbJ3L",
          "elements": [
            {
              "type": "rich_text_section",
              "elements": [
                {
                  "type": "user",
                  "user_id": "U025RUT3QQM"
                },
                {
                  "type": "text",
                  "text": " thread "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                }
              ]
            }
          ]
        }
      ],
      "thread_ts": "1656384026.588109",
      "parent_user_id": "U01AP4BM8SD",
      "channel": "G01Q4U75KAP",
      "event_ts": "1656384418.460309",
      "channel_type": "group"
    }
    """)


def message_added_six_emojis_single_recipient():
    return json.loads("""
    {
      "client_msg_id": "b37fae04-bd59-4fdc-b038-89be0a65a8c2",
      "type": "message",
      "text": "<@U01AP4BM8SD> :burrito: :burrito: :burrito: :burrito: :burrito: :burrito:",
      "user": "U01AP4BM8SD",
      "ts": "1656384992.257099",
      "team": "T01929SP50C",
      "blocks": [
        {
          "type": "rich_text",
          "block_id": "gZlAY",
          "elements": [
            {
              "type": "rich_text_section",
              "elements": [
                {
                  "type": "user",
                  "user_id": "U01AP4BM8SD"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                },
                {
                  "type": "text",
                  "text": " "
                },
                {
                  "type": "emoji",
                  "name": "burrito",
                  "unicode": "1f32f"
                }
              ]
            }
          ]
        }
      ],
      "thread_ts": "1656384026.588109",
      "parent_user_id": "U01AP4BM8SD",
      "channel": "G01Q4U75KAP",
      "event_ts": "1656384992.257099",
      "channel_type": "group"
    }
    """)


def message_added_single_emoji_multiple_recipients():
    return json.loads("""
    {
        "client_msg_id": "8114f141-b9d9-4c0a-b73e-004fb10b3721",
        "type": "message",
        "text": "<@U0G9QF9C6> <@U0G9QF9C7> :burrito:",
        "user": "U025RUT3QQM",
        "ts": "1656021597.657979",
        "team": "T01929SP50C",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "EVBP",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U0G9QF9C6"
                            },
                            {
                                "type": "user",
                                "user_id": "U0G9QF9C7"
                            },
                            {
                                "type": "text",
                                "text": " "
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            }
                        ]
                    }
                ]
            }
        ],
        "channel": "G01Q4U75KAP",
        "event_ts": "1656021597.657979",
        "channel_type": "group"
    }
    """)


def message_added_multiple_emojis_single_recipient():
    return json.loads("""
    {
        "client_msg_id": "8114f141-b9d9-4c0a-b73e-004fb10b3721",
        "type": "message",
        "text": "<@U0G9QF9C6> :burrito: :burrito:",
        "user": "U025RUT3QQM",
        "ts": "1656021597.657979",
        "team": "T01929SP50C",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "EVBP",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U0G9QF9C6"
                            },
                            {
                                "type": "text",
                                "text": " "
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            }
                        ]
                    }
                ]
            }
        ],
        "channel": "G01Q4U75KAP",
        "event_ts": "1656021597.657979",
        "channel_type": "group"
    }
    """)

def message_added_multiple_emojis_multiple_recipients():
    return json.loads("""
    {
        "client_msg_id": "8114f141-b9d9-4c0a-b73e-004fb10b3721",
        "type": "message",
        "text": "<@U0G9QF9C6> <@U0G9QF9C7> :burrito: :burrito:",
        "user": "U025RUT3QQM",
        "ts": "1656021597.657979",
        "team": "T01929SP50C",
        "blocks": [
            {
                "type": "rich_text",
                "block_id": "EVBP",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "user",
                                "user_id": "U0G9QF9C6"
                            },
                            {
                                "type": "user",
                                "user_id": "U0G9QF9C7"
                            },
                            {
                                "type": "text",
                                "text": " "
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            },
                            {
                                "type": "emoji",
                                "name": "burrito",
                                "unicode": "1f32f"
                            }
                        ]
                    }
                ]
            }
        ],
        "channel": "G01Q4U75KAP",
        "event_ts": "1656021597.657979",
        "channel_type": "group"
    }
    """)
