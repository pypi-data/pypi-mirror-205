import copy
from math import log2
from space_invaders.entity import Entity, Enemy
import space_invaders.spaceship as spaceship
from space_invaders.spaceship import DEFAULT_ENEMY_SHIP, DEFAULT_SHIP
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT


class Phase:
    """This class represents a phase of a level, which is basically a list of enemies and their actions"""
    def __init__(self, phase_enemies, positions, speeds, actions):
        """
        @param phase_enemies a list of enemy constants
        @param positions their spawn positions as a collection of tuples
        @param speeds the movement speed for each enemy in a list
        @param actions a list of lists, that contain the actions done by the enemies in the phase
        """
        self._enemy_ships = phase_enemies
        self._positions = positions
        self._initialized = False
        self._actions = copy.deepcopy(actions)
        self._speeds = speeds
        self._enemies = []

    @property
    def initialized(self):
        """@return: whether the phase has already been initialized or not"""
        return self._initialized

    def initialize(self):
        """Initializes the phase: spawns the enemies and adds them to the phase's enemies array"""
        for i in range(len(self._enemy_ships)):
            added_enemy = spawn_entity(self._enemy_ships[i], self._positions[i], self._speeds[i], self._actions[i])
            if added_enemy is not None:
                self._enemies.append(added_enemy)

        self._initialized = True

    def create_new(self):
        """Creates a new Phase object using this object's data with new references"""
        return Phase(self._enemy_ships, self._positions, self._speeds, copy.deepcopy(self._actions))

    def execute_all_actions(self):
        """Executes the next action for all the enemies in the phase, but only if they are alive and haven't
        left the window's bottom. Those are removed from the phase"""
        for enemy in self._enemies:
            if enemy.alive() and enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                enemy.execute_next_action()
            else:
                self._enemies.remove(enemy)

    def is_over(self):
        """@return: True if all the phase enemies are dead or left the window, else it's false"""
        if self._initialized:
            if len(enemies) == 0:
                return True
            for enemy in enemies:
                if enemy.image_rect.center[1] < WINDOW_HEIGHT + 100:
                    return False
            return True
        return False


class Level:
    """This class represents the levels of the game"""
    def __init__(self, phases, player_ship, player_spawn_position, player_speed, spawned_weapons, level_text):
        """
        @param phases the phase constants given as a list, phase constants are in the level module
        @param player_ship a ship constant that tells what ship the player plays with on the level, chosen
        from the spaceship module
        @param player_spawn_position the start position of the player on the level
        @param player_speed the movement speed of the player
        @param spawned_weapons a list of weapon constants from the spaceship module, tells which of the non default
        weapons can be spawned on the level as pickups
        @param level_text the text that is displayed at the start of the level, tuple(Title, BottomText)
        """
        self._phases = phases
        self._player_ship = player_ship
        self._player_spawn_position = player_spawn_position
        self._player_speed = player_speed
        self._spawned_weapons = spawned_weapons
        self._level_text = level_text

    @property
    def level_text(self):
        """@return: the text of the level"""
        return self._level_text

    @property
    def spawned_weapons(self):
        """@return: the spawn able weapons of the level"""
        return self._spawned_weapons

    @property
    def player_spawn_position(self):
        """@return: the player's spawn position"""
        return self._player_spawn_position

    def create_new(self):
        """@return: A new Level object with the same data as this object but different references"""
        new_phases = [phase.create_new() for phase in self._phases]
        return Level(new_phases, self._player_ship, self._player_spawn_position,
                     self._player_speed, self._spawned_weapons, self._level_text)

    def spawn_player(self):
        """spawns the player @return: the spawned entity object"""
        return spawn_entity(self._player_ship, self._player_spawn_position, self._player_speed)

    def execute_phase(self):
        """Executes the phases of the level, until there is none left"""
        if not self.is_complete():
            if not self._phases[0].initialized:
                self._phases[0].initialize()

            if self._phases[0].is_over():
                self._phases.remove(self._phases[0])
            else:
                self._phases[0].execute_all_actions()

    def is_complete(self):
        """@return: True if there are phases left, False otherwise"""
        return len(self._phases) == 0


