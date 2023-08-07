import random
import pygame.display
from pygame.locals import K_w, K_a, K_s, K_d, K_SPACE, K_LSHIFT, USEREVENT
from shapely.geometry import Polygon
from space_invaders.entity import Entity
from space_invaders.pickup import PICKUP_LIFE, PICKUP_MINIGUN, PICKUP_REPAIR, PICKUP_ROCKET_GUN, PICKUP_SMALL_HEAL, \
    PICKUP_MEDIUM_HEAL, PICKUP_FIRE_RATE_BOOSTER, Pickup, RESET_FIRE_RATE, PICKUP_DEFAULT_GUN
from space_invaders.spaceship import ROCKET_GUN, MINIGUN
from space_invaders.config import WINDOW_WIDTH, WINDOW_HEIGHT, play_sound, PICKUP_SPEED, PICKUP_SPAWN_INTERVAL, \
    SOUND_CREDITS_DATA, SOUND_EXPLOSION_DATA, SOUND_MAIN_THEME_DATA, SOUND_DEFEAT_DATA, SOUND_VICTORY_DATA, \
    SOUND_ENEMY_HIT_DATA, SOUND_PLAYER_HIT_DATA, SHOW_COLLIDERS, get_credits_text, EXPLOSION_DURATION, \
    RESET_SWITCH_DELAY, FONT_CREDITS_TEXT_DATA, FONT_CREDITS_TITLE_DATA, FONT86_DATA, FONT15_DATA, FONT152_DATA, \
    FONT25_DATA, FONT36_DATA, CHANNEL_COUNT, CAPTION, BACKGROUND_IMAGE, SOUND_PICKUP_DATA, LAUNCH_GAME
import space_invaders.config as config
import space_invaders.level as level


def update_pickups():
    """
    Moves each pickup downwards, checks if any of them collides with the player.
    If there is collision, it plays a sound and applies the effect of the pickup
    """
    global pickups, window, player
    player_poly = Polygon(player.collider)

    for pickup in pickups:
        if pickup.position[1] > WINDOW_HEIGHT + 55:
            pickups.remove(pickup)
        else:
            pickup_poly = Polygon([pickup.collider.topleft, pickup.collider.topright,
                                   pickup.collider.bottomright, pickup.collider.bottomleft])
            if pickup_poly.intersects(player_poly):
                play_sound(SOUND_PICKUP_DATA, 0)
                pickup.action(player, *pickup.args)
                pickups.remove(pickup)
            else:
                pickup.move((0, PICKUP_SPEED))
                pickup.render(window)
                if SHOW_COLLIDERS:
                    pygame.draw.rect(window, (255, 0, 255), pickup.collider, 1)


def spawn_pickup():
    """
    Spawns a random pickup at a random position, adds it to the global pickups array
    """
    global pickups, current_level

    rnd = random.randint(0, 100)
    if rnd > 96:
        pickup_type = PICKUP_LIFE
    elif rnd > 87:
        pickup_type = PICKUP_REPAIR
    elif rnd > 80 and ROCKET_GUN in current_level.spawned_weapons:
        pickup_type = PICKUP_ROCKET_GUN
    elif rnd > 70 and MINIGUN in current_level.spawned_weapons:
        pickup_type = PICKUP_MINIGUN
    elif rnd > 60:
        pickup_type = PICKUP_FIRE_RATE_BOOSTER
    elif rnd > 30:
        pickup_type = PICKUP_MEDIUM_HEAL
    else:
        pickup_type = PICKUP_SMALL_HEAL

    spawn_location = (random.randint(50, WINDOW_WIDTH-50), -60)
    spawned_pickup = pickup_type.new_pickup()
    spawned_pickup.position = spawn_location
    pickups.append(spawned_pickup)


def spawn_at_random_interval():
    """Sets a timer with random delay for the SPAWN PICKUP event"""
    pygame.time.set_timer(SPAWN_PICKUP, random.randint(int(PICKUP_SPAWN_INTERVAL[0]*1000),
                                                       int(PICKUP_SPAWN_INTERVAL[1]*1000)))


def get_pickup_image_by_gun(gun):
    """
    @param gun a Gun object
    @return: a pygame Surface image based on the type of the given gun
    """
    match gun.type:
        case "rocket":
            return PICKUP_ROCKET_GUN.image
        case "minigun":
            return PICKUP_MINIGUN.image
        case _:
            return PICKUP_DEFAULT_GUN.image


