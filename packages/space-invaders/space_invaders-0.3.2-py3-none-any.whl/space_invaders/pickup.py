import copy
import pygame
from pygame.locals import USEREVENT
import space_invaders.spaceship as spaceship
import space_invaders.config as config


class Pickup(pygame.sprite.Sprite):
    """Represents objects that the player can pick up and gain bonuses from them"""
    def __init__(self, action, args, image=None, image_file=""):
        """
        Make sure that the use of image or image_file is required, at least one of them has to be given, if both given
        the image will be used
        @param action a static function selected from this class given in as callback function that is executed when
        the player picks up this object
        @param args a list of arguments that are passed in for the callback function
        @param image a pygame Surface (image) that can is cloned and used as image, by default it is null
        @param image_file the source of an image file that is used as image for the object
        """
        super().__init__()

        if image is not None:
            self._image = image
        else:
            self._image = pygame.image.load(image_file)

        self._rect = self._image.get_rect()
        self._action = action
        self._args = args

    def new_pickup(self):
        """
        Creates a new instance of the same object, but with new references
        @return: the new object
        """
        return Pickup(action=self._action, args=self._args, image=copy.copy(self._image))

    def move(self, vec):
        """
        Moves the Pickup to the given position
        @param vec the new position of the pickup (2D tuple)
        """
        self._rect.center = (self._rect.center[0] + vec[0], self._rect.center[1] + vec[1])

    def render(self, window):
        """
        Renders the pickup onto the window
        @param window The surface where you want the Pickup to be rendered
        """
        window.blit(self._image, (self._rect.center[0] - self._rect.width//2,
                                  self._rect.center[1] - self._rect.height//2))

    @property
    def collider(self):
        """@return: the bounding rect of the image of this pickup"""
        return self._rect

    @property
    def image(self):
        """@return: the image of this pickup"""
        return self._image

    @property
    def position(self):
        """@return: position of this pickup (center)"""
        return self._rect.center

    @position.setter
    def position(self, vec):
        """
        sets the center to the given vector
        @param vec the new center position
        """
        self._rect.center = vec

    @property
    def action(self):
        """@return: the action of this pickup"""
        return self._action

    @property
    def args(self):
        """@return: the arguments for the action of this pickup"""
        return self._args

    @staticmethod
    def action_heal(entity, amount):
        """
        Calls the given entity's heal method with the given amount
        @param entity the entity
        @param amount the healed amount
        """
        entity.heal(amount)

    @staticmethod
    def action_give_gun(entity, gun):
        """
        Calls the given entity's add_ammo method with the given gun constant
        @param entity the entity
        @param gun the given gun constant, selected from spaceship module
        """
        entity.add_ammo(gun.new_gun())

    @staticmethod
    def action_give_life(entity):
        """
        Calls the given entity's give_life method
        @param entity the entity
        """
        entity.add_life()

    @staticmethod
    def action_fire_rate_boost(entity, multiplier, duration):
        """
        Sets the given entity's fire_rate_multiplier to the given multiplier, then starts a reset timer
        that triggers a RESET_FIRE_RATE event after the time duration
        @param entity the entity
        @param multiplier the multiplier that is applied (the smaller, the faster)
        @param duration the length of the effect
        """
        entity.set_fire_rate_multiplier(multiplier)
        pygame.time.set_timer(RESET_FIRE_RATE, duration)

    @staticmethod
    def action_reset_fire_rate(entity):
        """
        Sets the entity's fire_rate_multiplier back to 1
        """
        entity.set_fire_rate_multiplier(1)


RESET_FIRE_RATE = USEREVENT + 1

"""
The constant Pickup objects used as samples for pickup instantiation
"""
PICKUP_REPAIR = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "repair.png"),
    args=[1000000]
)
PICKUP_SMALL_HEAL = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "small_heal.png"),
    args=[5]
)
PICKUP_MEDIUM_HEAL = Pickup(
    action=Pickup.action_heal,
    image_file=config.get_path("Sprites", "medium_heal.png"),
    args=[10]
)
# Only for technical purposes, it is not spawned at all tho
PICKUP_DEFAULT_GUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "default_gun_pickup.png"),
    args=[spaceship.DEFAULT_GUN]
)
PICKUP_MINIGUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "minigun_pickup.png"),
    args=[spaceship.MINIGUN]
)
PICKUP_ROCKET_GUN = Pickup(
    action=Pickup.action_give_gun,
    image_file=config.get_path("Sprites", "rocket_gun_pickup.png"),
    args=[spaceship.ROCKET_GUN]
)
PICKUP_LIFE = Pickup(
    action=Pickup.action_give_life,
    image_file=config.get_path("Sprites", "life.png"),
    args=[]
)
PICKUP_FIRE_RATE_BOOSTER = Pickup(
    action=Pickup.action_fire_rate_boost,
    image_file=config.get_path("Sprites", "fire_rate_booster.png"),
    args=[0.5, 5000]
)
