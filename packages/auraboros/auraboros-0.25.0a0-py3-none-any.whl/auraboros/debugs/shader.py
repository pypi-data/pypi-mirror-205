from pathlib import Path
# from array import array
import sys

import pygame
# import moderngl

import init_for_dev  # noqa
from auraboros import engine
from auraboros.animation import AnimationImage, SpriteSheet, AnimationImageDict
from auraboros.entity import Entity
from auraboros.gameinput import Keyboard
from auraboros.gamescene import Scene, SceneManager
from auraboros.shader import Shader2D, VERTEX_DEFAULT
from auraboros.utilities import Arrow, AssetFilePath, draw_grid

engine.init(pixel_scale=1, set_mode_flags=pygame.DOUBLEBUF | pygame.OPENGL)

AssetFilePath.set_asset_root(Path(sys.argv[0]).parent / "assets")


class EntityIdle(AnimationImage):
    def __init__(self):
        super().__init__()
        self.sprite_sheet = SpriteSheet(AssetFilePath.img("testsprite.png"))
        self.anim_frames: list[pygame.surface.Surface] = [
            self.sprite_sheet.image_by_area(0, 0, 32, 32),
            self.sprite_sheet.image_by_area(0, 32, 32, 32),
            self.sprite_sheet.image_by_area(0, 32*2, 32, 32),
            self.sprite_sheet.image_by_area(0, 32*3, 32, 32),
            self.sprite_sheet.image_by_area(0, 32*4, 32, 32),
            self.sprite_sheet.image_by_area(0, 32*3, 32, 32),
            self.sprite_sheet.image_by_area(0, 32*2, 32, 32),
            self.sprite_sheet.image_by_area(0, 32, 32, 32)]
        self.anim_interval = 75
        self.loop_count = -1


class TestEntity(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.animation = AnimationImageDict()
        self.animation["idle"] = EntityIdle()
        self.animation["idle"].seek(self.animation["idle"].frame_num//4)
        self.image = self.animation["idle"].image
        self.rect = self.image.get_rect()
        self.movement_speed = 2

    def update(self):
        self.move_by_arrow()
        if self.is_moving:
            self.animation["idle"].let_play()
            self.image = self.animation["idle"].image
        else:
            self.animation["idle"].let_stop()


class DebugScene(Scene):
    def setup(self):
        # super().__init__(*args, **kwargs)
        self.testentity = TestEntity()
        self.testentity.set_x_to_center_of_screen()
        self.testentity.set_y_to_center_of_screen()
        self.keyboard["player"] = Keyboard()
        self.keyboard["player"].register_keyaction(
            pygame.K_LEFT, 0, 0, 0,
            lambda: self.testentity.set_move_direction(Arrow.LEFT),
            lambda: self.testentity.cancel_move_direction(Arrow.LEFT))
        self.keyboard["player"].register_keyaction(
            pygame.K_UP, 0, 0, 0,
            lambda: self.testentity.set_move_direction(Arrow.UP),
            lambda: self.testentity.cancel_move_direction(Arrow.UP))
        self.keyboard["player"].register_keyaction(
            pygame.K_RIGHT, 0, 0, 0,
            lambda: self.testentity.set_move_direction(Arrow.RIGHT),
            lambda: self.testentity.cancel_move_direction(Arrow.RIGHT))
        self.keyboard["player"].register_keyaction(
            pygame.K_DOWN, 0, 0, 0,
            lambda: self.testentity.set_move_direction(Arrow.DOWN),
            lambda: self.testentity.cancel_move_direction(Arrow.DOWN))
        self.keyboard.set_current_setup("player")
        shader2d = Shader2D()
        with open(Path(sys.argv[0]).parent / "vignette.frag", "r") as f:
            vignette_frag = f.read()
        shader2d.compile_and_register_program(
            VERTEX_DEFAULT,
            vignette_frag, "vignette")
        shader2d.set_uniform("vignette", "radius", 0.67)
        shader2d.set_uniform("vignette", "softness", 0.33)

    def update(self, dt):
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_LEFT)
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_UP)
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_RIGHT)
        self.keyboard.current_setup.do_action_on_keyinput(pygame.K_DOWN)
        self.testentity.update()

    def draw(self, screen):
        draw_grid(screen, 32, (178, 178, 178))
        self.testentity.draw(screen)


scene_manager = SceneManager()
scene_manager.push(DebugScene(scene_manager))

if __name__ == "__main__":
    engine.run(scene_manager=scene_manager)
