import pygame

from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT


class Entity(pygame.sprite.Sprite):
    """
    Represents an entity in the game, each entity is a special Sprite which features are not really used,
    but it is kept in order to help adding features in the future
    """
    def __init__(self, ship, spawn_position, speed, lives=1, looks_down=True):
        """
        @param ship a ship constant from the spaceship module
        @param spawn_position the 2D position where we spawn the entity
        @param speed the movement speed of the entity
        @param lives the number of lives the entity has, by default it's 1
        @param looks_down True if the entity should shoot/look downwards on the screen
        """
        super().__init__()
        self._ship = ship.new_ship()
        self._hp = ship.hp
        self._max_hp = ship.hp
        self._lives = lives
        self._speed = speed
        self._ship.looks_down = looks_down
        self._ship.set_position(spawn_position)

    def render(self, window, show_colliders):
        """
        Calls the ship's render method with the same parameters.
        @param window the window where we want to render our entity
        @param show_colliders whether to display colliders on screen
        """
        self._ship.render(window, show_colliders)

    def check_projectile_hit(self, enemies):
        """
        Calls the ship's check projectile_hit method
        @param enemies the array of enemies that if the projectile intersects with it explodes
        """
        return self._ship.check_projectile_hit(enemies)

    def set_fire_rate_multiplier(self, multiplier):
        """
        Sets the ship's fire rate multiplier by calling the method of the self._ship
        @param multiplier the multiplier to apply on the fire rate (smaller the faster)
        @return: an array of explosion data that can be used to display explosions
        """
        self._ship.set_fire_rate_multiplier(multiplier)

    @property
    def collider(self):
        """
        @return: the entity's ship's collider (2d coordinate tuple array)
        """
        return self._ship.collider

    @property
    def image_rect(self):
        """
        @return: the entity's ship's image rect (pygame Rect object)
        """
        return self._ship.image_rect

    @property
    def hp(self):
        """
        @return: the entity's current hp
        """
        return self._hp

    @property
    def max_hp(self):
        """
        @return: the entity's maximum hp
        """
        return self._max_hp

    @property
    def speed(self):
        """
        @return: the entity's speed
        """
        return self._speed

    def in_bounds(self):
        """
        Checks if the player is within the window space
        @return: bool
        """
        position = self.ship.image_rect.center
        return 0 <= position[0] < WINDOW_WIDTH and 0 <= position[1] < WINDOW_HEIGHT

    def add_ammo(self, gun):
        """
        Passes the parameter to the ship's add_ammo method
        """
        self._ship.add_ammo(gun)

    def next_gun(self):
        """
        Calls the ship's next gun method which cycles the current gun to the next possible gun
        """
        if not self.alive():
            return

        self._ship.next_gun()

    def shoot(self):
        """
        Calls the ship's next gun method which cycles the current gun to the next possible gun
        """
        if not self.alive():
            return

        self._ship.shoot()

    def alive(self):
        """Checks if entity's health is greater than zero"""
        return self._hp > 0

    @property
    def ship(self):
        """Getter for the entity's ship"""
        return self._ship

    @property
    def lives(self):
        """Getter for the entity's number of lives"""
        return self._lives

    def add_life(self, amount=1):
        """Increases the entity's life count by the given amount"""
        if self.alive():
            self._lives = max(self._lives, self._lives + amount)

    def heal(self, amount):
        """Increases the entity's health by the given amount"""
        if self.alive() and amount > 0:
            self._hp = min(self._hp + amount, self._max_hp)

    def take_damage(self, amount):
        """Decreases the entity's health by the given amount"""
        if not self.alive() or not self.in_bounds() or amount <= 0:
            return

        self._hp = max(0, self._hp - amount)

        if self._hp == 0:
            self._lives -= 1
            if self._lives == 0:
                self.die()
            else:
                self._hp = self._max_hp

    def move(self, vec, clamp=True):
        """
        Moves the entity based on its speed and the
        @param vec which tells the direction
        @param clamp clamping the diagonal movement since it would be faster than any single axis move
        """
        if not self.alive():
            return

        # correcting diagonal speed
        if clamp and vec[0] != 0 and vec[1] != 0:
            diagonal_len = (vec[0] ** 2 + vec[1] ** 2) ** (1 / 2)
            vec = (vec[0] / diagonal_len, vec[1] / diagonal_len)

        vec = (vec[0] * self._speed, vec[1] * self._speed)
        self._ship.move(vec)

    def die(self):
        """Self destructs :("""
        del self


class Enemy(Entity):
    """A special Entity that has only 1 life and has a list of actions that it can perform"""
    def __init__(self, ship, spawn_position, speed, actions):
        """
        @param ship a ship constant from spaceship module
        @param spawn_position the 2D position of spawn given in a tuple
        @param speed the enemy's speed
        @param actions the array of actions that the enemy should conduct. An action is a tuple with the first parameter
        being a string, and a second parameter containing the arguments in a list
        """
        super().__init__(ship, spawn_position, speed, lives=1, looks_down=True)
        self._actions = actions

    def execute_next_action(self):
        """Executes the next action if there is next action in the actions array"""
        if len(self._actions) > 0:
            action = self._actions[0]
            match action[0]:
                case "shoot":
                    self.shoot()
                case "move":
                    self.move(action[1][0], clamp=False)
                case "move_fire":
                    self.shoot()
                    self.move(action[1][0], clamp=False)

            self._actions.remove(action)
