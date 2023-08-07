import runpy
import space_invaders.config as config


def main():
    """
    This is the Entry point of the program, if you want to run the project you need to run this method
    It launches the main.py module, also sets the LAUNCH_GAME True so that global code in main will run
    """
    print("3.. 2.. 1.. LAUNCH!")
    config.LAUNCH_GAME = True
    runpy.run_module("space_invaders.main")


if __name__ == '__main__':
    main()
