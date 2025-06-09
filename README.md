
# What is Universe's Hardest Game?
The "Universe's Hardest Game" is inspired by another popular game following the same convention, ["World's Hardest Game"](https://www.coolmathgames.com/0-worlds-hardest-game) on [Cool Math Games](https://www.coolmathgames.com/). It follows the exact same play style and level design. You control a red square through either WASD or the arrow keys, where you are forced to navigate and beat levels. Each level requires you to collect every coin. There are green zones which represents checkpoints or a win condition to fulfill a level.

Similarly, the game is extremely punishing. If you make a single mistake, such as you hitting an obstacle, your character is forced to respawn at the latest checkpoint, with the coins collected also being reset. Obstacles in this game, take the form of blue circles, they can move in a variety of patterns such as a circular motion, horizontally, and vertically.

# How to access and play the game
To run the game, you need to run `main.py`. To download the game on a UNIX based operating system, you can do the following:
```
git clone https://github.com/barbaronbow/Universe_Hardest_Game
cd Universe_Hardest_Game
python3 main.py
```

If you are on Windows, you can download the ZIP file and extract the contents, and run the main.py file.



# How to create custom levels
If you follow the instructions to download the game, you have access to a level editor. If you are on an UNIX based operating system, you can input the following command.
```
python3 level_editor.py 
```

If you are on Windows:
```
python level_editor.py
```

**Note:** Tiles in this game are by default 100 pixels x 100 pixels. The screen size is 18 tiles by 10 tiles.

You can select what tiles you want to place down on the game. Selecting `0` as a square is a requirement as it serves as the base tile of the game, which allows the player to traverse over it. Selecting `1` will place down walls (**Note:** do not place walls over character spawn point as it is impossible to play). 

**Note:** character spawnpoint is by default set at (100, 100) in pixels, meaning walls cannot be placed at (2, 2) in tiles.

Selecting `2` will place down checkpoints, meaning if your player travels over it, your progress will be saved up to that point. Selecting `3` will allow you place down a win square, meaning if your character travels over it, and as long as it collected all the coins, the level or game will be completed.


The other number squares can be set different functions if you are willing to spend extra time on it. To make sure the level will playable, you must add an extra index to both `levels_obstacles` list and `level_coins` list. The extra index does not need to contain anything.

In `level_coins` you just need to store the coordinates of each coin (in pixels). In `level_obstacles`, it stores dictionaries. The dictionary follows the format `{"x": x-coordinate, "y": y-coordinate, pattern, "range": the range the pattern takes, "speed" the quickness of the obstacle}`. The possible options for pattern includes:
* "circle" **Note:** the range is just the radius
* "horizontal"
* "vertical"
