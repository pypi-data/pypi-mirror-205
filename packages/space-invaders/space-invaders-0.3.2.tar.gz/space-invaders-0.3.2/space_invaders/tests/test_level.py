import unittest
from space_invaders.level import Level, Phase, shoot_actions, initialize_global_arrays, PHASE_TRIANGLE_TRIO
from space_invaders.spaceship import DEFAULT_ENEMY_SHIP, DEFAULT_SHIP, MINIGUN


class TestLevel(unittest.TestCase):
    def test_phase(self):
        phs = Phase(
            [   # Spawned Enemy Ships
                DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
            ],
            [   # Spawn Positions
                (100, 100), (300, 100), (500, 100)
            ],  # Movement speed
            [5, 5, 5],
            [
                shoot_actions(),
                shoot_actions() + shoot_actions(),
                []
            ]
        )
        self.assertFalse(phs.initialized, "Haven't even initialized the phase, its true")
        self.assertFalse(phs.is_over(), "Haven't even initialized the phase, but its already over")

        initialize_global_arrays([], [])
        phs.initialize()
        self.assertTrue(phs.initialized, "Initialized returns wrong value after initialize()")
        self.assertFalse(phs.is_over(), "Shouldn't be over yet")

    def test_level(self):
        lvl = Level(
            [  # The phases of the level
                PHASE_TRIANGLE_TRIO.create_new()
            ],  # The ship constant of the player, player's spawn position, and player's movement speed
            DEFAULT_SHIP, (500, 514), 20,
            [  # Array of weapons that can be spawned to pick up, on the level
                # (default can't be spawned because it has infinite ammo)
                MINIGUN
            ],
            # The text shown at the start of the level: Title, text
            ("Level Test", "The Testing Level")
        )

        self.assertEqual(lvl.level_text, ("Level Test", "The Testing Level"), "The value of the level text was set "
                                                                              "inappropriately in the constructor")
        self.assertEqual(len(lvl.spawned_weapons), 1, "The number of spawn able weapons is incorrect")
        self.assertEqual(lvl.spawned_weapons[0], MINIGUN, "The spawn able weapons property is wrongly assigned")
        self.assertFalse(lvl.is_complete(), "There are still phases, so it should not be complete")

        initialize_global_arrays([], [])
        player = lvl.spawn_player()
        self.assertEqual(player.image_rect.center[0], 500, "X coordinate of spawn position is incorrect")
        self.assertEqual(player.image_rect.center[1], 514, "Y coordinate of spawn position is incorrect")
        self.assertEqual(player.speed, 20, "The speed of the spawned player is incorrect")

