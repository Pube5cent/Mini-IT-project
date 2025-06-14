import pygame
import random
from variables import *
from music_ import *
from text_writer import *
from image_processor import *
from utility_functions import *
from chart import *
from game import *
from score_saver import *



def update_jacket(name):
    global jacket_size, jacket_loc
    jacket_path = 'jackets/' + name
    jacket_image = load_image(jacket_path)
    if not jacket_image: # no jacket
        jacket_path = 'jackets/not available'
        jacket_image = load_image(jacket_path)
    jacket_image = resize_image(jacket_image, jacket_size)
    jacket_rect = move_image(jacket_image, jacket_loc)
    return jacket_image, jacket_rect


def update_song_info():
    global song_info_list
    new_song_name = music_list[music_pointer]
    song_info_list = list(get_chart_info(new_song_name))
    play_current_music(new_song_name)
    return new_song_name, fetch_highest_score(new_song_name)


def exit_song_selection_screen(music_list, music_pointer, song_name):
    return music_list, music_pointer, song_name

def play_current_music(song_name):
    music_Q(song_name)


def song_selection_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics):
    # Variables needed to run run_FGHJ (the main function)
    # Used after song selection
    # stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics

    pygame.mixer.music.stop()
    
    song_selection_run = True


    # song selection settings
    global music_list, music_pointer, song_name
    music_list = get_musics()
    number_of_musics = len(music_list)
    min_index = max(music_pointer - 2, 0)
    max_index = min(music_pointer + 2, number_of_musics - 1)
    song_name = music_list[music_pointer]
    song_name,song_highest_score = update_song_info()

    # load jacket
    global jacket_size, jacket_loc
    height = screen.get_height()

    jacket_image, jacket_rect = update_jacket(song_name)
    screen.blit(jacket_image, jacket_rect)

    info_gap = 100
    song_list_x_level = width // 2#3 * (width // 10) #- info_gap
    song_info_x_level = width // 2#7*(width // 10)
    song_list_y_level = (height // 8) * 6 - info_gap
    song_info_y_level = (height // 8) * 6 + (info_gap//5)*7
    song_info_big_step = 10
    song_info_small_step = 5

    # back button
    back = load_image('back')
    back = resize_image(back, (big_text,big_text))
    back_rect = move_image(back, (back_button_x_loc,back_button_y_loc))


    while song_selection_run:
    
        
        music_pointer = random.randint(0, len(music_list) - 1)
        song_name = music_list[music_pointer]
        song_highest_score = fetch_highest_score(song_name)

        pygame.mixer.music.stop()
        game_start_sound()

        transition_time = pygame.time.get_ticks()
        delay_time = 1200
        while pygame.time.get_ticks() - transition_time < delay_time:
            screen.fill(background_color[0])
            jacket_image, jacket_rect = update_jacket(song_name)
            screen.blit(jacket_image, jacket_rect)
            pygame.display.flip()
            clock.tick(main_loop_render_fps)

        run_FGHJ(screen, clock, song_name, stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
        return exit_song_selection_screen(music_list, music_pointer, song_name)
