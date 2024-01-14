import pygame as game
from random import randint
import variables
from functions import *
from classes import *

game.init()
game.mixer.init()
# initialize all variables
variables.init()

# adjust volume settings based on last session
set_volumes(variables.sfx_volume, variables.bgm_volume)

variables.bgm.load('Sounds/startmenu_bgm.wav')
variables.bgm.play(loops=-1, fade_ms=8000)

while variables.game_running:

    # only happens when retry or restart is clicked, skip drawing the start menu
    if variables.skip_start_menu == False:
        draw_menu(variables.start_menu_buttons, variables.background)
    
    # immediately start game and skip drawing menu
    else:
        variables.ingame = True
        initialize_ingame_assets()
    
    # Checks player inputs in start menu
    for event in game.event.get(exclude=game.MOUSEMOTION):
        # check what event type and react appropriately
        match event.type:
            # close game when window is closed
            case game.QUIT:
                close_game()
            
            # where a mouse is clicked
            case game.MOUSEBUTTONDOWN:
                mouse_pos = game.mouse.get_pos()
                
                # stops proceeding if the clicked button isn't left click
                if event.button != 1:
                    continue
                
                clicked_button = check_clicked(variables.start_menu_buttons, mouse_pos)
                
                # handles start button clicked
                if clicked_button == variables.start_button:
                    variables.ingame = True
                    variables.click_sound.play()
                    initialize_ingame_assets()
                
                # handles options button clicked
                elif clicked_button == variables.option_button:
                    variables.click_sound.play()
                    options_menu()

                # handles the quit button by closing game
                elif clicked_button == variables.quit_button:
                    close_game()

    # enter the game
    while variables.ingame:
        # in case player presses quit instead of retry later on, so start menu can be drawn again
        variables.skip_start_menu = False

        # shift where grapple point is by having it scroll with the environment
        if variables.player.grapple_state == True:
            mouse_pos = (mouse_pos[0]+variables.scroll_spd, mouse_pos[1])

        # Checks player inputs
        for event in game.event.get(exclude=game.MOUSEMOTION):
            match event.type:
                case game.QUIT:
                    close_game()

                case game.MOUSEBUTTONDOWN:
                    # get coordinates to use for drawing and calculating trajectory
                    mouse_pos = game.mouse.get_pos()

                    # toggles between grappling and ungrappling
                    if event.button == 1 and variables.player.grapple_state == False:
                        variables.player.grapple_state = True
                        variables.shoot_sound.play()
                    else:
                        variables.player.grapple_state = False

                # handles keyboard presses
                case game.KEYDOWN:
                    match event.key:
                        # handles the escape key being pressed
                        case game.K_ESCAPE:

                            # go into the options menu w/ function, returns string representing the button that was pressed in the options menu
                            action_needed = pause_game()

                            # handles quit function by returning to main menu
                            if action_needed == 'quit':
                                variables.bgm.unload()
                                variables.bgm.load('Sounds/startmenu_bgm.wav')
                                variables.bgm.play(loops=-1, fade_ms=8000)
                                variables.skip_start_menu = False
                                variables.ingame = False

                            # handles restart by exiting immediately and skipping start menu
                            elif action_needed == 'restart':
                                variables.skip_start_menu = True
                                variables.ingame = False
                                                
        # update the player speed and move them
        if variables.player.grapple_state == True:
            variables.player.update_speed(mouse_pos, variables.accel)
        variables.player.speed[1] += variables.gravity

        # for animating chracter, uses mouse_pos to determine where end point of grapple point
        variables.player.animate(mouse_pos)

        move_blocks(variables.scroll_spd, variables.block1_top, variables.block1_bot, variables.block2_top, variables.block2_bot)
        handle_collision(variables.ground, variables.ceiling, variables.block1_top, variables.block1_bot, variables.block2_top, variables.block2_bot)
        variables.player.move()

        # keep player in camera
        variables.player.hitbox.clamp_ip(0,0,variables.width,variables.height)


        if check_death(variables.block1_top, variables.block1_bot, variables.block2_top, variables.block2_bot) == True:
            # exit loop and enable gameover menu
            variables.ingame = False
            variables.game_over = True
            variables.player.grapple_state = False
            variables.player.change_frame('dead')
            variables.oof_sound.play()
            variables.bgm.stop()

            # play falling animation
            while variables.player.hitbox.bottom < variables.height-20:  
                variables.player.speed = [0,3]
                variables.player.move()
                draw_ingame_assets(mouse_pos, False) 

            # clear queues in which clicks were done during falling animation
            game.event.clear()
        if check_passed(variables.block1_bot, variables.block2_bot) == True:
            variables.player.score += 1
            variables.ding_sound.play()

            # 50% chance that the scroll speed increases per pass
            if randint(0,1) == 1:
                variables.scroll_spd -= 0.1

        draw_ingame_assets(mouse_pos)

        # cap tick-rate to 120ps
        variables.clock.tick(120)

    # save the score to file if a highscore was achieved
    if variables.player.score > variables.highest_score:
        variables.highest_score = variables.player.score
        # save high score
        save()
    
    # limit framerate to 60 in menu
    variables.clock.tick(60)

    # enter game over menu
    while variables.game_over:
        variables.clock.tick(60)
        draw_gameover()
        for event in game.event.get(exclude=game.MOUSEMOTION):
            if event.type == game.QUIT:
                close_game()
            elif event.type == game.MOUSEBUTTONDOWN:
                mouse_pos = game.mouse.get_pos()
                if event.button != 1:
                    continue
                clicked_button = check_clicked(variables.gameover_menu_items, mouse_pos)

                # go into the game again immediately via skipping start menu
                if clicked_button == variables.retry_button:
                    variables.click_sound.play()
                    variables.game_over = False
                    variables.skip_start_menu = True

                elif clicked_button == variables.quit_button:
                    variables.game_over = False
                    variables.click_sound.play()
                    variables.bgm.unload()
                    variables.bgm.load('Sounds/startmenu_bgm.wav')
                    variables.bgm.play(loops=-1, fade_ms=8000)