def display_hud():
    """
    Displays each enemy's health, then the player's health, lives.
    Draws the fire rate booster's symbol if the player's fire rate is boosted
    And shows the player's current score
    """
    global player, enemies, window

    # Enemy healths
    for enemy_ in enemies:
        position = (enemy_.image_rect.center[0], enemy_.image_rect.center[1] - 18)
        shift = 37
        scale = 15
        width = 90
        pygame.draw.rect(window, (255, 50, 50), (position[0] - width/2, position[1] - scale//2 - shift, width, scale))
        pygame.draw.rect(window, (50, 255, 50), (position[0] - width/2, position[1] - scale//2 - shift,
                                                 width * enemy_.hp / enemy_.max_hp, scale))
        player_hp_amount = FONT15.render(f"{enemy_.hp}", True, (25, 25, 20))
        window.blit(player_hp_amount, (position[0] - scale//2, position[1] - scale//2 - shift))

    # Player health
    player_hp_text = FONT36.render("+", True, (50, 255, 20))
    window.blit(player_hp_text, (10, 17))
    pygame.draw.rect(window, (255, 50, 50), (40, 20, 250, 30))
    pygame.draw.rect(window, (50, 255, 50), (40, 20, 250 * player.hp/player.max_hp, 30))
    player_hp_amount = FONT36.render(f"{player.hp}", True, (25, 25, 20))
    window.blit(player_hp_amount, (50, 17))

    # Player lives
    lives_image = pygame.image.load(config.get_path("Sprites", "life.png"))
    lives_image = pygame.transform.scale(lives_image, (45, 45))
    for i in range(max(player.lives - 1, 0)):
        window.blit(lives_image, (0 + i * 50, 65))

    # Player is fire rate boosted
    if player.ship.fire_rate_multiplier < 1:
        fire_rate_image = pygame.image.load(config.get_path("Sprites", "fire_rate_booster.png"))
        fire_rate_image = pygame.transform.scale(fire_rate_image, (45, 45))
        window.blit(fire_rate_image, (5, 120))

    # Player ammo
    guns = player.ship.guns
    ordered_guns = [guns[i % len(guns)] for i in range(player.ship.active_gun, player.ship.active_gun + len(guns))]
    for i in range(len(ordered_guns)):
        gun_icon = get_pickup_image_by_gun(ordered_guns[i])
        gun_icon = pygame.transform.scale(gun_icon, (70, 70) if i == 0 else (55, 55))
        window.blit(gun_icon, (WINDOW_WIDTH - 180 + (0 if i == 0 else 20),
                               10 + ((80 if i == 1 else 140) if i > 0 else 0)))
        ammo_count = ordered_guns[i].ammo
        gun_ammo_text = (FONT36 if i == 0 else FONT25).render(f"{ammo_count if ammo_count >=0 else 'inf'}", True,
                                                              (50, 200, 200) if ammo_count != 0 else (200, 50, 50))
        window.blit(gun_ammo_text, (WINDOW_WIDTH - (100 if i == 0 else 90),
                                    30 + ((80 if i == 1 else 140) if i > 0 else 0)))

    # Player Score
    score_text = FONT36.render(str(config.score), True, (255, 255, 0))
    score_text_shadow = FONT36.render(str(config.score), True, (50, 50, 0))
    window.blit(score_text_shadow, (15, WINDOW_HEIGHT - 45))
    window.blit(score_text, (10, WINDOW_HEIGHT - 50))


def display_credits():
    """
    Displays the credits of the project, makes it possible fast-forward with SPACE, W, S keys
    At the end of the credits, the application is closed
    """
    global window
    pygame.mixer_music.stop()
    play_sound(SOUND_CREDITS_DATA, -1)
    shift = 0
    while shift < int(WINDOW_HEIGHT * 3.05):
        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                exit()

        if pygame.key.get_pressed()[K_SPACE] or pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_s]:
            shift += 10

        window.fill((11, 11, 11))
        i = 0
        for line in get_credits_text().split('\n'):
            data = FONT_CREDITS_TITLE if line.isupper() else FONT_CREDITS_TEXT
            text = data.render(line, True, (255, 0, 255) if line.isupper() else (0, 255, 255))
            window.blit(text, (WINDOW_WIDTH // 2 - text.get_width() / 2, WINDOW_HEIGHT + i * 70 - shift))
            i += 1

        pygame.display.update()
        clock.tick(60)
        shift += 1

    pygame.time.wait(1500)

    for i in range(12, 0, -1):
        window.fill((i, i, i))
        pygame.display.update()
        clock.tick(30)

    pygame.time.wait(500)
    pygame.quit()
    exit()


def level_over():
    """
    Handles the end of the current level
    Loads the first level if the player died
    Otherwise it loads the next level if it exists, if it doesn't, the display_credits is called
    """
    global LEVELS, LEVEL_OVER, level_index

    if player.alive():
        play_sound(SOUND_VICTORY_DATA, 0)
        text_color = (50, 200, 50)
        shadow_color = (20, 100, 20)
        config.score += 1000

        if len(LEVELS) - 1 == level_index:
            text = "VICTORY!"
        else:
            text = "COMPLETED!"
    else:
        play_sound(SOUND_DEFEAT_DATA, 0)
        text_color = (200, 50, 50)
        shadow_color = (100, 20, 20)
        text = "DEFEAT!"
        config.score = 0

    level_over_text = FONT152.render(text, True, text_color)
    level_over_text_shadow = FONT152.render(text, True, shadow_color)

    window.blit(level_over_text_shadow, (WINDOW_WIDTH // 2 - level_over_text.get_size()[0]/2 + 5,
                                         WINDOW_HEIGHT // 2 - level_over_text.get_size()[1] + 5))
    window.blit(level_over_text, (WINDOW_WIDTH // 2 - level_over_text.get_size()[0]/2,
                                  WINDOW_HEIGHT // 2 - level_over_text.get_size()[1]))
    pygame.display.update()

    LEVEL_OVER = False
    pygame.mixer_music.stop()
    pygame.time.wait(3000)
    pygame.mixer_music.play(-1)

    if player.alive():
        level_index += 1
        if level_index < len(LEVELS):
            load_level(LEVELS[level_index])
        else:
            display_credits()
    else:
        entities.remove(player)
        level_index = 0
        load_level(LEVELS[0])


def check_entity_collision(player_entity, enemy_entities):
    """
    Checks if the player collides with any of the enemy entities, if yes they both take damage equal to the other's hp

    @param player_entity the player
    @param enemy_entities the array of enemies that are checked
    """
    player_poly = Polygon(player_entity.collider)

    for _enemy in enemy_entities:
        enemy_poly = Polygon(_enemy.collider)
        if player_poly.intersects(enemy_poly):
            play_sound(SOUND_ENEMY_HIT_DATA, 0)
            play_sound(SOUND_PLAYER_HIT_DATA, 0)
            enemy_hp = _enemy.hp
            _enemy.take_damage(player_entity.hp)
            player_entity.take_damage(enemy_hp)


def handle_player_input(player_entity: Entity, max_x, max_y):
    """
    Handles the player's input
    @param player_entity the player's entity
    @param max_x the maximum x position that is allowed
    @param max_y the maximum y position that is allowed
    """
    global CAN_SWITCH_GUN, RESET_CAN_SWITCH
    pressed_keys = pygame.key.get_pressed()
    vec = [0, 0]

    # setting up the movement vector
    if pressed_keys[K_w]:
        vec[1] -= 0.65
    if pressed_keys[K_s]:
        vec[1] += 0.65
    if pressed_keys[K_a]:
        vec[0] -= 1
    if pressed_keys[K_d]:
        vec[0] += 1

    # applying the movement
    player_entity.move(vec)

    # keeping the player inbound
    if player_entity.image_rect.left < 0:
        player_entity.move((-player_entity.image_rect.left/player_entity.speed, 0))
    elif player_entity.image_rect.right > max_x:
        player_entity.move(((max_x - player_entity.image_rect.right)/player_entity.speed, 0))
    if player_entity.image_rect.top < 0:
        player_entity.move((0, -player_entity.image_rect.top/player_entity.speed))
    elif player_entity.image_rect.bottom > max_y:
        player_entity.move((0, (max_y - player_entity.image_rect.bottom)/player_entity.speed))

    # other inputs
    if pressed_keys[K_LSHIFT] and CAN_SWITCH_GUN:
        CAN_SWITCH_GUN = False
        player_entity.next_gun()
        pygame.time.set_timer(RESET_CAN_SWITCH, RESET_SWITCH_DELAY)
    if pressed_keys[K_SPACE]:
        player_entity.shoot()


def load_level(_level):
    """
    Loads the next level, resets the global arrays to be empty
    If the player is still alive from the last level it is copied to the new level and his position is set to the
    new level's spawn position, also the player's hp is recharged.
    After loading the level, the level's title and text is displayed
    """
    global current_level, player, entities, enemies, pickups, explosions
    entities = []
    enemies = []
    pickups = []
    explosions = []
    level.initialize_global_arrays(entities, enemies)

    previous_level = current_level
    current_level = _level.create_new()
    if previous_level is None or not player.alive():
        player = current_level.spawn_player()
    else:
        entities.append(player)
        player.ship.empty_projectiles()
        player.heal(200000)
        player.ship.set_position(_level.player_spawn_position)

    # Rendering text shown before the level starts
    title = FONT152.render(current_level.level_text[0], True, (0, 255, 255))
    title_shadow = FONT152.render(current_level.level_text[0], True, (255, 0, 255))
    text = FONT86.render(current_level.level_text[1], True, (200, 200, 200))
    text_shadow = FONT86.render(current_level.level_text[1], True, (50, 50, 50))

    window.fill((8, 8, 8))
    window.blit(title_shadow, (154, 255))
    window.blit(title, (150, 250))
    window.blit(text_shadow, (154, 424))
    window.blit(text, (150, 420))

    pygame.display.update()
    pygame.time.wait(2000)

    return player, current_level


"""
The main game loop tat pulls everything together
"""
if LAUNCH_GAME:
    # INITIALIZATIONS
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(CHANNEL_COUNT)
    LEVEL_OVER = False
    CAN_SWITCH_GUN = True
    RESET_CAN_SWITCH = USEREVENT + 2
    SPAWN_PICKUP = USEREVENT + 3
    LEVELS = [level.LEVEL_ONE, level.LEVEL_TWO, level.LEVEL_THREE, level.LEVEL_FOUR, level.LEVEL_FIVE, level.LEVEL_SIX]
    level_index = 0

    pygame.display.set_caption(CAPTION)
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    FONT_CREDITS_TEXT = pygame.font.Font(*FONT_CREDITS_TEXT_DATA)
    FONT_CREDITS_TITLE = pygame.font.Font(*FONT_CREDITS_TITLE_DATA)
    FONT152 = pygame.font.Font(*FONT152_DATA)
    FONT86 = pygame.font.Font(*FONT86_DATA)
    FONT36 = pygame.font.Font(*FONT36_DATA)
    FONT25 = pygame.font.Font(*FONT25_DATA)
    FONT15 = pygame.font.Font(*FONT15_DATA)
    background_img = pygame.image.load(BACKGROUND_IMAGE).convert()
    background_img = pygame.transform.scale(background_img, (WINDOW_WIDTH, WINDOW_HEIGHT))

    clock = pygame.time.Clock()
    play_sound(SOUND_MAIN_THEME_DATA, -1)

    # Declaration of global arrays
    entities = enemies = pickups = explosions = []

    # Loading the first level, and its player
    current_level = player = None
    player, current_level = load_level(LEVELS[0])

    if player is not None and current_level is not None:
        # Queues a new pickup spawn
        spawn_at_random_interval()

        while True:
            if LEVEL_OVER:
                level_over()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == SPAWN_PICKUP:
                    spawn_pickup()
                    spawn_at_random_interval()
                elif event.type == RESET_FIRE_RATE:
                    Pickup.action_reset_fire_rate(player)
                elif event.type == RESET_CAN_SWITCH:
                    CAN_SWITCH_GUN = True

            handle_player_input(player, WINDOW_WIDTH, WINDOW_HEIGHT)
            current_level.execute_phase()
            check_entity_collision(player, enemies)

            if player.alive():
                explosions.extend(player.check_projectile_hit(enemies))

                for enemy in enemies:
                    explosions.extend(enemy.check_projectile_hit([player]))

                    if not enemy.alive():
                        play_sound(SOUND_EXPLOSION_DATA, 0)
                        config.score += 500

                        explosions.append([pygame.image.load(config.get_path("Sprites", "ship_explosion.png")),
                                           enemy.image_rect.center, EXPLOSION_DURATION])

                        enemies.remove(enemy)
                        entities.remove(enemy)

            # render everything
            window.blit(background_img, (0, 0))
            for entity in entities:
                entity.render(window, SHOW_COLLIDERS)
            update_pickups()
            for explosion in explosions:
                if explosion[2] == 0:
                    explosions.remove(explosion)
                else:
                    explosion_image = explosion[0]
                    explosion_image = pygame.transform.scale(explosion_image, (explosion_image.get_size()[0] * 1.15,
                                                                               explosion_image.get_size()[1] * 1.15))
                    explosion[0] = explosion_image

                    window.blit(explosion_image, (explosion[1][0] - explosion_image.get_rect().width // 2,
                                                  explosion[1][1] - explosion_image.get_rect().height // 2))
                    explosion[2] -= 1
            display_hud()

            if not player.alive() or current_level.is_complete():
                if not player.alive():
                    explosions.append([pygame.image.load(config.get_path("Sprites", "ship_explosion.png")),
                                       player.image_rect.center, EXPLOSION_DURATION])

                LEVEL_OVER = True

            pygame.display.update()
            clock.tick(60)
