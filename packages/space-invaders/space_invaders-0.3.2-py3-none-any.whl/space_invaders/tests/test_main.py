import unittest
import pygame
from space_invaders.main import get_pickup_image_by_gun, check_entity_collision
from space_invaders.entity import Entity, Enemy
from space_invaders.spaceship import DEFAULT_GUN, MINIGUN, ROCKET_GUN, DEFAULT_SHIP, DEFAULT_ENEMY_SHIP
from space_invaders.pickup import PICKUP_ROCKET_GUN, PICKUP_MINIGUN, PICKUP_DEFAULT_GUN


class TestMain(unittest.TestCase):
    """ Only a couple of methods are tested since for the test of the rest
        I would basically have to recreate the entire game here as tests
        OR alternatively just mock everything which at that point wouldn't test anything """

    def test_get_pickup_image_by_gun(self):
        self.assertEqual(get_pickup_image_by_gun(DEFAULT_GUN), PICKUP_DEFAULT_GUN.image,
                         "Incorrect image for Default Gun")
        self.assertEqual(get_pickup_image_by_gun(MINIGUN), PICKUP_MINIGUN.image, "Incorrect image for Minigun")
        self.assertEqual(get_pickup_image_by_gun(ROCKET_GUN), PICKUP_ROCKET_GUN.image, "Incorrect image for Rocket Gun")

    def test_check_entity_collision(self):
        player = Entity(DEFAULT_SHIP, (100, 100), 15, 1, False)
        enemies = [Enemy(DEFAULT_ENEMY_SHIP, (100, 100), 5, []), Enemy(DEFAULT_ENEMY_SHIP, (1500, 100), 5, [])]

        player_target_hp = max(0, player.hp - enemies[0].hp)
        hit_enemy_target_hp = max(0, enemies[0].hp - player.hp)
        not_hit_enemy_target_hp = enemies[1].hp

        pygame.init()
        pygame.mixer.init()
        check_entity_collision(player, enemies)
        pygame.quit()

        self.assertEqual(player.hp, player_target_hp, "The player's hp was incorrectly set after the collision")
        self.assertEqual(enemies[0].hp, hit_enemy_target_hp, "The enemy that we collided with, "
                                                             "had his hp incorrectly modified")
        self.assertEqual(enemies[1].hp, not_hit_enemy_target_hp, "We didn't hit the enemy, but his hp was decreased")
