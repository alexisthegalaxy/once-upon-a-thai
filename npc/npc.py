import copy
from dataclasses import dataclass
from datetime import datetime
import time
import pygame
from typing import List, Tuple, Optional, Union

from direction import string_from_direction, opposite_direction, Direction, dir_equal
from languages import render_multilingual_text
from lexicon.items import Word, Letter
from lexicon.learning import LetterLearning, WordLearning
from models import xp_from_word
from npc.letter import get_sprite_name_from_letter_class
from npc.question import Question
from sounds.play_sound import play_thai_word


def _get_time_type():
    now = datetime.now().microsecond
    if now < 250_000:
        return 1
    if now < 500_000:
        return 2
    if now < 750_000:
        return 3
    return 4


def _process_dialog(dialog: List[str], al: "All"):
    for i, line in enumerate(dialog):
        if type(line) == str:
            dialog[i] = line.replace("[Name]", al.learner.name)
            if "[sibling_gender_of_player]" in dialog[i]:
                if al.learner.gender == 0:
                    sibling = "sister"
                else:
                    sibling = "brother"
                dialog[i] = line.replace("[sibling_gender_of_player]", sibling)


def _can_turn(sprite_type):
    return not (
        sprite_type
        in [
            "sign",
            "bed",
            "chest_open",
            "chest_closed",
            "television_on",
            "crashed_plane",
            "spirit_bird",
            "spirit_bird_invisible",
            "spirit_gecko",
            "spirit_gecko_invisible",
            "garbage_0",
            "garbage_1",
            "garbage_2",
            "garbage_3",
            "television_off",
            "boat",
            "seed",
        ]
        or "spell" in sprite_type
    )


def _is_gif(sprite):
    return sprite and sprite[0] == "_"


def make_letter_beaten(wild_letter):
    wild_letter.is_walkable = True
    wild_letter.wobble = False
    wild_letter.shows_sprite = False
    wild_letter.letter_color = (255, 255, 255)


@dataclass
class Position:
    x: int
    y: int


Dialog = List[Union[str, Question]]


