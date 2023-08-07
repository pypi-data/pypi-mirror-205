import unittest
from space_invaders.spaceship import DEFAULT_SHIP, DEFAULT_ENEMY_SHIP
from space_invaders.entity import Entity, Enemy


class TestEntity(unittest.TestCase):
    def test_entity_constructor(self):
        ent = Entity(DEFAULT_SHIP.new_ship(), (100, 150), 1, 2, True)

        self.assertTrue(ent.in_bounds(), "The in_bounds is faulty")
        self.assertEqual(ent.speed, 1, "Entity speed is not set correctly")
        self.assertEqual(ent.lives, 2, "Entity lives is not set correctly")
        self.assertEqual(ent.hp, DEFAULT_SHIP.hp, "Entity hp is not set correctly")
        self.assertEqual(ent.max_hp, DEFAULT_SHIP.hp, "Entity max_hp is not set correctly")

    def test_entity_move(self):
        ent = Entity(DEFAULT_SHIP.new_ship(), (100, 150), 1, 2, True)

        ent.move((100, 0))
        ent.move((0, 200))
        self.assertEqual(ent.image_rect.center[0], 200, "X coordinate changes incorrectly after move")
        self.assertEqual(ent.image_rect.center[1], 350, "Y coordinate changes incorrectly after move")
        self.assertTrue(ent.in_bounds(), "In-bounds is not updated after move / faulty")

        ent.move((100, 200))
        self.assertEqual(ent.image_rect.center[0], 200, "Shouldn't be able to move while dead")
        self.assertEqual(ent.image_rect.center[1], 350, "Shouldn't be able to move while dead")

    def test_entity_hp_actions(self):
        ent = Entity(DEFAULT_SHIP.new_ship(), (100, 150), 1, 2, True)

        ent.take_damage(10)
        self.assertEqual(ent.hp, DEFAULT_SHIP.hp - 10, "Entity take_damage is faulty")
        self.assertEqual(ent.max_hp, DEFAULT_SHIP.hp, "Entity max_hp shouldn't decrease when taking damage")

        prev_hp = ent.hp
        ent.heal(-1)
        self.assertEqual(ent.hp, prev_hp, "Shouldn't be able to heal with -1 hp")
        ent.heal(500)
        self.assertEqual(ent.hp, DEFAULT_SHIP.hp, "Shouldn't be able to overheal your max_hp / incorrect heal amount")

        ent.take_damage(ent.hp)
        self.assertEqual(ent.lives, 1, "The number of lives doesn't decrease properly")
        self.assertEqual(ent.hp, DEFAULT_SHIP.hp, "Hp is not recharged after life loss")
        self.assertTrue(ent.alive(), "Shouldn't be dead with 1 life")

        ent.add_life(-1)
        self.assertEqual(ent.lives, 1, "Shouldnt be able to add -1 life")

        ent.take_damage(ent.ship.hp)
        self.assertEqual(ent.lives, 0, "The number of lives is not properly updated")
        self.assertEqual(ent.hp, 0, "Shouldn't recharge hp when the entity is dead")
        self.assertFalse(ent.alive(), "Shouldn't live with 0 hp")

        ent.add_life(1)
        self.assertEqual(ent.lives, 0, "Shouldnt be able to add lives after dying")

        ent = Entity(DEFAULT_SHIP, (100, 150), 1, 2, True)
        ent.add_life(2)
        self.assertEqual(ent.lives, 4, "Incorrect number of lives was added")

    def test_enemy_constructor(self):
        ent = Enemy(DEFAULT_ENEMY_SHIP.new_ship(), (-500, 150), 1, [])

        self.assertFalse(ent.in_bounds(), "The in_bounds is faulty")
        self.assertEqual(ent.speed, 1, "Enemy speed is not set correctly")
        self.assertEqual(ent.lives, 1, "Enemy lives is not set correctly")
        self.assertEqual(ent.hp, DEFAULT_ENEMY_SHIP.hp, "Enemy hp is not set correctly")
        self.assertEqual(ent.max_hp, DEFAULT_ENEMY_SHIP.hp, "Enemy max_hp is not set correctly")