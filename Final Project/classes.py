import pygame as game
import variables
from math import sqrt

class player_avatar:
    def __init__(self, frames):
        self.sprite = game.image.load(frames[0])
        self.hitbox = self.sprite.get_rect()
        self.grapple_state = False
        self.speed = [0,0]
        self.animation_frames = {'fall': frames[0], 'grapple': frames[1], 'dead': frames[2], 'roll': [frames[3], frames[4], frames[5], frames[6]]}
        self.roll_frame = 0
        self.score = 0
        
    def change_frame(self, action, mouse_pos=None):
        match action:
            case 'fall':
                self.sprite = game.image.load(self.animation_frames[action])
                variables.screen.blit(self.sprite, self.hitbox)
            case 'grapple':
                self.sprite = game.image.load(self.animation_frames[action])
                if variables.player.hitbox.left > mouse_pos[0]:
                    self.sprite = game.transform.flip(self.sprite, True, False)
                variables.screen.blit(self.sprite, self.hitbox)
            case 'roll':
                if self.roll_frame == 4:
                    self.roll_frame = 0
                self.sprite = game.image.load(self.animation_frames[action][self.roll_frame])
                variables.screen.blit(self.sprite, self.hitbox)
                self.roll_frame += 1
            case 'dead':
                self.sprite = game.image.load(self.animation_frames[action])
                variables.screen.blit(self.sprite, self.hitbox)

    def animate(self, mouse_pos):
        if self.grapple_state == True:
            self.change_frame('grapple', mouse_pos)
        elif self.speed[1] <= 0:
            self.change_frame('roll')    
        elif self.speed[1] >= 1.5:
            self.change_frame('fall')        

    def update_speed(self, grapple_pos, acceleration):
        # get all sides of the triangle
        opposite = grapple_pos[1] - self.hitbox[1]
        adjacent = grapple_pos[0] - self.hitbox[0]
        hypotenuse = sqrt(opposite**2 + adjacent**2)
        
        # Zcos0 (x-component), Zsin0 (y-component) -> cos0 = adj/hyp, sin0 = opp/hyp -> Z(adj/hyp) for x-component, etc... where Z = accel
        try:
            self.speed[0] += acceleration*adjacent/hypotenuse
            self.speed[1] += acceleration*opposite/hypotenuse
        # hypotenuse is 0 when mouse is directly on top of character, therefore no speed gained
        except ZeroDivisionError:
            pass

    def move(self):
        self.hitbox = self.hitbox.move(self.speed)

    # for collision checks
    def next_step(self):
        next_frame_hitbox = self.hitbox.move(self.speed)
        return next_frame_hitbox
        
class collidable:
    def __init__(self, img_file):
        self.sprite = game.image.load(img_file)
        self.hitbox = self.sprite.get_rect()
        self.passed = False

    # adjust size of image to fit with randomized sizes 
    def scale_sprite(self, left, top, rect_width, rect_height):
        self.hitbox.update(left, top, rect_width, rect_height)
        self.sprite = game.transform.scale(self.sprite, (rect_width, rect_height))

    def move(self, scroll_spd):
        speed = (scroll_spd, 0)
        self.hitbox = self.hitbox.move(speed)

    def next_step(self, scroll_spd):
        next_frame_hitbox = self.hitbox.move((scroll_spd, 0))
        return next_frame_hitbox

class menu_item:
    def __init__(self, frames, clickable=True):
        
        # handle 1 frame elements
        if type(frames) == str:
            self.sprite = game.image.load(frames)
            self.hitbox = self.sprite.get_rect()
            self.default_frames = None
            self.hover_frames = None
        
        # handle multiple animation frames
        else:
            self.sprite = game.image.load(frames[0])
            self.hitbox = self.sprite.get_rect()
            self.default_frames = []
            self.hover_frames = []
            self.button_index = 0

            # cycle thru all the frames
            for i in range(len(frames)):
                if i%2 == 0:
                    self.default_frames.append(frames[i])
                else:
                    self.hover_frames.append(frames[i])

        if clickable == True:
            self.clickable = True
        else:
            self.clickable = False

    # centers buttons 
    def position_item(self, y):
        self.hitbox.update(0, y, self.hitbox.width, self.hitbox.height)
        self.hitbox.center = (variables.width/2, self.hitbox.center[1])

    # changes button b/n hover and non-hover appearances, either hover and not hover
    def change_frame(self, state):
        if state == 'default':
            self.sprite = game.image.load(self.default_frames[self.button_index])
            variables.screen.blit(self.sprite, self.hitbox)
        else:
            self.sprite = game.image.load(self.hover_frames[self.button_index])        
            variables.screen.blit(self.sprite, self.hitbox)

class background_class:
    def __init__(self, img_file):
        self.bg = game.image.load(img_file).convert()
        self.bg = game.transform.scale(self.bg, (variables.width,variables.height))

        # save where the position of the left of the background is so it can properly loop
        self.left = 0

    def reset_bg(self):
        self.left = 0

    def scroll(self, scroll_spd):
        variables.screen.blit(self.bg, (self.left, 0))
        variables.screen.blit(self.bg, (variables.width+self.left, 0))

        # draw background on the right again
        if self.left <= -variables.width:
            variables.screen.blit(self.bg, (variables.width+self.left, 0))
            self.left = 0
        self.left += scroll_spd
    
    # draws static background
    def print(self):
        variables.screen.blit(self.bg, (0,0))

