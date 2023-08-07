import pygame
import os

"""
This is the configuration file, containing most of the globally used constants
Also a couple of globally used functions
"""

PATH = os.path.dirname(os.path.abspath(__file__))


def get_path(*args):
    """
    The method returns the given relative path converted into absolute path, based on where the project is installed
    It is required since the running environment may be elsewhere
    @param args the split relative path.
    @return: the absolute path
    """
    return os.path.join(PATH, *args)


CHANNEL_COUNT = 30
SOUND_MAIN_THEME_DATA = (get_path("Sounds", "340452__zagi2__dondolan2-loop.wav"), 0.5, 0)
SOUND_DEFAULT_GUN_DATA = (get_path("Sounds", "615809__flyingsaucerinvasion__sci-fi-laser-blaster-shot-3.wav"), 0.15, 0)
SOUND_MINIGUN_DATA = (get_path("Sounds", "156895__halgrimm__a-shot.wav"), 0.9, 0)
SOUND_ROCKET_DATA = (get_path("Sounds", "18380__inferno__hvrl.wav"), 0.6, 0)
SOUND_DEFEAT_DATA = (get_path("Sounds", "277403__landlucky__game-over-sfx-and-voice.wav"), 0.9, 0)
SOUND_VICTORY_DATA = (get_path("Sounds", "122255__jivatma07__level_complete.wav"), 1, 0)
SOUND_ENEMY_HIT_DATA = (get_path("Sounds", "427409__artembasov__ab_beep_or_blaster_shot.ogg"), 0.65, 0)
SOUND_PLAYER_HIT_DATA = (get_path("Sounds", "648200__strangehorizon__glitch_blip.wav"), 0.5, 0)
SOUND_EXPLOSION_DATA = (get_path("Sounds", "565481__jakegwizdak__small-explosion.wav"), 0.4, 0)
SOUND_PICKUP_DATA = (get_path("Sounds", "678384__jocabundus__item-pickup-v1.wav"), 0.7, 0)
SOUND_CREDITS_DATA = (get_path("Sounds", "353775__samueloak89__next-scene.mp3"), 0.7, 0)

MUSICS = (SOUND_MAIN_THEME_DATA, SOUND_CREDITS_DATA)


def play_sound(sound_data, loops):
    """
    Plays a sound or music based on the given sound_data, and loops it 'loops' times
    @param sound_data the sound_data tuple that is selected from the constants defined in config
    @param loops the number of loops
    """
    if sound_data in MUSICS:
        pygame.mixer_music.load(sound_data[0], "muzsika")
        pygame.mixer_music.set_volume(sound_data[1])
        pygame.mixer_music.fadeout(sound_data[2])
        pygame.mixer_music.play(loops=loops)
        return

    sound = pygame.mixer.Sound(sound_data[0])
    sound.set_volume(sound_data[1])
    sound.fadeout(sound_data[2])
    for i in range(pygame.mixer.get_num_channels()):
        if not pygame.mixer.Channel(i).get_busy():
            pygame.mixer.Channel(i).play(sound, loops=loops)
            break


FONT_CREDITS_TITLE_DATA = (get_path("Fonts", "AGENCYB.TTF"), 35)
FONT_CREDITS_TEXT_DATA = (get_path("Fonts", "AGENCYR.TTF"), 27)
FONT152_DATA = (get_path("Fonts", "Alien Invader.ttf"), 152)
FONT86_DATA = (get_path("Fonts", "Alien Invader.ttf"), 86)
FONT36_DATA = (get_path("Fonts", "Alien Invader.ttf"), 36)
FONT25_DATA = (get_path("Fonts", "Alien Invader.ttf"), 25)
FONT15_DATA = (get_path("Fonts", "Alien Invader.ttf"), 15)

EXPLOSION_DURATION = 4
RESET_SWITCH_DELAY = 200
PICKUP_SPEED = 5
PICKUP_SPAWN_INTERVAL = (4, 8)
score = 0

LAUNCH_GAME = False

SHOW_COLLIDERS = False
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 950
CAPTION = "Space Invaders"
BACKGROUND_IMAGE = get_path("Sprites", "background.png")


def get_credits_text():
    """
    Returns the credits string, with the updated score value
    @return: the credits string
    """
    return f"""CONGRATULATIONS!
YOU HAVE SUCCESSFULLY BEATEN THE GAME!
FINAL SCORE:  {score}



SOUNDS
main-theme-song:   https://freesound.org/people/zagi2/sounds/340452/  -  zagi2
default-gun-sound:   https://freesound.org/people/flyingsaucerinvasion/sounds/615809/  -  flyingsaucerinvasion
minigun-sound:   https://freesound.org/people/Halgrimm/sounds/156895/  -  Halgrimm
rocket-sound:   https://freesound.org/people/inferno/sounds/18380/  -  inferno
defeat-sound:   https://freesound.org/people/landlucky/sounds/277403/  -  landlucky
win-sound:   https://freesound.org/people/jivatma07/sounds/122255/  -  jivatma07
hit-positive-sound:   https://freesound.org/people/ArtemBasov/sounds/427409/  -  ArtemBasov
hit-negative-sound:   https://freesound.org/people/strangehorizon/sounds/648200/  -  strangehorizon
explosion-sound:   https://freesound.org/people/JakeGwizdak/sounds/565481/  -  JakeGwizdak
pick-up-sound:   https://freesound.org/people/Jocabundus/sounds/678384/  -  Jocabundus
credits-music:   https://freesound.org/people/samueloak89/sounds/353775/  -  samueloak89

FONTS
alien-invader-font:   https://www.dafont.com/alien-invader.font  -  Darrell Flood
agency-fb-font:  Builtin Windows Font  -  Bill Gates (I guess)

ART
Bódi Martin (Z9WTNS)

PROGRAMMING
Martin Bódi (h150714)
\n\n\n\n\n
--------------~ THE END ~--------------"""
