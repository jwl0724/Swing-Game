import pygame as game
from classes import *
import variables
from random import randint
import json
import sys

# set volume of everythign based on settings
def set_volumes(sfx_val, bgm_val):
    match sfx_val:
        case 0:
            sfx_volume = 0
        case 1:
            sfx_volume = 0.1
        case 2:
            sfx_volume = 0.2
        case 3:
            sfx_volume = 0.3
        case 4:
            sfx_volume = 0.4
        case 5:
            sfx_volume = 0.5
        case 6:
            sfx_volume = 0.6
        case 7:
            sfx_volume = 0.7
        case 8:
            sfx_volume = 0.8
        case 9:
            sfx_volume = 0.9
        case 10:
            sfx_volume = 1

    match bgm_val:
        case 0:
            bgm_volume = 0
        case 1:
            bgm_volume = 0.1
        case 2:
            bgm_volume = 0.2
        case 3:
            bgm_volume = 0.3
        case 4:
            bgm_volume = 0.4
        case 5:
            bgm_volume = 0.5
        case 6:
            bgm_volume = 0.6
        case 7:
            bgm_volume = 0.7
        case 8:
            bgm_volume = 0.8
        case 9:
            bgm_volume = 0.9
        case 10:
            bgm_volume = 1       

    variables.click_sound.set_volume(sfx_volume)
    variables.ding_sound.set_volume(sfx_volume)
    variables.oof_sound.set_volume(sfx_volume)
    variables.shoot_sound.set_volume(sfx_volume)
    variables.variables.bgm.set_volume(bgm_volume)    

# draw the buttons of a given list of menu items
def draw_buttons(menu_items):
    mouse_pos = game.mouse.get_pos()
    for i in range(len(menu_items)):
        button = menu_items[i]

        # for elements that don't have animation frames 
        if button.hover_frames == None:
            variables.screen.blit(button.sprite, button.hitbox)
            continue
    
        # for regular buttons, try is used for first frames where mouse_pos does not exist
        try:
            if button.hitbox.collidepoint(mouse_pos) == True:
                button.change_frame('hover')
            else:
                button.change_frame('default')
        except TypeError:
            button.change_frame('default')

# centers the buttons, has option to input gap b/n buttons, and choose how high first element is
def align_buttons(menu_items, gap, first_element_height):
    for i in range(len(menu_items)):
        # set first element based on inputted height
        if i == 0:
            menu_items[i].position_item(first_element_height)
            continue

        # subsequent elements go directly underneath last element placed
        menu_items[i].position_item(menu_items[i-1].hitbox.bottom+gap)

# draws all of the menus
def draw_menu(menu_items, bg=None, gap=30, first_element_height=30):
    # draw background first
    if bg != None:
        variables.background.print()

    # align buttons to center and update display to show buttons
    align_buttons(menu_items, gap, first_element_height)
    draw_buttons(menu_items)
    game.display.flip()

# returns the button in the menu that was clicked
def check_clicked(menu_items, mouse_pos):
    for i in range(len(menu_items)):
        if menu_items[i].hitbox.collidepoint(mouse_pos) == True and menu_items[i].clickable == True:
            return menu_items[i]
    return None

# pause loop
def pause_game():
    paused = True
    while paused:
        draw_menu(variables.pause_menu_items, first_element_height=variables.width/5)

        # read player inputs
        for event in game.event.get(exclude=game.MOUSEMOTION):
            match event.type:
                case game.QUIT:
                    close_game()
                case game.MOUSEBUTTONDOWN:
                    if event.button != 1:
                        continue
                    mouse_pos = game.mouse.get_pos()
                    clicked_button = check_clicked(variables.pause_menu_items, mouse_pos)

                    # do nothing when resume button pressed
                    if clicked_button == variables.resume_button:
                        variables.click_sound.play()
                        return None
                    
                    # tell outside that restart was pressed
                    elif clicked_button == variables.restart_button:
                        variables.click_sound.play()
                        return 'restart'
                    
                    # tell outside quit was pressed
                    elif clicked_button == variables.quit_button:
                        variables.click_sound.play()
                        return 'quit'

                # unpause the game by pressing esc
                case game.KEYDOWN:
                    if event.key == game.K_ESCAPE:
                        paused = False

    return None

