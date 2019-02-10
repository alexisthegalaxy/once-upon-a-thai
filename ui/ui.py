# import os

import pygame


class Fonts(object):
    def __init__(self):
        self.garuda64 = pygame.font.Font("../fonts/Garuda.ttf", 64)
        self.garuda32 = pygame.font.Font("../fonts/Garuda.ttf", 32)
        self.garuda16 = pygame.font.Font("../fonts/Garuda.ttf", 16)
        self.setha64 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 64)
        self.setha32 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 32)
        self.setha16 = pygame.font.Font("../fonts/JS-Setha-Normal.ttf", 16)


def npc_sprites():
    # TODO Alexis
    # This should be done automatically
    return {
        "sign": pygame.image.load("../npc/sprites/sign.png"),
        "mom_up": pygame.image.load("../npc/sprites/mom_up.png"),
        "mom_down": pygame.image.load("../npc/sprites/mom_down.png"),
        "mali_down": pygame.image.load("../npc/sprites/mali_down.png"),
        "mom_right": pygame.image.load("../npc/sprites/mom_right.png"),
        "mom_left": pygame.image.load("../npc/sprites/mom_left.png"),
        "old_man_left": pygame.image.load("../npc/sprites/old_man_left.png"),
        "old_man_right": pygame.image.load("../npc/sprites/old_man_right.png"),
        "old_man_down": pygame.image.load("../npc/sprites/old_man_down.png"),
        "old_man_up": pygame.image.load("../npc/sprites/old_man_down.png"),
        "kid_up": pygame.image.load("../npc/sprites/kid_up.png"),
        "nurse_down": pygame.image.load("../npc/sprites/nurse_down.png"),
        "monk_down": pygame.image.load("../npc/sprites/monk_down.png"),
    }


def random_images():
    return {
        "full_heart": pygame.image.load("../images/full_heart.png"),
        "empty_heart": pygame.image.load("../images/empty_heart.png"),
    }


class Ui(object):
    def __init__(self):
        # dir_path = os.path.dirname(os.path.realpath(__file__))
        logo = pygame.image.load("../images/thai.png")
        pygame.init()
        pygame.font.init()
        pygame.display.set_icon(logo)
        pygame.display.set_caption("Learn Thai!")
        self.width = 1200
        self.height = 700
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.fonts = Fonts()
        self.sprites = {
            "grass": pygame.image.load("../ow/sprites/grass.bmp"),
            "path": pygame.image.load("../ow/sprites/path.bmp"),
            "tree": pygame.image.load("../ow/sprites/tree.bmp"),
            "water": pygame.image.load("../ow/sprites/water.bmp"),
            "ground": pygame.image.load("../ow/sprites/ground.bmp"),
            "tall_grass": pygame.image.load("../ow/sprites/tall_grass.bmp"),
        }
        self.images = random_images()
        self.npc_sprites = npc_sprites()
        self.clock = pygame.time.Clock()
        self.cell_size = 80

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.space = False
        self.backspace = False
        self.w = False

    def can_draw_cell(self, x: int, y: int):
        min_x = -self.cell_size
        min_y = -self.cell_size
        return min_x <= x <= self.width and min_y <= y <= self.height

    def percent_height(self, ratio):
        return int(ratio * self.height)

    def percent_width(self, ratio):
        return int(ratio * self.width)

    def listen_event(self, al):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    al.ui.up = True
                if event.key == pygame.K_DOWN:
                    al.ui.down = True
                if event.key == pygame.K_RIGHT:
                    al.ui.right = True
                if event.key == pygame.K_LEFT:
                    al.ui.left = True
                if event.key == pygame.K_o:
                    al.learner.open()
                if event.key == pygame.K_r:
                    al.words.reset_words(al)
                if event.key == pygame.K_BACKSPACE:
                    al.ui.backspace = True
                if event.key == pygame.K_SPACE:
                    al.ui.space = True
                if event.key == pygame.K_w:
                    al.dex.w()
                if event.key == pygame.K_RETURN:
                    al.ui.space = True
                if event.key == pygame.K_p:
                    al.learner.print_location()
                if event.key == pygame.K_ESCAPE:
                    if al.active_test:
                        al.active_test = None
                    elif al.active_learning:
                        al.active_learning = None
                    elif al.active_npc:
                        al.active_npc = None
                    elif al.dex.active:
                        al.dex.active = False
                    else:
                        self.running = False
                if event.key == pygame.K_s:
                    al.profiles.current_profile.save(al)
                if event.key == pygame.K_l:
                    al.profiles.current_profile.load(al)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    al.ui.up = False
                if event.key == pygame.K_DOWN:
                    al.ui.down = False
                if event.key == pygame.K_RIGHT:
                    al.ui.right = False
                if event.key == pygame.K_LEFT:
                    al.ui.left = False