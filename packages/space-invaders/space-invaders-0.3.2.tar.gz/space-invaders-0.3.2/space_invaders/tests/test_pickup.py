import unittest
from space_invaders.pickup import Pickup
from space_invaders import config


class TestPickup(unittest.TestCase):
    def test_pickup1(self):
        target_args = [1000000]
        p = Pickup(
            action=Pickup.action_heal,
            image_file=config.get_path("Sprites", "repair.png"),
            args=target_args
        )

        self.assertEqual(p.action, Pickup.action_heal, "Wrong pickup action set in constructor")
        self.assertEqual(p.args, target_args, "Wrong arguments were passed in (args)")

        p.position = (50, 50)
        self.assertEqual(p.position[0], 50, "Wrong x position set in setter")
        self.assertEqual(p.position[1], 50, "Wrong x position set in setter")

        for i, arg in enumerate(target_args):
            self.assertEqual(arg, p.args[i], f"Argument mismatch at index {i} (args)")

    def test_pickup2(self):
        target_args = []
        p = Pickup(
            action=Pickup.action_give_life,
            image_file=config.get_path("Sprites", "life.png"),
            args=target_args
        )

        self.assertEqual(p.action, Pickup.action_give_life, "Wrong pickup action set in constructor")
        self.assertEqual(p.args, target_args, "Wrong arguments were passed in (args)")

        p.position = (50, 50)
        self.assertEqual(p.position[0], 50, "Wrong x position set in setter")
        self.assertEqual(p.position[1], 50, "Wrong x position set in setter")