# called when game is closed
def close_game():
    game.display.quit()
    game.quit()
    sys.exit()

# randomizes block gaps
def randomize_block(block_top, block_bot, spawn_location):
    # randomize size of gap
    min_gap_size = variables.player.hitbox.height+60
    max_gap_size = variables.player.hitbox.height+160
    gap_size = randint(min_gap_size, max_gap_size)
    
    # randomize where gap will be
    gap_location_top_bound = 120
    gap_location_bot_bound = variables.height - 120 - gap_size
    gap_location = randint(gap_location_top_bound, gap_location_bot_bound)

    # calculate the height of the block at the bottom
    block_bot_size = variables.height - gap_location - gap_size

    # adjust image based on size of block
    if block_bot_size < variables.height/2-100:
        block_bot.sprite = game.image.load('Images/Block.png')
    elif block_bot_size > variables.height/2:
        block_bot.sprite = game.image.load('Images/crates.png')
    if gap_location > variables.height/2:
        block_top.sprite = game.image.load('Images/Light.png')
    elif gap_location < variables.height/2-100:
        block_top.sprite = game.image.load('Images/planter.png')

    # scale the blocks with what was calculated and spawn them in
    block_top.scale_sprite(spawn_location, 0, variables.block_width, gap_location)
    block_bot.scale_sprite(spawn_location, variables.height-block_bot_size, variables.block_width, block_bot_size)

# Usage: block pairings, top first then bottom
def move_blocks(scroll_spd, *blocks):
    for i in [0,2]:
        if blocks[i].hitbox.right < 0:
            randomize_block(blocks[i], blocks[i+1], variables.width+variables.width/1.5)
            blocks[i+1].passed = False
        else:
            if variables.player.speed[0] > abs(scroll_spd) and variables.player.hitbox.right > variables.width*0.65:
                blocks[i].move(-variables.player.speed[0]+scroll_spd)
                blocks[i+1].move(-variables.player.speed[0]+scroll_spd)
            else:
                blocks[i].move(scroll_spd)
                blocks[i+1].move(scroll_spd)

# reset all values to initial state
def initialize_ingame_assets():
    # move variables.player to center of arena and reset all values
    variables.player.hitbox.update(variables.width/2, variables.height/2, variables.player.hitbox[2], variables.player.hitbox[3])
    variables.player.speed = [0,0]
    variables.player.grapple_state = False
    variables.player.sprite = game.image.load(variables.player.animation_frames['fall'])

    # make ground and ceiling
    variables.ground.scale_sprite(0, variables.height-20, variables.width, 20)
    variables.ceiling.scale_sprite(0, 0, variables.width, 20)

    # make obstacles
    randomize_block(variables.block1_top, variables.block1_bot, variables.width)
    randomize_block(variables.block2_top, variables.block2_bot, variables.width+variables.width)  

    # reset score and set passed bools to false
    variables.player.score = 0
    variables.block1_bot.passed, variables.block2_bot.passed = False, False  
    variables.background.left = 0

    # start bgm
    variables.bgm.load('Sounds/ingame_bgm.wav')
    variables.bgm.play(loops=-1)

    # resets scroll speed to default difficulty
    match variables.difficulty:
        case 0:
            variables.scroll_spd = -1
            variables.difficulty_button.button_index = 0
        case 1:
            variables.scroll_spd = -2
            variables.difficulty_button.button_index = 1
        case 2:
            variables.scroll_spd = -3
            variables.difficulty_button.button_index = 2
        case 3:
            variables.scroll_spd = -6
            variables.difficulty_button.button_index = 3

