# SWING
## **Video Demo:** https://youtu.be/Q0IERwxRH6Q
## **Overview:** 
Swing is a game inspired by the game Flappy Bird. The game was created in PyGame, where you are tasked with weaving between gaps in the environment and to survive for as long as possible. The game tracks how many gaps you have passed, much like Flappy Bird. Where it differs is in how the game controls. Instead of tapping the screen to make the character jump in the air, you use a grappling hook to swing across the screen, hence where the name of the game came from. Below are the breakdowns of each file/directory that is involved in creating the game, and my thought processes behind them.

## **Images:**
This folder consists of all of the images that are used in the game, all of which are .png files. I chose to use .png files since they supported transparent backgrounds, which would allow me to overlap non-block shaped images such as the player sprite with the background. All of the images were drawn by me using a program called Aseprite, where I exported the finished image as a .png file. In the folder itself consists of the folders: *Animation*, *Buttons*, *Numbers*, and various *non-categorized images*.
### *Non-Categorized Images* 
These images are ones that don't have any animation/variance to them. The rest were bundled together by functions in game to avoid disorganized clutter within the folder while I was still creating the program. These images range from being the background of the game, to UI elements in the menus.
### *Animations*
These images consists of all of the frames involved in animating the player character. The rolling animation in particular consists of 4 frames that are looped between roll1 through roll4.
### *Buttons*
These images consists of all of the buttons that are used within the menus of the game. I decided to just manually draw out each variation of the menu as I did not have many menus in my game, so creating a function that dynamically renders each button would take much longer than the amount of buttons I would actually be using in game. Each button consists of a word/number representing a menu element, and 2 variants in the form of the default or hover states. The default state is when the button is drawn normally, while the hover state is drawn when the mouse is hovering over the button in game. Each button follows the naming scheme of button_(word on button)_(default/hover).png, that way organizing the buttons would be less of a mess when writing into code. 
### *Numbers*
These images consists of all the number symbols drawn in the pixel artstyle. These numbers are used in the program to dynamically generate the score UI. Unlike with the buttons, score would have too much variations to be able to realistically draw them all independently, so I just drew every digit and have the program put together the digits to generate a number to represent the score on the UI. 

