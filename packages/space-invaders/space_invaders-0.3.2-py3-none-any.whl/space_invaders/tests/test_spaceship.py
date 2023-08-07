import unittest

import pygame

from space_invaders import config
from space_invaders.spaceship import Spaceship, DEFAULT_GUN, MINIGUN, ROCKET_GUN, Gun, DEFAULT_PROJECTILE, Projectile
from space_invaders.config import get_path


class TestSpaceship(unittest.TestCase):
    def test_spaceship_guns(self):
        ship = Spaceship(DEFAULT_GUN.new_gun(), 100, [(0, 0), (100, 0), (100, 100), (0, 100)],
                         False, image_file=get_path("Sprites", "default_ship.png"))
        self.assertEqual(len(ship.guns), 1, "Wrong []guns length")

        ship.add_ammo(MINIGUN.new_gun())
        self.assertEqual(len(ship.guns), 2, "Wrong []guns length")

        ship.add_ammo(ROCKET_GUN.new_gun())
        self.assertEqual(len(ship.guns), 3, "Wrong []guns length")

        ship.add_ammo(MINIGUN.new_gun())
        self.assertEqual(len(ship.guns), 3, "Wrong []guns length")
        self.assertEqual(ship.guns[1].ammo, MINIGUN.ammo * 2, "Wrong rocket ammo amount added")

        self.assertEqual(ship.active_gun, 0, "Wrong active gun index")
        ship.next_gun()
        self.assertEqual(ship.active_gun, 1, "Wrong active gun index after next_gun")
        ship.next_gun()
        self.assertEqual(ship.active_gun, 2, "Wrong active gun index after next_gun")
        ship.next_gun()
        self.assertEqual(ship.active_gun, 0, "Wrong active gun index after reaching the end with next_gun")

    def test_gun(self):
        gun = Gun(100, DEFAULT_PROJECTILE.new_projectile(), 15, (0, 0), (0, 0), (15, 23),
                  image_file=get_path("Sprites", "default_gun.png"))
        self.assertEqual(gun.type, "default", "Incorrect type set if not given as argument")
        self.assertEqual(gun.ammo, 15, "Incorrect ammo amount was set in the constructor")

        gun.set_position((10, 10))
        self.assertEqual(gun.rect.center[0], 25, "x coordinate not set properly in set position")
        self.assertEqual(gun.rect.center[1], 33, "y coordinate not set properly in set position")

        gun.move((1, 1))
        self.assertEqual(gun.rect.center[0], 26, "x coordinate not set properly in move")
        self.assertEqual(gun.rect.center[1], 34, "y coordinate not set properly in move")

    def test_projectile(self):
        proj = Projectile(
            pygame.Rect(0, 0, 30, 60), 2, 20, image_file=config.get_path("Sprites", "default_projectile.png")
        )
        self.assertEqual(proj.damage, 2, "Incorrect damage amount for the projectile")
        self.assertEqual(proj.speed, 20, "Incorrect speed amount for the projectile")

        proj.set_position((50, 52))
        self.assertEqual(proj.image_rect.center[0], 50, "x coordinate not set properly in set position")
        self.assertEqual(proj.image_rect.center[1], 52, "y coordinate not set properly in set position")

        prev_pos = proj.image_rect.center
        for i in range(12):
            proj.move_forward(False)
            self.assertEqual(proj.image_rect.center[0], prev_pos[0], "x coordinate not set properly in set position")
            self.assertEqual(proj.image_rect.center[1], prev_pos[1] - 20, "y coordinate set wrong in set position")
            prev_pos = proj.image_rect.center
            if proj.collider.bottom < -100:
                self.assertTrue(proj.check_if_out(), f"Projectile is out, should return True")
            else:
                self.assertFalse(proj.check_if_out(), "Projectile is in, should return False")
