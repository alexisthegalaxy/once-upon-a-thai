from direction import Direction
from lexicon.items import Letter
from npc.npc import Npc


def plane(al):
    npcs = [
        Npc(
            al=al,
            name="Nim",
            # taught=Letter.get_by_thai("น"),
            ma=al.mas.get_map_from_name("plane"),
            x=8,
            y=7,
            sprite="nim",
            direction=Direction.UP,
            eyesight=1,
            standard_dialog=[
                "So, [Name], are you excited to land in Ko Chang soon?",
                "I can't wait to have a relaxing vacation with my little [sibling_gender_of_player]...",
                "And as promised, I will teach you how to master magic first,",
                "and how to modify the world around you using the magic of Thai language.",
                "As you know, each word is a spell with its own powers...",
                "But first, let's learn the alphabet.",
                "Let me teach you the most common consonant first: N.",
                "I will first show it to you, and then test you on it.",
            ],
            end_dialog_trigger_event=["talked_to_nim_in_plane"],
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=8,
            y=5,
            sprite="kid",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=9,
            y=5,
            standard_dialog=[
                "Hello there!",
                "You're also spending your holidays in Ko Chang island?",
                "Did you know all places in this game are based off real Thailand?",
            ],
            sprite="dad",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=9,
            y=9,
            standard_dialog=[
                "I've played long enough.",
                "To save the game, press s.",
            ],
            sprite="lass",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=8,
            y=9,
            sprite="mom",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=5,
            y=5,
            sprite="old_woman",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=6,
            y=5,
            sprite="old_woman",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=5,
            y=9,
            sprite="kid",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=6,
            y=9,
            sprite="woman",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=5,
            y=7,
            sprite="rich_woman",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=9,
            y=3,
            sprite="dad",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=8,
            y=3,
            sprite="old_man",
            direction=Direction.UP,
        ),
        Npc(
            al=al,
            name="random plane passenger",
            ma=al.mas.get_map_from_name("plane"),
            x=5,
            y=3,
            sprite="mom",
            direction=Direction.UP,
        ),

    ]

    for npc in npcs:
        npc.ma.add_npc(npc)
