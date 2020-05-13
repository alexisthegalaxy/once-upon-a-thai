import time
import pygame

from lexicon.items import Words
from mechanics.minimap import want_to_launch_map

import os

from profile.profile import save
from ui.import_images_and_fonts import get_sprites, random_images, npc_sprites

dir_path = os.path.dirname(os.path.realpath(__file__))


class Fonts(object):
    def __init__(self):
        sarabun_path = f"{dir_path}/../fonts/Sarabun.ttf"
        self.khmer32 = pygame.font.Font(f"{dir_path}/../fonts/Khmer.ttf", 32)
        self.lao32 = pygame.font.Font(f"{dir_path}/../fonts/Lao.ttf", 32)
        self.burmese32 = pygame.font.Font(f"{dir_path}/../fonts/ZawgyiOne.ttf", 32)
        self.sanskrit32 = pygame.font.Font(f"{dir_path}/../fonts/Jaldi.ttf", 32)

        self.sarabun128 = pygame.font.Font(sarabun_path, 128)
        self.sarabun96 = pygame.font.Font(sarabun_path, 96)
        self.sarabun64 = pygame.font.Font(sarabun_path, 64)
        self.sarabun48 = pygame.font.Font(sarabun_path, 48)
        self.sarabun32 = pygame.font.Font(sarabun_path, 32)
        self.sarabun16 = pygame.font.Font(sarabun_path, 16)
        self.sarabun18 = pygame.font.Font(sarabun_path, 18)
        self.sarabun24 = pygame.font.Font(sarabun_path, 24)
        self.sarabun28 = pygame.font.Font(sarabun_path, 28)


class Ui(object):
    def __init__(self):
        logo = pygame.image.load(f"{dir_path}/../images/thai.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Once upon a Thai!")
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fonts = Fonts()
        self.sprites = get_sprites()
        self.images = random_images()
        self.npc_sprites = npc_sprites()
        self.clock = pygame.time.Clock()
        self.cell_size = 80
        self.draw_tick = 0.03
        self.last_draw_tick = 0

        self.click = None  # looks like (x, y)
        self.click_up = None  # looks like (x, y)
        self.hover = None  # looks like (x, y)

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.backspace = False
        self.plus = False
        self.minus = False
        self.w = False
        self.m = False
        self.escape = False

    def can_draw_cell(self, x: int, y: int, cell_is_special=False):
        if not cell_is_special:
            min_x = -self.cell_size
            min_y = -self.cell_size
            return min_x <= x <= self.width and min_y <= y <= self.height
        min_x = -self.cell_size * 4
        min_y = -self.cell_size * 4
        result = min_x <= x <= self.width * 3 and min_y <= y <= self.height * 3
        return result

    def percent_height(self, ratio):
        return int(ratio * self.height)

    def percent_width(self, ratio):
        return int(ratio * self.width)

    def lapsed_tick(self) -> bool:
        return time.time() - self.last_draw_tick > self.draw_tick

    def tick(self) -> None:
        self.last_draw_tick = time.time()

    def listen_event(self, al):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    al.ui.up = True
                if event.key == pygame.K_DOWN:
                    al.ui.down = True
                if event.key == pygame.K_RIGHT:
                    al.ui.right = True
                if event.key == pygame.K_LEFT:
                    al.ui.left = True
                if event.key == 61:  # PLUS
                    al.ui.plus = True
                if event.key == pygame.K_MINUS:
                    al.ui.minus = True
                if event.key == pygame.K_o:
                    al.learner.open()
                if event.key == pygame.K_r:
                    # Words.reset_words(xp=0)
                    # al.learner.money = 3
                    al.learner.hp = 5
                    al.learner.max_hp = 5
                if event.key == pygame.K_u:
                    al.learner.hp = max(al.learner.hp - 1/8, 0)
                # if event.key == pygame.K_t:
                #     Words.reset_words(xp=100)
                if event.key == pygame.K_BACKSPACE:
                    al.ui.backspace = True
                if event.key == pygame.K_SPACE:
                    al.ui.space = True
                if event.key == pygame.K_w:
                    al.dex.w()
                if event.key == pygame.K_l:
                    al.lex.l()
                if event.key == pygame.K_m:
                    if not al.active_presentation:
                        if al.active_minimap:
                            al.active_minimap = None
                        else:
                            want_to_launch_map(al, show_learner=True)
                    else:
                        al.ui.m = True
                if event.key == pygame.K_RETURN:
                    al.ui.space = True
                if event.key == pygame.K_p:
                    al.learner.print_location()
                if event.key == pygame.K_ESCAPE:
                    # TODO All of this should be processed after all the al.interact
                    #  so that each component can have its own way of dealing with the escape key
                    #  eg Dex closing the presentation page.
                    al.ui.escape = True
                    if al.active_test:
                        al.active_test = None
                        al.ui.escape = False
                    elif al.active_minimap:
                        al.active_minimap = None
                        al.ui.escape = False
                    elif al.active_npc:
                        al.active_npc = None
                        al.ui.escape = False
                    elif al.active_naming:
                        al.active_naming.end_naming()
                        al.ui.escape = False
                    elif al.active_fight:
                        al.active_fight.end_fight()
                        al.ui.escape = False
                    elif al.active_consonant_race:
                        al.active_consonant_race.end()
                        al.ui.escape = False
                    elif al.active_sale:
                        al.active_sale = None
                        al.ui.escape = False
                    elif al.active_spell_identification:
                        al.active_spell_identification = None
                        al.ui.escape = False
                if event.key == pygame.K_s:
                    save(al)
                # if event.key == pygame.K_l:
                #     al.profiles.current_profile.load(al)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    al.ui.up = False
                if event.key == pygame.K_DOWN:
                    al.ui.down = False
                if event.key == pygame.K_RIGHT:
                    al.ui.right = False
                if event.key == pygame.K_LEFT:
                    al.ui.left = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                al.ui.click = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEBUTTONUP:
                al.ui.click_up = pygame.mouse.get_pos()
            elif event.type == pygame.MOUSEMOTION:
                al.ui.hover = pygame.mouse.get_pos()