def shoot_actions(duration_in_seconds=1/60):
    """
    Generates a list of shooting actions in the tuple(action: str, args: list) format
    @param duration_in_seconds the duration of the shooting
    @return: the list of actions
    """
    return [("shoot", [])] * int(60 * duration_in_seconds)


def go_towards_actions(position, target, speed, fire=False):
    """
    Generates a list of moving actions in the tuple(action: str, args: list) format
    The movement is smoothed out by applying log2
    @param position the current position, from which you want to get to the target position
    @param target the target position
    @param speed the speed that the entity moves with
    @param fire True if you want the entity to fire while moving, False otherwise
    @return: the list of actions in the format above
    """
    actions = []
    while abs(position[0] - target[0]) > 0.01 or abs(position[1] - target[1]) > 0.01:
        diff = (target[0] - position[0], target[1] - position[1])
        ease_x = ease_y = move_x = move_y = 0

        if diff[0] < 0:
            ease_x = min(1.0, log2(abs(diff[0])))
            move_x = max(diff[0] / speed, -1.0)
        elif diff[0] > 0:
            ease_x = min(1.0, log2(diff[0]))
            move_x = min(diff[0] / speed, 1.0)

        if diff[1] < 0:
            ease_y = min(1.0, log2(abs(diff[1])))
            move_y = max(diff[1] / speed, -1.0)
        elif diff[1] > 0:
            ease_y = min(1.0, log2(diff[1]))
            move_y = min(diff[1] / speed, 1.0)

        move = ("move_fire" if fire else "move", [(move_x * ease_x, move_y * ease_y)])
        actions.append(move)
        position = (position[0] + move_x * speed, position[1] + move_y * speed)
    return actions


initialized_arrays = False
enemies, entities = [], []


def initialize_global_arrays(entities_array, enemies_array):
    """
    Sets the global constants defined in the level module equal to the inputs
    @param entities_array the entities array containing all entities that are alive
    @param enemies_array the enemies array containing all enemies that are alive
    """
    global entities, enemies, initialized_arrays
    entities, enemies = entities_array, enemies_array
    initialized_arrays = True


def spawn_entity(ship, position, speed, actions=None):
    """
    If the global arrays are initialized, the function creates a new entity with the given parameters and
    adds it to the appropriate global arrays.
    @param ship the ship constant selected for the entity, chosen from spaceship module
    @param position the spawn position
    @param speed the movement speed
    @param actions the actions that the entity performs. if its None then it's a player entity else an Enemy
    @return: the created entity
    """
    if initialized_arrays:
        if actions is None:
            player = Entity(ship, position, speed)
            entities.append(player)
            return player
        else:
            enemy = Enemy(ship, position, speed, actions)
            entities.append(enemy)
            enemies.append(enemy)
            return enemy