# draws number at the center of the screen, based on height
def render_score(int_score, height):
    score = str(int_score)
    separator = 0
    for i in range(len(score)):
        match score[i]:
            case '0':
                num = game.image.load('Images/Numbers/0.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '1':
                num = game.image.load('Images/Numbers/1.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '2':
                num = game.image.load('Images/Numbers/2.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '3':
                num = game.image.load('Images/Numbers/3.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '4':
                num = game.image.load('Images/Numbers/4.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '5':
                num = game.image.load('Images/Numbers/5.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '6':
                num = game.image.load('Images/Numbers/6.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '7':
                num = game.image.load('Images/Numbers/7.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '8':
                num = game.image.load('Images/Numbers/8.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
            case '9':
                num = game.image.load('Images/Numbers/9.png')
                variables.screen.blit(num, (variables.width/2-num.get_width()*(len(score)/2-i)+separator, height))
        separator += 1

# calls every frame to draw game assets
def draw_ingame_assets(mouse_pos, scrolling=True):

    # draw background
    if scrolling == True:
        variables.background.scroll(int(variables.scroll_spd))
    else:
        variables.screen.blit(variables.background.bg, (variables.background.left, 0))
        variables.screen.blit(variables.background.bg, (variables.width+variables.background.left, 0))

    # draw grapple line
    if variables.player.grapple_state == True:
        # draws line to the left when the point is left of player, so sprite will flip and look towards left
        if variables.player.hitbox.left > mouse_pos[0]:
            game.draw.line(variables.screen, (0,0,0), (variables.player.hitbox.left+10, variables.player.hitbox.top+10), mouse_pos, 5)
        else:
            game.draw.line(variables.screen, (0,0,0), (variables.player.hitbox.right-10, variables.player.hitbox.top+10), mouse_pos, 5)
        # draws a cloud at the end point of line, where line end point is center of cloud
        grapple_cloud = game.image.load('Images/Cloud.png')
        variables.screen.blit(grapple_cloud, (mouse_pos[0]-grapple_cloud.get_width()/2, mouse_pos[1]-grapple_cloud.get_height()/2))

    # draw all assets
    variables.screen.blits(blit_sequence=[(variables.player.sprite, variables.player.hitbox), (variables.block1_bot.sprite, variables.block1_bot.hitbox),
                                (variables.block1_top.sprite, variables.block1_top.hitbox), (variables.block2_bot.sprite, variables.block2_bot.hitbox),
                                (variables.block2_top.sprite, variables.block2_top.hitbox), (variables.ground.sprite, variables.ground.hitbox), 
                                (variables.ceiling.sprite, variables.ceiling.hitbox)])
    
    # draws number
    render_score(variables.player.score, 40)

    # update the display
    game.display.flip()    

# called every frame during game over
def draw_gameover():
    # redraw all of the backgrounds at the time of death
    variables.screen.blit(variables.background.bg, (variables.background.left, 0))
    variables.screen.blit(variables.background.bg, (variables.width+variables.background.left, 0))
    variables.screen.blits(blit_sequence=[(variables.player.sprite, variables.player.hitbox), (variables.block1_bot.sprite, variables.block1_bot.hitbox),
                                (variables.block1_top.sprite, variables.block1_top.hitbox), (variables.block2_bot.sprite, variables.block2_bot.hitbox),
                                (variables.block2_top.sprite, variables.block2_top.hitbox), (variables.ground.sprite, variables.ground.hitbox), 
                                (variables.ceiling.sprite, variables.ceiling.hitbox)])
    
    # overlay everything with the score and highscore messages
    score_message = game.image.load('Images/you_scored.png')
    highscore_message = game.image.load('Images/high_score.png')  
    variables.screen.blit(score_message, (variables.width/2-score_message.get_width()/2, 10))
    variables.screen.blit(highscore_message, (variables.width/2-highscore_message.get_width()/2, 200))
    render_score(variables.player.score, score_message.get_height()+25)
    render_score(variables.highest_score, highscore_message.get_height()*2+115) 

    # draw the gameover menu over the background
    draw_menu(variables.gameover_menu_items, gap=50, first_element_height=variables.height/2)

# called everyframe to check for collisions
def handle_collision(*obstacles):
    for i in range(len(obstacles)):
        obstacle_x_dimension = range(obstacles[i].next_step(variables.scroll_spd).left, obstacles[i].next_step(variables.scroll_spd).right)
        obstacle_y_dimension = range(obstacles[i].next_step(variables.scroll_spd).top, obstacles[i].next_step(variables.scroll_spd).bottom)
        
        # handle vertical collisions
        if (variables.player.next_step().top in obstacle_y_dimension or variables.player.next_step().bottom in obstacle_y_dimension) and game.Rect.colliderect(variables.player.next_step(), obstacles[i].hitbox) == True:
            variables.player.speed[1] = -variables.player.speed[1]*0.5

        # handle left side collisions
        if variables.player.next_step().right in obstacle_x_dimension and game.Rect.colliderect(variables.player.next_step(), obstacles[i].hitbox) == True:
            variables.player.speed[0] = abs(variables.scroll_spd+variables.player.speed[0]*0.5)*-1

        # handle right side collisions
        if variables.player.next_step().left in obstacle_x_dimension and game.Rect.colliderect(variables.player.next_step(), obstacles[i].hitbox) == True:
            variables.player.speed[0] = -variables.player.speed[0]*0.5
    
# called every frame to check if player has died
def check_death(*obstacles):
    for i in range(len(obstacles)):
        if game.Rect.colliderect(variables.player.hitbox, obstacles[i].hitbox) == True and variables.player.hitbox.left < 1:
            return True
    return False

# checked every frame to see if player passed a gap
def check_passed(*obstacles_bot):
    for i in range(len(obstacles_bot)):
        if variables.player.hitbox.left > obstacles_bot[i].hitbox.right and obstacles_bot[i].passed == False:
            obstacles_bot[i].passed = True
            return True
    return False

# saves settings and score to file
def save():
    with open('data.json', 'w') as outfile:
        json_dump = {'high_score': variables.highest_score, 'sfx_settings': variables.sfx_volume, 'bgm_settings': variables.bgm_volume, 'difficulty': variables.difficulty}
        json.dump(json_dump, outfile, indent=4)

# enter options menu
def options_menu():
    in_options = True
    # enter a loop for options menu
    while in_options:
        # determine which buttons to draw based on last settings
        match variables.difficulty:
            case 0:
                variables.difficulty_button.button_index = 0
            case 1:
                variables.difficulty_button.button_index = 1
            case 2:
                variables.difficulty_button.button_index = 2
            case 3:
                variables.difficulty_button.button_index = 3

        # volume is saved via 0 to 10, the volume setting = the index
        variables.sfx_button.button_index = variables.sfx_volume
        variables.bgm_button.button_index = variables.bgm_volume
        
        # draws menu 
        draw_menu(variables.options_menu_items, variables.background, first_element_height=10)

        # read player input in options menu
        for event in game.event.get(exclude=game.MOUSEMOTION):
            if event.type == game.QUIT:
                close_game()
            
            elif event.type == game.MOUSEBUTTONDOWN:
                mouse_pos = game.mouse.get_pos()
                if event.button != 1:
                    continue
                
                clicked_button = check_clicked(variables.options_menu_items, mouse_pos)
                
                # handles back button in options menu
                if clicked_button == variables.back_button:
                    in_options = False
                    variables.click_sound.play()
                
                # cycles thru difficulty button
                elif clicked_button == variables.difficulty_button:
                    # reset index once it reaches last element
                    if variables.difficulty_button.button_index == 3:
                        variables.difficulty_button.button_index = 0
                        variables.difficulty = 0
                    else:
                        variables.difficulty_button.button_index += 1
                        variables.difficulty += 1
                    variables.click_sound.play()
                
                # cycles thru sfx buttons
                elif clicked_button == variables.sfx_button:
                    # reset index
                    if variables.sfx_button.button_index == 10:
                        variables.sfx_button.button_index = 0
                        variables.sfx_volume = 0
                    else:
                        variables.sfx_button.button_index += 1
                        variables.sfx_volume += 1
                    
                    # update sounds immediately
                    set_volumes(variables.sfx_volume, variables.bgm_volume)
                    variables.click_sound.play()

                # cycles thru bgm buttons
                elif clicked_button == variables.bgm_button:
                    if variables.bgm_button.button_index == 10:
                        variables.bgm_button.button_index = 0
                        variables.bgm_volume = 0
                    else:
                        variables.bgm_button.button_index += 1
                        variables.bgm_volume += 1
        
                    set_volumes(variables.sfx_volume, variables.bgm_volume)  
                    variables.click_sound.play()
                
                # saves all the changed options immediately
                save()               
