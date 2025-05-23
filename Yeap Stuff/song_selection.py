import pygame
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                song_selection_run = False
                return exit_song_selection_screen(music_list, music_pointer, song_name)

            if event.type == pygame.MOUSEMOTION:  
                # point.pos = pygame.mouse.get_pos()
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(), (xp, yp)))
                mouse_click_sound()

                if abs(xp - back_button_x_loc - big_text) < big_text:  # press back button to quit song selection
                    if abs(yp - back_button_y_loc) < big_text:
                        song_selection_run = False
                        return exit_song_selection_screen(music_list, music_pointer, song_name)


            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    music_pointer -= 1
                    music_pointer = boundary_checker(0, number_of_musics - 1, music_pointer)
                
                    min_index = max(music_pointer - 2, 0)
                    max_index = min(music_pointer + 2, number_of_musics - 1)
                    song_name,song_highest_score = update_song_info()

                if event.button == 5:
                    music_pointer += 1
                    music_pointer = boundary_checker(0, number_of_musics - 1, music_pointer)
                    
                    min_index = max(music_pointer - 2, 0)
                    max_index = min(music_pointer + 2, number_of_musics - 1)
                    song_name,song_highest_score = update_song_info()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    song_selection_run = False
                    return exit_song_selection_screen(music_list, music_pointer, song_name)

                # after choosing music
                elif event.key == pygame.K_RETURN:
                    if song_info_list[4]==0:
                        continue

                    pygame.mixer.music.stop()
                    game_start_sound()
                    transition_time = pygame.time.get_ticks()
                    delay_time = 1200
                    ######################################## transition screen
                    droplet = True
                    while 1:
                        current_run_time = pygame.time.get_ticks()
                        if current_run_time - transition_time > delay_time:
                            break

                        screen.fill(background_color[0])
                        screen.blit(jacket_image, jacket_rect)
                        if droplet == True:
                            deploy_time = transition_time
                            position = (jacket_loc[0]+jacket_size[0]//2 ,jacket_loc[1]+jacket_size[1]//2)
                            delta = (current_run_time - (deploy_time)) / 1000
                            if delta >= water_draw_time:
                                droplet = False
                            factor = delta / water_draw_time
                            radi = calc_drop_radius(factor, 40)
                            pygame.draw.circle(screen, highlight_text_color, position, radi, particle_width)
                        pygame.display.flip()
                        clock.tick(main_loop_render_fps)
                    ######################################## transition screen
                
                    run_FGHJ(screen, clock, song_name, stage_speed, offset, judgement_shown, guide_line_shown,
                             high_quality_verifying_graphics)
                    song_selection_run = False
                    return exit_song_selection_screen(music_list, music_pointer, song_name)
                #list going up /down
                elif event.key == pygame.K_UP:
                    music_pointer -= 1
                    music_pointer = boundary_checker(0, number_of_musics - 1, music_pointer)
                    
                    min_index = max(music_pointer - 2, 0)
                    max_index = min(music_pointer + 2, number_of_musics - 1)
                    song_name,song_highest_score = update_song_info()

                elif event.key == pygame.K_DOWN:
                    music_pointer += 1
                    music_pointer = boundary_checker(0, number_of_musics - 1, music_pointer)
                    
                    min_index = max(music_pointer - 2, 0)
                    max_index = min(music_pointer + 2, number_of_musics - 1)
                    song_name,song_highest_score = update_song_info()

        if not song_selection_run:
            return exit_song_selection_screen(music_list, music_pointer, song_name)

        screen.fill(background_color[0])

        # draw keys
        if creater_mode:
            write_text(screen, width // 2, small_text * 2, '- This is a creater mode -', small_text,
                       background_color[0],
                       debug_color)

        write_text(screen, width // 2, height // 8 - big_text, 'Song selection', big_text, background_color[0],
                   highlight_text_color)

        pygame.draw.rect(screen, highlight_text_color, [width // 4- big_text,  height // 8 - big_text - button_y_offset, button_x_size, button_y_size], 4,8)


        write_text(screen, width // 2, height // 8 + tiny_text, 'Press ENTER to start!', small_text, background_color[0],
                   highlight_text_color)


        # song settings
        for index in range(min_index, max_index + 1):
            music = music_list[index]
            location = index - music_pointer
            music_string = '%s' % (music)
            if location == 0:
                music_string = '< %s >' % (music)
            write_text(screen, song_list_x_level, song_list_y_level + location * small_text, music_string,
                       song_size_gradient[abs(location)],
                       background_color[0],
                       song_color_gradient[abs(location)])

        write_text(screen, song_list_x_level, song_list_y_level - 6 * small_text, 'scroll to select', tiny_text,
                   background_color[0],
                   highlight_text_color)
        draw_arrow('1up', screen, song_list_x_level, (song_list_y_level - 4 * small_text))
        draw_arrow('1down', screen, song_list_x_level, (song_list_y_level + 4 * small_text))


        write_text(screen, song_info_x_level, song_info_y_level - 4 * small_text, '[ Song Info ]',
                   small_text, background_color[0],
                   highlight_text_color)


        write_text(screen, song_info_x_level, song_info_y_level - 2 * small_text,
                   f"{'Length':<12}| {song_info_list[1]// 1000:>4} s", tiny_text, background_color[0],
                   highlight_text_color)
        write_text(screen, song_info_x_level, song_info_y_level - 1 * small_text, f"{'BPM':<15}| {song_info_list[0]:>4}" ,
                   tiny_text, background_color[0],
                   highlight_text_color)
        write_text(screen, song_info_x_level, song_info_y_level - 0 * small_text,
                   f"{'Difficulty':<15}| {song_info_list[2]:>4}" , tiny_text, background_color[0],
                   highlight_text_color)
        write_text(screen, song_info_x_level, song_info_y_level + 1 * small_text,
                   f"{'Total points':<13}| {song_info_list[3]:>4}" , tiny_text, background_color[0],
                   highlight_text_color)

        write_text(screen, song_info_x_level, song_info_y_level + 3 * small_text,
                   f"{'Score':<10}| {round(song_highest_score,2):>4} %", tiny_text, background_color[0],
                   red_highlight_text_color)


        jacket_image, jacket_rect = update_jacket(song_name)
        # draw the jacket
        screen.blit(jacket_image, jacket_rect)

        # draw the back button
        screen.blit(back, back_rect)


        if mouse_particle_list:  # if not empty
           
            current_run_time = pygame.time.get_ticks()
            for mouse_particle in mouse_particle_list:
                mouse_click_time = mouse_particle[0]
                position = mouse_particle[1]
                delta = (current_run_time - (mouse_click_time)) / 1000
                if delta >= water_draw_time_mouse:
                    mouse_particle_list.remove(mouse_particle)
                factor = delta / water_draw_time_mouse
                radi = calc_drop_radius(factor, mouse_particle_radius)
                pygame.draw.circle(screen, effect_color, position, radi, particle_width_mouse)


        pygame.display.flip()
        clock.tick(main_loop_render_fps)