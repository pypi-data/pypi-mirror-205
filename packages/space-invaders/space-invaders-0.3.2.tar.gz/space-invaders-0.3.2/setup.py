from setuptools import setup, find_packages

setup(
    name='space-invaders',
    version='0.3.2',
    packages=find_packages(),
    install_requires=[
        'pygame',
        'shapely'
    ],
    entry_points={
        'console_scripts': [
            'space-invaders=space_invaders.run_game:main'
        ]
    },
    author='Bódi Martin',
    author_email='bodimartin22@gmail.com',
    description='A cool spaceship shooter rouge like game inspired by Hyperspace Invaders',
    long_description=open('space_invaders/README.md').read(),
    long_description_content_type='text/markdown',
    include_package_data=True
)