## **Sounds:**
This folder contains all of the sounds used in the game, including SFX (sound effects) and BGM (background music). Some of the SFX used were the same ones the games I used to play in my childhood used, and I felt it was fun to include them. The BGMs used are royalty free tracks found on google. In regardes to credits, **startmenu_bgm.wav** *(Music: "Water Drops", from PlayOnLoop.com, Licensed under Creative Commons by Attribution 4.0)*, and **ingame_bgm.wav** *(Music by <a href="https://pixabay.com/users/zen_man-4257870/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=2691">Zen_Man</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=2691">Pixabay</a>)*

## **data.json:**
This file is how the game saves the options settings and the high score of the player. Besides high_score, the values in the file aren't the exact variables that are used in the program, this will be further elaborated on later in the **variables.py** section. I used a .json file as a way to save the game solely because I had not worked with json files in the past, and I wanted to get some basic practice in doing so.

## **variables.py**
This part consists of initializing the variables that will be used throughout the entirety of the program. The variables initialized in this file are set to global so that the other python files can change them. While some of the variables aren't actually changed during the game, I felt I should still initialize the variables in this file so that it would keep the code less messy, as all of the variables would just be in one location. The two try sections are used to check if a save exists, and if the save is in the correct format respectively. If no file exists, or the file is incorrect, then a new save file is created with 'default' settings. 

sfx_settings and bgm_settings are saved as a value between 0 to 10, despite the fact that pygame's volume settings utilize a float value between 0 to 1. In the save settings, 1 represents 0.1, 2 represents 0.2, and so on, where it is converted using match case. I chose to save it that way since I sometimes would run into float value addition errors, in which a trailing decimal would cause my match case to no longer match to any cases, causing issues in the program. Past the two try statements are lists of all of the images locations that are needed, ordered in such a way that allows for easier manipulation in the program. Followed by converting the lists into their appropriate classes that I created, which will be elaborated further in the **classes.py** section. 

The menu item classes are then bundled into a list that corresponds to a specific menu, ordered whereby the first element is at the top. The list will later be passed to the *draw_menu* function that will be elaborated further in the **functions.py** section. Finally the sound is initialized and the scroll speed is set based on the difficulty that was found in the save file.

## **classes.py**
This part consists of the class definitions and their methods. I chose to convert these particular cases into classes because they were either used a lot within the program, or many of them were present within the program.
### *player_avatar<sup> init</sup>*
The sprite property is the visuals of the class that is to be loaded into the game, while the hitbox property is where the actual interactivity with the enviornment comes from. Both these properties are used in *collidable* and *menu_item* classes in the exact same way. The grapple_state property shows whether the player is currently grappled or not, a property that is used to determine when to change speed calculations. Speed and score properties are self explanatory. The animation_frames property is group of image locations as been attributed to an action. When creating the classes, the inputs were ordered in such a way that the images correspond to the correct action. Roll frame is the index used to navigate the list attributed to 'roll' in the animation_frames dictionary.
### *player_avatar<sup> change_frame, animate</sup>*
These method changes the sprite of the image depending on what action was called. The animate method is the functional side of changing the sprite, determining when to change the sprite to the appropriate frame. While change_frame is the actual act of changing the image based on the action called. I split these two functions apart because there are times when the functionality aspect is not needed and only the act of changing the sprite itself is needed. The change_frame method is also used with the *menu_item* class, acting the exact same as here.
### *player_avatar<sup> update_speed, move, next_step</sup>*
These methods are used to actually move the player character. The update_speed method calculates x and y components of a diagonal acceleration vector using right angle triangles. The move method is just calling pygame's built in move function on itself. I created an entire method for this one line for the sake of code readability. The next_step method is used in collision detection, where the hitbox will be next frame is calculated via moving an extra time. The move and next_step methods are also used in the *collidable* class in the exact same way.

### *collidable<sup> init, scale_sprite</sup>*
The passed property is used to determine if a player has already passed through the gap, that way a player will not score multiple times by passing through the same gap multiple times. The scale_sprite method is used to stretch/squash the image to fix with the hitbox. This is needed since the block sizes are randomized, and drawing each variation manually is unrealistic.

### *menu_item<sup> init</sup>*
Since menu elements vary in the amount of frames they could contain, the intiailization process will differ. For one frame elements, default and hover frames are both set to None. While multi-frame elements will have every odd entry in the list be default variants and even entries as hover variants, and these are appended to the corresponding properties. The list that was passed in will be organized where every frame alternates between default and hover varients. The button_index property is used to navigate through menu elements where the element needs to cycle (such as the difficulty button). The clickable property is used to determine if an element is interactable or not.
### *menu_item<sup> position_item</sup>*
This method positions menu elements to the center of the window. I made this method since I had to call it multiple times in different functions that involved drawing a menu, to which this helped with code readbility.

### *background_class*
The background class is mainly used group background manipulating methods together for the sake of code readability. The left property of the background is for reading when a background has been fully cycled through. The main methods print and scroll and used for static and moving backgrounds respectively, while *reset_bg* is mainly if the background scroll position needs to be reset.

## **functions.py**
This file contains all of the functions that are used within **main.py**. The functions were separated from main in order to have more readability within the code.
### *set_volumes*
Converts data.json values into values usable by pygame set_volume function, then sets the volumes of all sounds/music to such value. Passed values consists of the raw values from the data.json file.
### *draw_buttons*
Draws all of the elements in a passed list representing the specific menu that is needed to be drawn. The try section is included since I kept running into errors when the game initially booted up, where the mouse_pos didn't have a value yet, resulting in a TypeError.
### *align_buttons*
Centers all of menu_elements and moves each element below the element before by an inputted amount, and the first elements height can be specified. I made the layout relatively uncustomizable since my menu layout for all menus was going to be the same, and this would streamline the process of creating different menus without writing a specific draw function for each different menu.
### *draw_menu*
Combines *draw_buttons* and *align_buttons* into one function, where an organized menu is finally drawn. I made this it's own function since the previous two functions need to be constantly called together in order to have a proper menu.
### *check_clicked*
Goes through the entire list of buttons within the menu to see if any was clicked, returns the button that was clicked if there was one, otherwise it will return None. While inefficient, this way of checking can be easily generalized to every menu possible in the game. Combined with the fact that there aren't enough menu elements that would drop performance, I ended up choosing to use this inefficient means of checking.
### *pause_game*
The loop where **main.py** enters when a key that pauses the game is pressed. The functionality within the pause menu is not in the function itself, but is located in **main.py**. I chose to do this to make it easier to read the main file, since you would have to refer back to the functions file to see what is happening.
### *close_game*
Called when either the menu is closed, or the quit button is pressed in the start menu. Used the properly close the program entirely.
### *randomize_block*
Randomizes the size and location of the gap along the wall, and assigns a sprite to the blocks depending on the size that was generated.
### *move_blocks*
Scrolls the blocks across the screen from right to left at the inputted speed, and re-randomizes the blocks once it has moved out of the screen. I added an extra part where the scrolling speed will be faster than the player's horizontal speed once the player character is too far right of the screen. This was done so a skilled player that was further ahead in the screen wouldn't have to slowly wait for the next obstacle to scroll in.
### *initialize_ingame_assets*
Resets all of the values used in game to that of the values at the beginning of the game. Along with randomizing the blocks and restarting the music from the beginning. I decided to make this a function rather than being in **main.py** since this needed to be called from multiple different menus.
### *render_score*
Takes an inputted number and displays that number using the pixel style numbers at the center of the screen at a specified height. I chose to convert the number into a string so I could more intuitively work with one digit at a time. Match case was used since there were 10 entries to compare with, and match case are better for performance in such cases.
### *draw_ingame_assets*
Refreshes the screen every frame by drawing each asset in the correct order. This function is called every frame at the end of each loop. I made this into a function to make it more clear what the code in **main.py** is doing.
### *draw_game_over*
A variation of the previous function, where it is called in the game over menu. The initial part redraws where everything was at the time of the player's death. The later parts is responsible for drawing the score UI and the menu itself. I needed to redraw the background again to remove the in-game score display from the game over menu.
### *handle_collision*
Adjusts the player's speed when a collision is detected, and is called every frame to check for any possible collisions. I decided to use next frames to detect collisions rather than the current frame because the player character would sometimes get stuck against the blocks if I didn't. The bounce-back effect of hitting an obstacle might not be enough to escape the hitbox of it, and since the player's speed is reversed and halved every frame they are in the hitbox of the obstacle, it results in the player getting stuck against the obstacle. I ended up choosing to use next frames for collision detection after remembering that the game Super Mario 64 also used the same system, though in a more complicated way.
### *check_death*
Checks if the player is squished between the left of the screen and a block, and is called every frame.
### *check_passed*
Checks if the player has passed the gap of a wall, and is called every frame. Either the top or bottom block would work in this scenario, but I arbtirarily chose the bottom block for checking.
### *save*
Writes any changes in save data into the json file.
### *options_menu*
The loop of the options menu that is called when the options button is pressed in the start menu, and contains all the functionality of the options menu. This was originally part of **main.py**, but ended up being moved into **functions.py** because of how cluttered and nested it ended up at the end. Since the options menu loop resides for loop event queue, of which already has if/else statements, not extracting this part made reading the code very annoying, since it was so heavily nested.

## **main.py**
This file contains all of the loops used to run the game, along with where all the functions in **functions.py** are used. 
### *Event Queues*
These are the for loops that preside in each while loop, and was also present in the options menu loop that was in **functions.py**. These loops are for processing a queue of events that pygame registers. Event queues are used instead of detecting an input directly in the loop so that there would not be any input dropping, in case multiple buttons were clicked for example. There is a lot of mouse motion involved in playing the game, and since the act of moving the mouse itself does not have any functionality in the game, it was excluded. Some of these loops use match cases, while others use if/else statements, this is solely due to me trying to get used to the syntax of match cases earlier on in development. Each event needs to be further broken down into specific keys pressed, in which all functionality associated with that key resides.
### *Game Loops*
The game_running loop comprises of the entire game, where on start-up the start menu is loaded in. The loop comprises of drawing the start menu (or skipping the drawing if skip_start_menu is True), a for loop to process event queue for user input, the in_game loop that comprises the main game, the game_over loop that comprises of the game over menu, and the options_menu loop located within the for loop that comprises the options menu. The in_game loop is runs at 120 tps (ticks per second) and was set to that because most games I have played usually run at that rate. The tick rate was limited because the loop would be too fast for the player to be able to control the player properly, since physics calculations are done on a per tick basis. The menus were arbtirarily set to 60 tps, since menu navigation can get away with using lower tps.
### *Boolean Variables*
These were used to determine whether to enter a loop, along with determining whether an action should be preformed or not, with exception to game_running which will always be True as long as the program is running. Swapping between menus and determining actions of button clicks consists of setting these values in true or false depending on what was pressed. For example, the restart button in the pause menu consists of setting skip_start_menu to True so that the menu can be skipped, then setting ingame to False, so that it can immediately exit the current session and start a new session. 