"""
The Phase and Level constant objects below define what happens in the different phases, levels
They serve as samples that can be used to create new instances with their data
--Beware that the additions seen below between function returns is list concatenation
The first phase, level constants are commented for easier understanding
"""
# Phase Constant Objects, used to create new instances of the phase type
PHASE_TOKYO_DRIFT = Phase(
    [   # Spawned Enemy Ships
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [   # Their Spawn Position
        (WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//2, -120), (2*WINDOW_WIDTH/3, -130)
    ],   # Their Speed
    [5, 5, 5],
    [   # The actions they perform
        go_towards_actions((WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//3 - 150, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//3 - 150, 130), (WINDOW_WIDTH//3 - 50, 200), 5, True)
        + go_towards_actions((WINDOW_WIDTH//3 - 50, 200), (WINDOW_WIDTH//3 - 250, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((WINDOW_WIDTH//2, -120), (WINDOW_WIDTH//2, 130), 5, False)
        + go_towards_actions((WINDOW_WIDTH//2, 130), (WINDOW_WIDTH//2, 185), 5, True)
        + go_towards_actions((WINDOW_WIDTH//2, 185), (WINDOW_WIDTH//2, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((2*WINDOW_WIDTH/3, -130), (2*WINDOW_WIDTH/3 + 150, 130), 5, False)
        + go_towards_actions((2*WINDOW_WIDTH/3 + 150, 130), (2*WINDOW_WIDTH/3 + 50, 200), 5, True)
        + go_towards_actions((2*WINDOW_WIDTH/3 + 50, 200), (2*WINDOW_WIDTH/3 + 250, WINDOW_HEIGHT + 200), 5, True)
    ]
)
PHASE_TRIANGLE_TRIO = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//2, -120), (2*WINDOW_WIDTH/3, -130)
    ],
    [5, 5, 5],
    [
        go_towards_actions((WINDOW_WIDTH//3, -130), (WINDOW_WIDTH//3, 130), 5, False)
        + shoot_actions(6)
        + go_towards_actions((WINDOW_WIDTH//3, 130), (WINDOW_WIDTH//3, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((WINDOW_WIDTH//2, -120), (WINDOW_WIDTH//2, 120), 5, False)
        + shoot_actions(6.5)
        + go_towards_actions((WINDOW_WIDTH//2, 120), (WINDOW_WIDTH//2, WINDOW_HEIGHT + 200), 5, True),

        go_towards_actions((2*WINDOW_WIDTH/3, -130), (2*WINDOW_WIDTH/3, 130), 5, False)
        + shoot_actions(6)
        + go_towards_actions((2*WINDOW_WIDTH/3, 130), (2*WINDOW_WIDTH/3, WINDOW_HEIGHT + 200), 5, True)
    ]
)
PHASE_CENTER_LINE = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (WINDOW_WIDTH//2, -100), (WINDOW_WIDTH//2, -300), (WINDOW_WIDTH//2, -500), (WINDOW_WIDTH//2, -700)
    ],
    [5, 5, 5, 5],
    [
        go_towards_actions((WINDOW_WIDTH//2, -100), (WINDOW_WIDTH//2, 700), 5, False)
        + go_towards_actions((WINDOW_WIDTH//2, 700), (100, WINDOW_HEIGHT + 150), 5, True),

        go_towards_actions((WINDOW_WIDTH//2, -300), (WINDOW_WIDTH//2, 500), 5, False)
        + go_towards_actions((WINDOW_WIDTH // 2, 500), (WINDOW_WIDTH - 100, WINDOW_HEIGHT + 150), 5, True),

        go_towards_actions((WINDOW_WIDTH // 2, -500), (WINDOW_WIDTH // 2, 300), 5, False)
        + go_towards_actions((WINDOW_WIDTH // 2, 300), (-100, WINDOW_HEIGHT + 150), 5, True),

        go_towards_actions((WINDOW_WIDTH // 2, -700), (WINDOW_WIDTH // 2, 100), 5, False)
        + go_towards_actions((WINDOW_WIDTH // 2, 100), (WINDOW_WIDTH + 100, WINDOW_HEIGHT + 150), 5, True)
    ]
)
PHASE_DOUBLE_SWEEP = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (WINDOW_WIDTH//5, -100), (3*WINDOW_WIDTH//5, -100), (2*WINDOW_WIDTH//5, -100), (4*WINDOW_WIDTH//5, -100)
    ],
    [4, 4, 4, 4],
    [
        go_towards_actions((WINDOW_WIDTH//5, -100), (WINDOW_WIDTH//5, 110), 4, False)
        + (
            go_towards_actions((WINDOW_WIDTH//5, 110), (3*WINDOW_WIDTH//5, 110), 4, True)
            + go_towards_actions((3*WINDOW_WIDTH//5, 110), (WINDOW_WIDTH//5, 110), 4, True)
        ) * 10,

        go_towards_actions((3*WINDOW_WIDTH//5, -100), (3*WINDOW_WIDTH//5, 110), 4, False)
        + (
            go_towards_actions((3*WINDOW_WIDTH//5, 110), (WINDOW_WIDTH-120, 110), 4, True)
            + go_towards_actions((WINDOW_WIDTH - 120, 110), (3*WINDOW_WIDTH//5, 110), 4, True)
        ) * 10,

        go_towards_actions((2*WINDOW_WIDTH//5, -100), (2*WINDOW_WIDTH//5, 310), 4, False)
        + (
            go_towards_actions((2*WINDOW_WIDTH//5, 310), (120, 310), 4, True)
            + go_towards_actions((120, 310), (2*WINDOW_WIDTH//5, 310), 4, True)
        ) * 10,

        go_towards_actions((4*WINDOW_WIDTH//5, -100), (4*WINDOW_WIDTH//5, 310), 4, False)
        + (
            go_towards_actions((4*WINDOW_WIDTH//5, 310), (2*WINDOW_WIDTH//5, 310), 4, True)
            + go_towards_actions((2*WINDOW_WIDTH//5, 310), (4*WINDOW_WIDTH//5, 310), 4, True)
        ) * 10
    ]
)
PHASE_SWEEP = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (WINDOW_WIDTH//5, -100), (3*WINDOW_WIDTH//5, -100)
    ],
    [4, 4],
    [
        go_towards_actions((WINDOW_WIDTH//5, -100), (WINDOW_WIDTH//5, 110), 4, False)
        + (
            go_towards_actions((WINDOW_WIDTH//5, 110), (3*WINDOW_WIDTH//5, 110), 4, True)
            + go_towards_actions((3*WINDOW_WIDTH//5, 110), (WINDOW_WIDTH//5, 110), 4, True)
        ) * 10,

        go_towards_actions((3*WINDOW_WIDTH//5, -100), (3*WINDOW_WIDTH//5, 110), 4, False)
        + (
            go_towards_actions((3*WINDOW_WIDTH//5, 110), (WINDOW_WIDTH-120, 110), 4, True)
            + go_towards_actions((WINDOW_WIDTH - 120, 110), (3*WINDOW_WIDTH//5, 110), 4, True)
        ) * 10
    ]
)
PHASE_INVASION = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (WINDOW_WIDTH//4, -130), (WINDOW_WIDTH//2, -200), (3*WINDOW_WIDTH/4, -130),
        (WINDOW_WIDTH//3, -200), (2*WINDOW_WIDTH/3, -200)
    ],
    [
        7, 6, 5, 7, 6
    ],
    [
        go_towards_actions((WINDOW_WIDTH//4, -130), (WINDOW_WIDTH//4, WINDOW_HEIGHT//2), 7, True)
        + go_towards_actions((WINDOW_WIDTH//4, WINDOW_HEIGHT//2),
                             (WINDOW_WIDTH//4 - 200, WINDOW_HEIGHT//2 + 100), 7, False)
        + go_towards_actions((WINDOW_WIDTH//4 - 200, WINDOW_HEIGHT//2 + 100),
                             (WINDOW_WIDTH//4 - 100, WINDOW_HEIGHT + 200), 7, False),

        go_towards_actions((WINDOW_WIDTH//2, -200), (WINDOW_WIDTH//2, WINDOW_HEIGHT//3), 6, True)
        + go_towards_actions((WINDOW_WIDTH//2, WINDOW_HEIGHT//3),
                             (WINDOW_WIDTH//2 + 100, WINDOW_HEIGHT//3 + 150), 6, False)
        + go_towards_actions((WINDOW_WIDTH//2 + 100, WINDOW_HEIGHT//3 + 150),
                             (WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT + 200), 6, False),

        go_towards_actions((3*WINDOW_WIDTH/4, -130), (3*WINDOW_WIDTH/4, WINDOW_HEIGHT//2), 5, True)
        + go_towards_actions((3*WINDOW_WIDTH/4, WINDOW_HEIGHT//2),
                             (3*WINDOW_WIDTH/4 + 200, WINDOW_HEIGHT//2 + 100), 5, False)
        + go_towards_actions((3*WINDOW_WIDTH/4 + 200, WINDOW_HEIGHT//2 + 100),
                             (3*WINDOW_WIDTH/4 + 100, WINDOW_HEIGHT + 200), 5, False),

        go_towards_actions((WINDOW_WIDTH//3, -200), (WINDOW_WIDTH//3, WINDOW_HEIGHT//3), 7, True)
        + go_towards_actions((WINDOW_WIDTH//3, WINDOW_HEIGHT//3),
                             (WINDOW_WIDTH//3 - 100, WINDOW_HEIGHT//3 + 150), 7, False)
        + go_towards_actions((WINDOW_WIDTH//3 - 100, WINDOW_HEIGHT//3 + 150),
                             (WINDOW_WIDTH//3 + 100, WINDOW_HEIGHT + 200), 7, False),

        go_towards_actions((2*WINDOW_WIDTH/3, -200), (2*WINDOW_WIDTH/3, WINDOW_HEIGHT//3), 6, True)
        + go_towards_actions((2*WINDOW_WIDTH/3, WINDOW_HEIGHT//3),
                             (2*WINDOW_WIDTH/3 + 100, WINDOW_HEIGHT//3 + 150), 6, False)
        + go_towards_actions((2*WINDOW_WIDTH/3 + 100, WINDOW_HEIGHT//3 + 150),
                             (2*WINDOW_WIDTH/3 - 100, WINDOW_HEIGHT + 200), 6, False)
    ]
)
PHASE_QUAD_PUSH = Phase(
    [
        DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP, DEFAULT_ENEMY_SHIP
    ],
    [
        (100, -100), (WINDOW_WIDTH//2-100, -100), (WINDOW_WIDTH//2+100, -100), (WINDOW_WIDTH-100, -100)
    ],
    [
        6, 6, 6, 6
    ],
    [
        go_towards_actions((100, -100), (100, WINDOW_HEIGHT + 150), 6, True),
        go_towards_actions((WINDOW_WIDTH//2-100, -100), (WINDOW_WIDTH//2-100, WINDOW_HEIGHT + 150), 6, True),
        go_towards_actions((WINDOW_WIDTH//2+100, -100), (WINDOW_WIDTH//2+100, WINDOW_HEIGHT + 150), 6, True),
        go_towards_actions((WINDOW_WIDTH-100, -100), (WINDOW_WIDTH-100, WINDOW_HEIGHT + 150), 6, True),
    ]
)

# Level Constant Objects, used to create new instances of the level type
LEVEL_ONE = Level(
    [   # The phases of the level
        PHASE_SWEEP.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_TOKYO_DRIFT.create_new()
    ],  # The ship constant of the player, player's spawn position, and player's movement speed
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [   # Array of weapons that can be spawned to pick up, on the level
        # (default can't be spawned because it has infinite ammo)
    ],
    # The text shown at the start of the level: Title, text
    ("Level 1", "The Hard Beginning")
)
LEVEL_TWO = Level(
    [
        PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_INVASION.create_new()
    ],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [
        spaceship.MINIGUN
    ],
    ("Level 2", "The Grinder")
)
LEVEL_THREE = Level(
    [
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_TOKYO_DRIFT.create_new()
    ],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [
        spaceship.MINIGUN
    ],
    ("Level 3", "Rush B")
)
LEVEL_FOUR = Level(
    [
        PHASE_INVASION.create_new(),
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_INVASION.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_INVASION.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_INVASION.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_TOKYO_DRIFT.create_new()
    ],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [
        spaceship.MINIGUN, spaceship.ROCKET_GUN
    ],
    ("Level 4", "Big Bang Boom")
)
LEVEL_FIVE = Level(
    [
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_INVASION.create_new()
    ],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [
        spaceship.MINIGUN, spaceship.ROCKET_GUN
    ],
    ("Level 5", "The Loose End")
)
LEVEL_SIX = Level(
    [
        PHASE_TOKYO_DRIFT.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_CENTER_LINE.create_new(),
        PHASE_DOUBLE_SWEEP.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_TRIANGLE_TRIO.create_new(),
        PHASE_INVASION.create_new(),
        PHASE_SWEEP.create_new(),
        PHASE_QUAD_PUSH.create_new(),
        PHASE_CENTER_LINE.create_new()
    ],
    DEFAULT_SHIP, (WINDOW_WIDTH//2, WINDOW_HEIGHT - 100), 20,
    [
        spaceship.MINIGUN, spaceship.ROCKET_GUN
    ],
    ("Level 6", "The Finale")
)
