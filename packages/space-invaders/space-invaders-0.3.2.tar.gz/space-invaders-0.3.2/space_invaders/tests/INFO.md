
# Unittesting The Project  
  
## Important  
- The tests folder is not required for the game to work, it only serves testing purposes
- These files are only included due to the project being a university project  
- Not every method is tested since the complexity of the project makes it a nightmare  
- If I tested all cases it would take more time than the age of the universe  
- Methods with non-sense parameters are not tested since checking them in every single   
  method would ruin the cleanness of the code, also they can never happen in action.   
  Also the error messages they Raise helps the development more, than not doing anything if the parameters   are wrong  
- Lastly methods that only fiddle around with private attributes, as well as render purpose methods and 
  methods that were only made to make the code cleaner (i. e. shortening .ship.gun.shoot to shoot), are also not tested

## How To Run The Tests  

The testing libraries are not included with the project since they're not required for the regular use
  
### Installation  
 1. Install  unittest with the command below
 
			`pip install unittest`
 
 2. Install coverage with this command
	
			`pip install coverage`

### Running The Tests
1.  Change the current working directory in your terminal to the folder containing the space-invaders project

			cd 'path/to/the/project/..../'

2.  Execute all the tests

                `coverage run -m unittest discover -s .\space_invaders\tests\`

### Test Coverage Information
- <i>Do this <b>after</b> running the test</i>
- Execute this command:
			
			coverage report

## Results

### Tests
If everything works properly you shouldnt face any errors during the execution of the tests.
You should see something like this in the terminal:

>---------------------------------------------------------------------- <br>
>Ran 13 tests in 0.186s <br>
> <br>
>OK

### Coverage
And the coverage should give you something like this:
> Name                                     Stmts   Miss  Cover   <br>
> ------------------------------------------------------------   <br>
> space_invaders\__init__.py                   1      0   100%   <br>
> space_invaders\config.py                    52      6    88%   <br>
> space_invaders\entity.py                    95     23    76%   <br>
> space_invaders\level.py                    124     18    85%   <br>
> space_invaders\main.py                     286    249    13%   <br>
> space_invaders\pickup.py                    63     11    83%   <br>
> space_invaders\spaceship.py                210     63    70%   <br>
> space_invaders\tests\test_entity.py         53      0   100%   <br>
> space_invaders\tests\test_level.py          23      0   100%   <br>
> space_invaders\tests\test_main.py           24      0   100%   <br>
> space_invaders\tests\test_pickup.py         22      0   100%   <br>
> space_invaders\tests\test_spaceship.py      49      0   100%   <br>
> ------------------------------------------------------------   <br>
> TOTAL                                     1002    370    63%

