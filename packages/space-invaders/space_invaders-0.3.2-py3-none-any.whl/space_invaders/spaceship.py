import copy
import pygame
from shapely.geometry import Polygon
import space_invaders.config as config


class Spaceship:
    """
    Represents spaceships with a weapon
    """
    def __init__(self, gun, hp, collider, enemy, image_file="", image=None):
        """
        Either the image_file or the image must be set, if both set, the image is used
        @param gun a gun constant chosen from spaceship module
        @param hp the health points that the ship has
        @param collider a list of 2D tuple points that describe the polygon collider of the ship, must be convex
        @param enemy True if the ship is an enemy ship, false otherwise
        @param image_file source of an image file used as image for the ship
        @param image a pygame Surface (image) that is copied to be the image of the ship
        """
        self._image = image if image is not None else pygame.image.load(image_file)
        self._guns = gun if isinstance(gun, list) else [gun]
        self._active_gun = 0
        self._hp = hp
        self._image_rect = self._image.get_rect()
        self._collider_relative_vertices = copy.copy(collider)
        self._collider = collider
        self._enemy = enemy
        self._fire_rate_multiplier = 1
        self._projectiles = []

    def new_ship(self):
        """
        Creates a new instance of this ship with the same data but new references
        @return: the new instance
        """
        shp = Spaceship([gun.new_gun() for gun in self._guns], self._hp, list(vertex for vertex in self._collider),
                        self._enemy, image=copy.copy(self._image))
        return shp

    def empty_projectiles(self):
        """Clears the projectiles list of the ship"""
        self._projectiles.clear()

    def add_ammo(self, gun):
        """
        Adds the gun to the gun collection of the ship, if already has a gun with the same type, then it adds the
        ammo count to the current ammo count
        @param gun a gun constant chosen from spaceship module
        """
        for checked in self._guns:
            if checked.type == gun.type:
                checked.add_ammo(gun.ammo)
                return
        self._guns.append(gun)

    def set_fire_rate_multiplier(self, multiplier):
        """@param multiplier the new multiplier, the smaller, the faster it shoots"""
        self._fire_rate_multiplier = multiplier

    def set_position(self, vec):
        """
        Sets the position of the ship to the given vector
        @param vec the new position (center)
        """
        self._image_rect.center = vec
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (vertex[0] + vec[0],
                                 vertex[1] + vec[1])
        for gun in self._guns:
            gun.set_position(vec)

    def move(self, vec):
        """
        Moves the ship by the given vector
        @param vec the move
        """
        self._image_rect.move_ip(vec[0], vec[1])
        for i, vertex in enumerate(self._collider_relative_vertices):
            self._collider[i] = (self._image_rect.center[0] + vertex[0],
                                 self._image_rect.center[1] + vertex[1])
        for gun in self._guns:
            gun.move(vec)

    def next_gun(self):
        """Cycles the selected gun to be the next available one"""
        self._active_gun += 1
        self._active_gun %= len(self._guns)
        self._guns[self._active_gun].set_position(self._image_rect.center)

    def shoot(self):
        """Creates a new projectile and stores it in the list of the ship's projectiles"""
        new_projectile = self._guns[self._active_gun].shoot(self._fire_rate_multiplier)
        if new_projectile is not None:
            self._projectiles.append(new_projectile)

    def render(self, window, show_colliders):
        """
        Renders the ship, its active gun and all its projectiles onto the given window
        @param window the Surface where you want it to be rendered
        @param show_colliders show the hitboxes, bounding boxes of the ship, projectiles, center of ship
        """
        self._guns[self._active_gun].render(window)
        window.blit(self._image, (self._image_rect.center[0] - self._image_rect.width//2,
                                  self._image_rect.center[1] - self._image_rect.height//2))
        self.render_projectiles(window, show_colliders)
        if show_colliders:
            pygame.draw.rect(window, (255, 255, 0), self._image_rect, 1)
            pygame.draw.circle(window, (255, 0, 0), self._image_rect.center, 3)
            pygame.draw.polygon(window, (255, 0, 255), self._collider, 1)

    def check_projectile_hit(self, enemies):
        """
        For each projectile in the list of projectile it checks if we have hit any of the enemies, if yes they all take
        damage and the projectile explodes and is removed from the list
        @param enemies an array of the enemies
        """
        explosions = []
        for projectile in self._projectiles:
            hit_count = 0
            p_poly = Polygon([projectile.collider.topleft, projectile.collider.topright,
                              projectile.collider.bottomright, projectile.collider.bottomleft])

            for enemy in enemies:
                enemy_poly = Polygon(enemy.collider)
                if p_poly.intersects(enemy_poly):
                    enemy.take_damage(projectile.damage)
                    hit_count += 1
                    if self._enemy:
                        config.score -= 15

            if hit_count > 0:
                config.play_sound(config.SOUND_PLAYER_HIT_DATA if self._enemy else config.SOUND_ENEMY_HIT_DATA, 0)
                self._projectiles.remove(projectile)
                explosions.append([pygame.image.load(config.get_path("Sprites", "explosion.png")),
                                   projectile.image_rect.center, config.EXPLOSION_DURATION])
        return explosions

    def check_projectiles(self):
        """Checks each projectile if it is still in play area and removes it if it is out"""
        for projectile in self._projectiles:
            projectile.move_forward(self._enemy)
            if projectile.check_if_out():
                self._projectiles.remove(projectile)
                del projectile

    def render_projectiles(self, window, show_colliders):
        """
        Renders each projectile onto the window
        @param window the surface where we render the projectiles
        @param show_colliders True if you want the bounding box to be visible
        """
        self.check_projectiles()
        for projectile in self._projectiles:
            projectile.render(window)
            if show_colliders:
                pygame.draw.rect(window, (255, 255, 0), projectile.image_rect, 1)
                pygame.draw.circle(window, (255, 0, 0), projectile.image_rect.center, 3)
                pygame.draw.rect(window, (255, 0, 255), projectile.collider, 1)

    @property
    def guns(self):
        """@return: the guns of the ship"""
        return self._guns

    @property
    def active_gun(self):
        """@return: the index of the active gun"""
        return self._active_gun

    @property
    def image(self):
        """@return: the image of the ship"""
        return self._image

    @property
    def hp(self):
        """@return: the hp of the ship"""
        return self._hp

    @property
    def image_rect(self):
        """@return: the ship's image bounding rect"""
        return self._image_rect

    @property
    def fire_rate_multiplier(self):
        """@return: the fire rate multiplier of the ship"""
        return self._fire_rate_multiplier

    @property
    def collider(self):
        """@return: the collider 'polygon' of the ship as 2D points"""
        return self._collider


class Gun:
    """A weapon that is mounted onto the ships, and can fire projectiles"""
    def __init__(self, fire_rate, projectile, ammo, left_muzzle, right_muzzle, offset,
                 gun_type="default", image=None, image_file=""):
        """
        One of the image and image_file parameters must be set, if both set, de image is used
        @param fire_rate the delay between shots in ms
        @param projectile a projectile constant chosen from the spaceship module
        @param ammo the amount of ammo it has by default, -1 means infinite
        @param left_muzzle the relative position of the left muzzle from the center
        @param right_muzzle the relative position of the right muzzle from the center
        @param offset the offset that is applied on the gun, would be used when reusing weapons on multiple ships,
        to fit them
        @param gun_type a string type that tells what type the gun is, by default it is 'default'
        @param image a pygame Surface (image) that is copied to be the image for the gun
        @param image_file the source of an image that is loaded in as image for the gun
        """
        self._image = image if image is not None else pygame.image.load(image_file)
        self._rect = self._image.get_rect()
        self._fire_rate = fire_rate
        self._projectile = projectile
        self._ammo = ammo
        self._left_muzzle = left_muzzle
        self._right_muzzle = right_muzzle
        self._offset = offset
        self._time_since_last_shot = 0
        self._type = gun_type

    def new_gun(self):
        """
        Creates a new instance of this gun with the same data but new references
        @return: the new instance
        """
        return Gun(self._fire_rate, self._projectile, self._ammo, self._left_muzzle, self._right_muzzle, self._offset,
                   image=copy.copy(self._image), gun_type=self._type)

    def set_position(self, vec):
        """
        Sets the position of the gun to be the given position + offset
        @param vec the new position
        """
        self._rect.center = (vec[0] + self._offset[0], vec[1] + self._offset[1])

    def move(self, vec):
        """
        Moves the gun by the given amount
        @param vec the moved 2D vecter
        """
        self._rect.move_ip(vec[0], vec[1])

    def render(self, window):
        """
        Renders the gun onto the given Surface
        @param window the pygame Surface
        """
        window.blit(self._image, (self._rect.center[0] - self._rect.width//2,
                                  self._rect.center[1] - self._rect.height//2))

    @property
    def image(self):
        """@return: the image of the gun"""
        return self._image

    @property
    def type(self):
        """@return: the type of the gun"""
        return self._type

    @property
    def rect(self):
        """@return: the bounding rect of the gun's image"""
        return self._rect

    @property
    def ammo(self):
        """@return: the ammo count of the gun"""
        return self._ammo

    def add_ammo(self, amount):
        """
        Adds the given amount to the gun's ammo count
        @param amount the added amount
        """
        self._ammo += max(0, amount)

    def shoot(self, fire_rate_multiplier):
        """
        Shoots a projectile if the current time is greater thant the time_we_last_shot + fire_rate * multiplier
        @param fire_rate_multiplier the amount that the fire_rate is multiplied by
        @return: the new projectile if it shot, else None
        """
        current_time = pygame.time.get_ticks()

        if self._ammo != 0 and current_time - self._time_since_last_shot > self._fire_rate * fire_rate_multiplier:
            config.play_sound(get_sound_by_projectile(self._projectile), 0)
            projectile = self.spawn_projectile(self._left_muzzle if self._ammo % 2 == 0 else self._right_muzzle)
            self._ammo -= 1
            self._time_since_last_shot = current_time
            return projectile
        return None

    def spawn_projectile(self, relative_position):
        """
        Creates a new projectile at center_of_gun + relative_position
        @param relative_position the offset from the center of the gun
        @return: the new projectile
        """
        position = (self._rect.center[0] + relative_position[0],
                    self._rect.center[1] + relative_position[1])

        new_projectile = self._projectile.new_projectile()
        new_projectile.set_position(position)
        return new_projectile


class Projectile:
    """Represents projectiles that can be shot, move with a given speed until they hit enemies and explode"""
    def __init__(self, collider, damage, speed, image_file="", image=None):
        """
        One of the image_file, image parameters must be set. If both set, the image is used.
        @param collider the bounding polygon collider passed in as 2D coordinates
        @param damage the amount of damage delt if it hits enemies
        @param speed the speed of the projectile
        @param image_file source of an image file used as image for the projectile
        @param image a pygame Surface (image) that is copied to be the image of the projectile
        """
        self._image = image if image is not None else pygame.image.load(image_file)
        self._image_rect = self._image.get_rect()
        self._collider = collider
        self._damage = damage
        self._speed = speed

    def set_position(self, position):
        """
        Sets the position of the projectile to bet the given position (center)
        @param position the new center
        """
        self._collider.center = position
        self._image_rect.center = position

    def new_projectile(self):
        """
        Creates a new instance of this projectile with same data but new references
        @return: the new instance
        """
        return Projectile(copy.copy(self._collider), self._damage, self._speed, image=copy.copy(self._image))

    @property
    def speed(self):
        """@return: the speed of the projectile"""
        return self._speed

    @property
    def damage(self):
        """@return: the damage of the projectile"""
        return self._damage

    @property
    def image(self):
        """@return: the image of the projectile"""
        return self._image

    @property
    def image_rect(self):
        """@return: the image bounding rect of the projectile"""
        return self._image_rect

    @property
    def collider(self):
        """@return: the collider of the projectile as list of 2D points"""
        return self._collider

    def render(self, window):
        """
        Renders the projectile onto the given Surface
        @param window the surface
        """
        window.blit(self._image, (self._image_rect.center[0] - self._image_rect.width//2,
                                  self._image_rect.center[1] - self._image_rect.height//2))

    def move_forward(self, enemy):
        """
        Moves the projectile up downwards if it's an enemy projectile else it moves upwards
        """
        diff = self._speed if enemy else -self._speed
        self._collider.center = (self._collider.center[0], self._collider.center[1] + diff)
        self._image_rect.center = (self._image_rect.center[0], self._image_rect.center[1] + diff)

    def check_if_out(self):
        """@return: True if the projectile is further outside than 100 units away from the screen's top or bottom"""
        return self._collider.bottom < -100 or self._collider.top > config.WINDOW_HEIGHT + 100


def get_sound_by_projectile(projectile):
    """
    Return a config sound_data constant based on the type of the projectile
    @param projectile the projectile
    @return: a config sound_data constant
    """
    global DEFAULT_PROJECTILE, DEFAULT_ENEMY_PROJECTILE, MINIGUN_PROJECTILE, ROCKET_PROJECTILE
    if projectile in (DEFAULT_PROJECTILE, DEFAULT_ENEMY_PROJECTILE):
        return config.SOUND_DEFAULT_GUN_DATA
    if projectile == MINIGUN_PROJECTILE:
        return config.SOUND_MINIGUN_DATA
    return config.SOUND_ROCKET_DATA


"""
The constants below define samples for different types of projectiles, guns, and ships
These constants are used to instantiate new projectiles, guns, ships with the same parameters
"""
DEFAULT_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 30, 60), 2, 20, image_file=config.get_path("Sprites", "default_projectile.png")
)
DEFAULT_GUN = Gun(
    170, DEFAULT_PROJECTILE, -1,
    (-58, -55), (58, -55), (0, 0),
    image_file=config.get_path("Sprites", "default_gun.png")
)
DEFAULT_SHIP_collider = [
    (-100, -50), (-20, -100), (20, -100), (99, -50), (99, 80), (60, 99), (-60, 99), (-100, 80)
]
DEFAULT_SHIP = Spaceship(
    DEFAULT_GUN, 25, DEFAULT_SHIP_collider, False, image_file=config.get_path("Sprites", "default_ship.png")
)

MINIGUN_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 15, 35), 1, 20, image_file=config.get_path("Sprites", "minigun_projectile.png")
)
MINIGUN = Gun(
    60, MINIGUN_PROJECTILE, 140,
    (-58, -55), (58, -55), (0, 0),
    gun_type="minigun", image_file=config.get_path("Sprites", "minigun.png")
)

ROCKET_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 50, 50), 10, 22, image_file=config.get_path("Sprites", "rocket_projectile.png")
)
ROCKET_GUN = Gun(
    300, ROCKET_PROJECTILE, 15,
    (-58, -55), (58, -55), (0, 0),
    gun_type="rocket", image_file=config.get_path("Sprites", "rocket_gun.png")
)

DEFAULT_ENEMY_PROJECTILE = Projectile(
    pygame.Rect(0, 0, 20, 40), 1, 22, image_file=config.get_path("Sprites", "default_enemy_projectile.png")
)
DEFAULT_ENEMY_GUN = Gun(
    250, DEFAULT_ENEMY_PROJECTILE, -1,
    (-20, 50), (20, 50), (0, 0),
    image_file=config.get_path("Sprites", "default_enemy_gun.png")
)
DEFAULT_ENEMY_SHIP_collider = [
    (-90, -80), (-60, -100), (60, -100), (90, -80), (99, 0), (90, 80), (60, 99), (-60, 99), (-80, 90), (-100, 0)
]
DEFAULT_ENEMY_SHIP = Spaceship(
    DEFAULT_ENEMY_GUN, 10, DEFAULT_ENEMY_SHIP_collider, True,
    image_file=config.get_path("Sprites", "default_enemy_ship.png")
)
