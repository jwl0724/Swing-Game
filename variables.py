import pygame as game
from classes import *
import json

def init():
    # set all variables to be used in different files
    global ingame, game_running, game_over, skip_start_menu, height, width, screen, clock, accel, gravity, scroll_spd, block_width
    global highest_score, bgm_volume, sfx_volume, difficulty, background, player, ground, ceiling, block1_bot, block1_top, block2_bot, block2_top
    global start_menu_buttons, gameover_menu_items, pause_menu_items, options_menu_items, click_sound, ding_sound, oof_sound, shoot_sound, bgm
    global start_button, difficulty_button, option_button, sfx_button, bgm_button, back_button, quit_button, restart_button, resume_button, retry_button

    ingame, game_running, game_over, skip_start_menu = False, True, False, False
    width, height = 1080, 800
    screen = game.display.set_mode((width, height))
    clock = game.time.Clock()
    accel, gravity = 0.3, 0.075
    block_width = 120

    # load data from previous sessions
    try:
        with open('data.json', 'r') as infile:
            saved_data = json.load(infile)
    # if no save exists, make new save file
    except FileNotFoundError:
        saved_data = {"high_score": 0, "sfx_settings": 10, "bgm_settings": 10, "difficulty": 1}
        with open('data.json', 'w') as outfile:
            json.dump(saved_data, outfile, indent=4)

    # load data into variables
    try:
        highest_score = saved_data['high_score']
        bgm_volume = saved_data['bgm_settings']
        sfx_volume = saved_data['sfx_settings']
        difficulty = saved_data['difficulty']
    # if the file doesnt have the correct values
    except KeyError:
        saved_data = {"high_score": 0, "sfx_settings": 10, "bgm_settings": 10, "difficulty": 1}
        with open('data.json', 'w') as outfile:
            json.dump(saved_data, outfile, indent=4) 

        highest_score = saved_data['high_score']
        bgm_volume = saved_data['bgm_settings']
        sfx_volume = saved_data['sfx_settings']
        difficulty = saved_data['difficulty']

    # make background
    background = background_class('Images/Cave_Background.png')

    # get all the animation frames listed
    start_button_frames = ['Images/Buttons/button_start_default.png', 'Images/Buttons/button_start_hover.png']
    options_button_frames = ['Images/Buttons/button_options_default.png', 'Images/Buttons/button_options_hover.png']
    quit_button_frames = ['Images/Buttons/button_quit_default.png', 'Images/Buttons/button_quit_hover.png']
    retry_button_frames = ['Images/Buttons/button_retry_default.png', 'Images/Buttons/button_retry_hover.png']
    resume_button_frames = ['Images/Buttons/button_resume_default.png', 'Images/Buttons/button_resume_hover.png']
    restart_button_frames = ['Images/Buttons/button_restart_default.png', 'Images/Buttons/button_restart_hover.png']
    back_button_frames = ['Images/Buttons/button_back_default.png', 'Images/Buttons/button_back_hover.png']
    difficulty_button_frames = ['Images/Buttons/button_easy_default.png', 'Images/Buttons/button_easy_hover.png', 'Images/Buttons/button_medium_default.png', 'Images/Buttons/button_medium_hover.png',
                                'Images/Buttons/button_hard_default.png', 'Images/Buttons/button_hard_hover.png', 'Images/Buttons/button_dont_default.png', 'Images/Buttons/button_dont_hover.png']
    player_animation_frames = ['Images/Animations/player_frame_falling.png', 'Images/Animations/player_frame_grappled.png', 'Images/Animations/player_frame_dead.png',
                            'Images/Animations/player_frame_roll1.png', 'Images/Animations/player_frame_roll2.png', 'Images/Animations/player_frame_roll3.png', 'Images/Animations/player_frame_roll4.png']
    sfx_button_frames = ['Images/Buttons/button_0_default.png', 'Images/Buttons/button_0_hover.png',
                        'Images/Buttons/button_1_default.png', 'Images/Buttons/button_1_hover.png', 'Images/Buttons/button_2_default.png', 'Images/Buttons/button_2_hover.png',
                        'Images/Buttons/button_3_default.png', 'Images/Buttons/button_3_hover.png','Images/Buttons/button_4_default.png', 'Images/Buttons/button_4_hover.png',
                        'Images/Buttons/button_5_default.png', 'Images/Buttons/button_5_hover.png','Images/Buttons/button_6_default.png', 'Images/Buttons/button_6_hover.png',
                        'Images/Buttons/button_7_default.png', 'Images/Buttons/button_7_hover.png','Images/Buttons/button_8_default.png', 'Images/Buttons/button_8_hover.png',
                        'Images/Buttons/button_9_default.png', 'Images/Buttons/button_9_hover.png','Images/Buttons/button_10_default.png', 'Images/Buttons/button_10_hover.png']
    bgm_button_frames = sfx_button_frames

    # create all the elements
    player, ground, ceiling = player_avatar(player_animation_frames), collidable('Images/Ground.png'), collidable('Images/Ground.png')
    block1_top, block1_bot, block2_top, block2_bot = collidable('Images/Light.png'), collidable('Images/crates.png'), collidable('Images/Light.png'), collidable('Images/crates.png')
    title, start_button, option_button = menu_item('Images/Swing Title.png', False), menu_item(start_button_frames), menu_item(options_button_frames)
    quit_button, retry_button, resume_button = menu_item(quit_button_frames), menu_item(retry_button_frames), menu_item(resume_button_frames)
    restart_button, back_button, difficulty_button = menu_item(restart_button_frames), menu_item(back_button_frames), menu_item(difficulty_button_frames)
    sfx_button, bgm_button, bgm_text, sfx_text = menu_item(sfx_button_frames), menu_item(bgm_button_frames), menu_item('Images/BGM.png', False), menu_item('Images/SFX.png', False)

    # bundle the buttons to the correct menu layouts
    start_menu_buttons = [title, start_button, option_button, quit_button]
    gameover_menu_items = [retry_button, quit_button]
    pause_menu_items = [resume_button, restart_button, quit_button]
    options_menu_items = [sfx_text, sfx_button, bgm_text, bgm_button, difficulty_button, back_button] # w/ volume slider to adjust sound (master volume)

    # initialize all sound assets
    click_sound = game.mixer.Sound('Sounds/click.wav')
    ding_sound = game.mixer.Sound('Sounds/ding.wav')
    oof_sound = game.mixer.Sound('Sounds/oof.wav')
    shoot_sound = game.mixer.Sound('Sounds/bow_shoot.wav')
    bgm = game.mixer.music

    # set scroll speed using difficulty, and button index
    match difficulty:
        case 0:
            scroll_spd = -1
            difficulty_button.button_index = 0
        case 1:
            scroll_spd = -2
            difficulty_button.button_index = 1
        case 2:
            scroll_spd = -3
            difficulty_button.button_index = 2
        case 3:
            scroll_spd = -6
            difficulty_button.button_index = 3