class Npc(object):
    def __init__(
        self,
        al,
        ma,
        x,
        y,
        name="...",
        standard_dialog=None,  # pre-fight, normal talk, pre-learn
        standard_dialog_2=None,  # npc says that instead of standard_dialog after having talked once already
        defeat_dialog=None,  # post-fight
        victory_dialog=None,  # post-fight
        extra_dialog_1=None,  # use in triggers
        extra_dialog_2=None,  # use in triggers
        extra_dialog_3=None,  # use in triggers
        extra_dialog_4=None,  # use in triggers
        extra_dialog_5=None,  # use in triggers
        direction=Direction.UP,
        sprite="kid",
        taught: Union[Word, Letter] = None,
        fight_words: List[Word] = None,
        money: int = 5,  # amount given when lost the fight
        lost_money_on_defeat: int = 0,  # amount lost when Learner loses
        eyesight: int = 5,  # how far the trainer can see
        wanna_meet: bool = False,  # if true, non trainers will also walk to the learner and start talking
        bubbles_max_hp: int = 1000,
        appears_between: Tuple[int, int] = (0, 24),
        end_dialog_trigger_event: List[str] = None,
        beginning_dialog_trigger_event: List[str] = None,
        consonants: List[Letter] = None,
        wobble=False,
        letter=None,
        is_walkable=False,
        shows_sprite=True,
        naming=None,
        is_silent=False,
        letter_color=(0, 0, 0),
        hp=2,
    ):
        standard_dialog = standard_dialog or ["Hello"]
        defeat_dialog = defeat_dialog or ["Well done!"]
        victory_dialog = victory_dialog or ["I won! Try again when you're stronger!"]
        self.end_dialog_trigger_event = end_dialog_trigger_event or []
        self.beginning_dialog_trigger_event = beginning_dialog_trigger_event or []
        self.extra_dialog_1 = extra_dialog_1 or []
        self.extra_dialog_2 = extra_dialog_2 or []
        self.extra_dialog_3 = extra_dialog_3 or []
        self.extra_dialog_4 = extra_dialog_4 or []
        self.extra_dialog_5 = extra_dialog_5 or []
        # if standard_dialog_2 exists, the npc will say that instead of standard_dialog, but only after the first time
        self.standard_dialog_2 = standard_dialog_2 or []

        self.name = name
        self.ma = ma
        self.sprite = sprite
        self.x = x
        self.y = y
        self.money = money
        self.lost_money_on_defeat = lost_money_on_defeat
        self.standard_dialog: Dialog = standard_dialog
        self.defeat_dialog: Dialog = defeat_dialog
        self.victory_dialog: Dialog = victory_dialog
        self.review_dialog: Dialog = ["Do you want to review the word"]
        self.dialogs = [
            self.standard_dialog,
            self.standard_dialog_2,
            self.defeat_dialog,
            self.victory_dialog,
            self.extra_dialog_1,
            self.extra_dialog_2,
            self.extra_dialog_3,
            self.extra_dialog_4,
            self.extra_dialog_5,
        ]
        self.active_dialog: Dialog = self.standard_dialog[:]
        self.direction = direction
        self.active_line_index = -1
        self.color = (0, 222, 222)
        self.taught = taught
        self.fight_words = fight_words
        self.has_learning_mark = self.taught and xp_from_word(self.taught.id) <= 0
        self.wants_battle = True
        self.wanna_meet = wanna_meet
        self.eyesight = eyesight
        self.have_exclamation_mark_until = None
        # must_walk_to - list of position: must first walk to the first, then when reached the first is removed
        self.must_walk_to: List[Position] = []
        self.walked_float = 0
        self.draw_text_since = 0
        self.bubbles_max_hp = bubbles_max_hp
        self.appears_between = appears_between
        self.process_dialog(al)
        self.wobble = wobble
        self.hp = hp
        self.letter_color = letter_color
        self.shows_sprite = shows_sprite
        self.is_walkable = is_walkable
        self.is_silent = is_silent
        self.consonants = consonants
        self.naming = naming
        if self.naming:
            self.naming.npc = self

        self.letter = letter
        if self.letter:
            self.sprite = get_sprite_name_from_letter_class(letter.class_, al)
            self.wobble = True
            self.taught = self.letter

    def process_dialog(self, al):
        for dialog in self.dialogs:
            _process_dialog(dialog, al)
        if self.taught:
            self.review_dialog[0] = self.review_dialog[0] + f" {self.taught.thai} ?"

    def is_trainer(self):
        return bool(self.fight_words)

    def sees_learner(self, al) -> Optional[List[Position]]:
        """
        :return: the must_walk_to position if there's one, else None
        """
        result = None
        if dir_equal(self.direction, Direction.UP):
            if (
                al.learner.x == self.x
                and al.learner.y < self.y
                and self.y - al.learner.y <= self.eyesight
            ):
                can_walk_to_trainer = True
                for y in range(al.learner.y, self.y):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(self.x, y).walkable()
                    )
                if can_walk_to_trainer:
                    result = Position(x=al.learner.x, y=al.learner.y + 1)
        elif dir_equal(self.direction, Direction.DOWN):
            if (
                al.learner.x == self.x
                and al.learner.y > self.y
                and al.learner.y - self.y <= self.eyesight
            ):
                can_walk_to_trainer = True
                for y in range(self.y, al.learner.y):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(self.x, y).walkable()
                    )
                if can_walk_to_trainer:
                    result = Position(x=al.learner.x, y=al.learner.y - 1)
        elif dir_equal(self.direction, Direction.RIGHT):
            if (
                al.learner.y == self.y
                and al.learner.x > self.x
                and al.learner.x - self.x <= self.eyesight
            ):
                can_walk_to_trainer = True
                for x in range(self.x, al.learner.x):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(x, self.y).walkable()
                    )
                if can_walk_to_trainer:
                    result = Position(x=al.learner.x - 1, y=al.learner.y)
        elif dir_equal(self.direction, Direction.LEFT):
            if (
                al.learner.y == self.y
                and al.learner.x < self.x
                and self.x - al.learner.x <= self.eyesight
            ):
                can_walk_to_trainer = True
                for x in range(al.learner.x, self.x):
                    can_walk_to_trainer = (
                        can_walk_to_trainer
                        and al.mas.current_map.get_cell_at(x, self.y).walkable()
                    )
                if can_walk_to_trainer:
                    result = Position(x=al.learner.x + 1, y=al.learner.y)
        if result:
            return [result]
        return None

    def is_saying_last_sentence(self) -> bool:
        return self.active_line_index == len(self.active_dialog) - 1

    def last_sentence_special_interaction(self, al):
        if self.active_dialog == self.standard_dialog and self.standard_dialog_2:
            self.active_dialog = self.standard_dialog_2
        if self.taught:
            if (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = (
                    WordLearning(al=al, word=self.taught, npc=self)
                    if isinstance(self.taught, Word)
                    else LetterLearning(al=al, letter=self.taught, npc=self)
                )
                al.active_learning.goes_to_first_step()
        if self.naming:
            if (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_naming = self.naming
                al.active_naming.actualize()
            if self.active_dialog == self.victory_dialog:
                self.active_dialog = self.standard_dialog[:]
        if self == "is a spell":  # TODO
            if (
                self.active_dialog == self.standard_dialog
                or self.active_dialog == self.review_dialog
            ):
                al.active_learning = (
                    WordLearning(al=al, word=self.taught, npc=self)
                    if isinstance(self.taught, Word)
                    else LetterLearning(al=al, letter=self.taught, npc=self)
                )
                al.active_learning.goes_to_first_step()
        if self.fight_words:
            if self.active_dialog == self.standard_dialog:
                from mechanics.fight.fight import Fight

                al.active_fight = Fight(
                    al=al, words=self.fight_words, npc=self, starting="npc"
                )
            if self.active_dialog == self.victory_dialog:
                al.learner.faints()
                self.active_dialog = self.standard_dialog[:]
                self.active_line_index = 0  # this should be -2 maybe because just after we will increase by one
        if self.consonants:
            if self.active_dialog == self.victory_dialog:
                self.active_dialog = self.standard_dialog[:]
                self.active_line_index = -2
                al.active_npc = None
            elif self.active_dialog == self.defeat_dialog:
                self.active_dialog = self.standard_dialog[:]
                self.active_line_index = -2
                al.active_npc = None
            else:
                from mechanics.consonant_race.consonant_race import ConsonantRace
                # TODO weirdly this seems to be triggered but then the race doesnt start
                al.active_consonant_race = ConsonantRace(
                    al=al, consonants=self.consonants, npc=self
                )

    def special_interaction(self, al):
        from event import execute_event

        if self.active_line_index == -1 and self.active_dialog == self.standard_dialog:
            for event in self.beginning_dialog_trigger_event:
                execute_event(event, al)
        if self.name == "nurse":
            if self.active_line_index == -1:
                play_thai_word("welcome")
            if self.active_line_index == 0:
                al.learner.inn_heal()
        if self.name == "bed":
            if self.active_line_index == 0:
                al.learner.bed_heal()
        if self.active_line_index == -1:
            play_thai_word(self.name)
        if self.is_saying_last_sentence():
            self.last_sentence_special_interaction(al)

    def go_to_next_line(self):
        self.active_line_index += 1

    def interact(self, al):
        if type(self.active_dialog[self.active_line_index]) == Question:
            self.active_dialog[self.active_line_index].interact(al)

    def reset_dialogs(self, al):
        self.active_dialog = self.standard_dialog[:]

    def first_interaction(self, al):
        self.direction = opposite_direction(al.learner.direction)
        self.has_learning_mark = False
        self.wanna_meet = False
        if not al.active_npc:
            self.reset_dialogs(al)
            if self.taught:  # If this NPC teaches
                if self.taught.total_xp >= 5:  # If the word is known
                    self.active_dialog = self.review_dialog
        al.active_npc = self

    def handle_question(self, al):
        try:
            if self.active_line_index > -1 and type(self.active_dialog[self.active_line_index]) == Question:
                self.active_dialog[self.active_line_index].execute_callback(al, self)
        except IndexError:
            print('ERROR WHEN HANDLING QUESTION!')

    def handle_dialog_triggered_events(self, al):
        if self.active_line_index >= len(
            self.active_dialog
        ):  # if this is the end of the current dialog
            self.active_line_index = -1
            trigger_event = False
            if self.taught:
                if self.active_dialog == self.defeat_dialog:
                    trigger_event = True
                    if self.letter:
                        make_letter_beaten(self)
            else:
                trigger_event = True
            if trigger_event:
                from event import execute_event
                for event in self.end_dialog_trigger_event:
                    execute_event(event, al)
            al.active_npc = None

    def space_interact(self, al):
        self.reset_cursor()
        self.first_interaction(al)
        self.handle_question(al)
        self.special_interaction(al)
        self.go_to_next_line()
        self.handle_dialog_triggered_events(al)

    def get_precise_position(self, x, y):
        if dir_equal(self.direction, Direction.UP):
            return x, y - self.walked_float
        if dir_equal(self.direction, Direction.DOWN):
            return x, y + self.walked_float
        if dir_equal(self.direction, Direction.RIGHT):
            return x + self.walked_float, y
        if dir_equal(self.direction, Direction.LEFT):
            return x - self.walked_float, y

    def should_appear(self):
        now = datetime.now().hour
        # appears_between = 23 - 5
        a0 = self.appears_between[0]
        a1 = self.appears_between[1]
        if a0 > a1:
            # a0 = 23
            # a1 = 5
            return now >= a0 or now < a1
        elif a1 > a0:
            # a0 = 8
            # a1 = 16
            return a0 <= now < a1
        return True

    def _maybe_draw_letter(self, ui, x, y):
        """Used to draw Thai Letters on the overworld"""
        if self.letter:
            rendered_letter = ui.fonts.sarabun32.render(f" {self.letter.thai} ", True, self.letter_color)
            x += int(ui.cell_size / 2 - rendered_letter.get_width() / 2)
            y += int(ui.cell_size / 2 - rendered_letter.get_height() / 2)
            ui.screen.blit(rendered_letter, (x, y))

    def _draw_ow(self, al, x, y):
        if not self.should_appear():
            return

        # get sprite
        time_type = _get_time_type()
        sprite_name = self.sprite
        sprite = None
        if _can_turn(self.sprite):
            sprite_name += f"_{string_from_direction(self.direction)}"
        if _is_gif(self.sprite):
            sprite_name = f"{self.sprite}_{time_type}"
        if sprite_name in al.ui.npc_sprites:
            sprite = al.ui.npc_sprites[sprite_name]

        x, y = self.get_precise_position(x, y)
        if self.wobble:
            if time_type == 1:
                y -= 1
            elif time_type == 2:
                y -= 2
            elif time_type == 3:
                y -= 1

        x += al.weather.get_offset_x()
        y += al.weather.get_offset_y()

        if sprite:
            if self.shows_sprite:
                al.ui.screen.blit(sprite, [x, y])
            self._maybe_draw_letter(al.ui, x, y)
        else:
            pygame.draw.rect(
                al.ui.screen,
                self.color,
                pygame.Rect(x, y, al.ui.cell_size, al.ui.cell_size),
            )

        if self.have_exclamation_mark_until:
            now = time.time()
            if self.have_exclamation_mark_until > now:
                al.ui.screen.blit(
                    al.ui.images["exclamation_mark"], [x, y - al.ui.cell_size]
                )
            else:
                self.have_exclamation_mark_until = None
        elif self.has_learning_mark:
            al.ui.screen.blit(al.ui.images["learning_mark"], [x, y - al.ui.cell_size])

    def draw(self, al):
        if not self.sprite == "":
            offset_x = -al.ui.cell_size * (al.learner.x - 7)
            offset_y = -al.ui.cell_size * (al.learner.y - 4)

            if (not al.learner.can_move()) and al.learner.movement:
                movement_offset_x, movement_offset_y = al.learner.movement.get_offset()
                offset_x += movement_offset_x * al.ui.cell_size
                offset_y += movement_offset_y * al.ui.cell_size

            x = self.x * al.ui.cell_size + offset_x
            y = self.y * al.ui.cell_size + offset_y
            self._draw_ow(al, x, y)

    def gets_exclamation_mark(self):
        now = time.time()
        self.have_exclamation_mark_until = now + 0.5

    def makes_a_step_towards_goal(self, al):
        must_walk_to = self.must_walk_to[0]
        if must_walk_to.x > self.x:
            self.x += 1
        elif must_walk_to.x < self.x:
            self.x -= 1
        elif must_walk_to.y > self.y:
            self.y += 1
        elif must_walk_to.y < self.y:
            self.y -= 1

        if self.x == must_walk_to.x and self.y == must_walk_to.y:
            self.must_walk_to.pop(0)
            if self.must_walk_to:
                if self.must_walk_to[0] == Position(x=0, y=0):
                    self.disappears(al)
                else:
                    must_walk_to = self.must_walk_to[0]
                    if must_walk_to.x > self.x:
                        self.direction = Direction.RIGHT
                    elif must_walk_to.x < self.x:
                        self.direction = Direction.LEFT
                    elif must_walk_to.y > self.y:
                        self.direction = Direction.DOWN
                    elif must_walk_to.y < self.y:
                        self.direction = Direction.UP
            elif al.learner.next_position() == (self.x, self.y):
                al.learner.direction = opposite_direction(self.direction)
                self.space_interact(al)

    def disappears(self, al):
        al.mas.current_map.npcs = [
            npc for npc in al.mas.current_map.npcs if npc != self
        ]

    def switch_to_dialog(self, dialog):
        self.active_dialog = dialog
        self.active_line_index = 0
        self.reset_cursor()

    def reset_cursor(self):
        self.draw_text_since = time.time()
