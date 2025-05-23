#some global variables that is used by modules
#according to tutorial its better to keep it seperate so that its easier to fix, if shit hits the fan


import math

#making music lists 

music_list = []
lobbyMusic = 'Drops of H2O_FULL'
scoreboardMusc = 'Another way_FULL'

# chart update : If you want to update chart, you should change the flag to True
#this is to let usage of custom charts, if one is wanted
update_chart_flag = True

# player settings
stage_speed = 80
offset = 0
judgement_shown = False
guide_line_shown = False
music_pointer = 1 # 4
song_name = None # as a default
song_info_list = []

high_quality_verifying_graphics = False
sound_effect = [True]
particle_effect = [True]

creater_mode = False

# time settings
fps = 60 #120 # 60
main_loop_render_fps = 60

max_speed = 100 # (float) pixels/100 milliseconds
min_speed = 15
max_offset = 1000
min_offset = -1000

# screen settings
line_number = 6
line_width = 120
#######
width = line_number * line_width
#######
line_axes = [(line_width//2) + line_width*(i+1) for i in range(line_number)]


option_key_x_level = width//2
option_key_y_level = 350

song_selection_key_x_level = width//2
song_selection_key_y_level = 550

button_y_offset = 25
button_x_size, button_y_size = 440,50


# node info
node_height = 20
# note that node width is equal to line_width

info_length = 200
line_lengths = [700,800]
line_length_idx = 0 # unchanged
line_length = line_lengths[line_length_idx]

#######
height = line_length + info_length # this is equal to 'border line' position
#######
node_spawning_y_pos = info_length + node_height//2

judgement_line_depth = node_height//2 + int(5 * (1000/60))  #node_height//2 + int(5 * (1000/fps)) # node_height//2 + ((max_speed//2) * (1000/fps))
judgement_line = height - judgement_line_depth


# frame settings
guide_keys = ['F','G','H','J']
guide_key_size = len(guide_keys)
guide_y_loc = (judgement_line) + 50
guide_x_loc = line_width//2 + line_width


# some color settings
background_color = [(40, 40, 30),(215, 215, 225)]
line_color = (240,240,235)

node_color = [(180,180,180),(80, 80, 70)]

hold_color = [(190,190,190),(80,80,70)] # listify
holding_middle_color = (160,160,160)
not_holding_middle_color = (120,120,120)


bad_apple_color = (240, 180, 180)
bad_apple_toggled_color = (0,0,0)
red_color = (150,25,25)
debug_color = (241, 196, 15)

score_grades = ['Pure Perfect!!! (PP)','Perfect (P)','AA','A','B','C','D','E','Failed']


score_colors = {'Pure Perfect!!! (PP)':(220,240,255),'Perfect (P)':(200,230,255),'AA':(255,223,79),'A':(230,200,50),'B':(169,194,169),'C':(200,200,240),'D':(240, 180, 180),'E':(210, 160, 160),'Failed':(160,160,160)}


def make_color_lighter(color):
    return min(color+100,255)

judgement_line_color = (make_color_lighter(background_color[0][0]),make_color_lighter(background_color[0][1]),make_color_lighter(background_color[0][2]))

# text settings
default_text_color = (0,220,220)
dark_text_color = (default_text_color[0]//2+10, default_text_color[1]//2+50, default_text_color[2]//2+50)
highlight_text_color = (200,230,255)
red_highlight_text_color = (240, 180, 180)
bar_color = (90,90,90)


frame_alpha_max = 100
frame_alpha = 0
frame_cycle = 2
frame_phase = 1/frame_cycle
frame_grad_color = 0

giant_text = 200
title_text = 50
sticker_text = title_text
big_text = 35
small_text = 20  
judgement_text = 20
tiny_text = 15
detail_text = 12

song_size_gradient = [22,18,15]
song_color_gradient = [(200,230,255),(180,220,235),(140,180,215)]


# song offsets
song_offsets = {'test': 0}



# special effects
freeze_delay = 400
change_background_color = [0]
hmm_x_loc, hmm_y_loc = line_width , judgement_line + 10



# jacket options
jacket_size = (300,300)
jacket_loc = (width//2 - jacket_size[0]//2, 180)
jacket_transition_size = (400,400)
jacket_transition_loc = (width//2 - jacket_size[0]//2, 300)


# back button
back_button_x_loc = width - big_text
back_button_y_loc = 0
