#prototype 2 27/4

#building main game loop

#should probably use fghj as my key press

#some other imports from the tutorial, will add more the further i get what they do
import pygame
from variables import * #done
from utility_functions import * #done
from music_ import * #done
from text_writer import * #done
from image_processor import * #done
from chart import * #done
from screen_options import * #done
from song_selection import * #done


pygame.init()
clock = pygame.time.Clock()


screen = pygame.display.set_mode((width,height))
<<<<<<< HEAD
#will put as 800,600, otherwise it will be the same size as the pc window
=======
#will put as 800,600
>>>>>>> BeatRhythm_pyto
width, height = pygame.display.get_surface().get_size()

pygame.display.set_caption('IDLEStudy:BEAT RHYTHM')


screen.fill(background_color[0])


#set main menu

run = True
meta_run = True

def exit():
    pygame.quit()
    return False, False
while meta_run:
    global stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics, music_list, music_pointer, song_name
    # The Music in main
    music_Q(lobbyMusic,True)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run, meta_run = exit()
                break

            if event.type == pygame.MOUSEMOTION:
                
<<<<<<< HEAD
                # point.pos = pygame.mouse.get_pos()
=======

>>>>>>> BeatRhythm_pyto
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(),(xp, yp)))
                mouse_click_sound()

                if abs(xp - option_key_x_level) < big_text*6:
                    if abs(yp - (option_key_y_level)) < big_text:
<<<<<<< HEAD
                        print('option clicked!')
                        run = False
                        stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics = option_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
                        #print(stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
=======
                        run = False
                        stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics = option_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
>>>>>>> BeatRhythm_pyto
                        break

                if abs(xp - song_selection_key_x_level) < big_text*6:
                    if abs(yp - (song_selection_key_y_level)) < big_text:
<<<<<<< HEAD
                        print('song selection clicked!')
                        run = False
                        music_list, music_pointer, song_name = song_selection_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
                        #print(music_list, music_pointer, song_name)
=======
                        run = False
                        music_list, music_pointer, song_name = song_selection_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
>>>>>>> BeatRhythm_pyto
                        break
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    run, meta_run = exit()
                    break

                elif event.key == pygame.K_RETURN:
<<<<<<< HEAD
                    print('Going to song selection!')
=======
>>>>>>> BeatRhythm_pyto
                    run = False
                    music_list, music_pointer, song_name = song_selection_screen(screen, clock, stage_speed, offset,
                                                                                 judgement_shown, guide_line_shown,
                                                                                 high_quality_verifying_graphics)
                    break



<<<<<<< HEAD
            if not run:
                break
            screen.fill(background_color[0])
            
    if creater_mode:
        write_text(screen, width // 2, small_text*2, '- This is a creater mode -', small_text, background_color[0],
                   debug_color)

            
    write_text(screen, width//2, height//8 , 'Beat Rhythm', big_text, background_color[0], highlight_text_color)

    write_text(screen, option_key_x_level, option_key_y_level,
                   'Options/Calibrations', big_text, background_color[0],
                   highlight_text_color)
    pygame.draw.rect(screen, highlight_text_color, [width//4 - big_text, option_key_y_level - button_y_offset, button_x_size, button_y_size], 4,8)

    write_text(screen, song_selection_key_x_level, song_selection_key_y_level,
                   'Song selection', big_text, background_color[0],
                   highlight_text_color)
    pygame.draw.rect(screen, highlight_text_color, [width//4 - big_text,  song_selection_key_y_level - button_y_offset, button_x_size, button_y_size], 4,8)
        
    write_text(screen, width // 2, height-small_text*4, 'How to play: ', small_text, background_color[0],
                   highlight_text_color)
    write_text(screen, width // 2, height-small_text*2, 'press %s,%s,%s,%s in appropriate timing!'%(guide_keys[0],guide_keys[1],guide_keys[2],guide_keys[3]), small_text, background_color[0],
                   highlight_text_color)

    if mouse_particle_list:  # if not empty
=======
        if not run:
                break
        screen.fill(background_color[0])
            
        if creater_mode:
            write_text(screen, width // 2, small_text*2, '- This is a creater mode -', small_text, background_color[0],
                   debug_color)

            
        write_text(screen, width//2, height//8 , 'Beat Rhythm', big_text, background_color[0], highlight_text_color)

        write_text(screen, option_key_x_level, option_key_y_level,
                   'Options/Calibrations', big_text, background_color[0],
                   highlight_text_color)
        pygame.draw.rect(screen, highlight_text_color, [width//4 - big_text, option_key_y_level - button_y_offset, button_x_size, button_y_size], 4,8)

        write_text(screen, song_selection_key_x_level, song_selection_key_y_level,
                   'Song selection', big_text, background_color[0],
                   highlight_text_color)
        pygame.draw.rect(screen, highlight_text_color, [width//4 - big_text,  song_selection_key_y_level - button_y_offset, button_x_size, button_y_size], 4,8)
        
        write_text(screen, width // 2, height-small_text*4, 'How to play: ', small_text, background_color[0],
                   highlight_text_color)
        write_text(screen, width // 2, height-small_text*2, 'press %s,%s,%s,%s in appropriate timing!'%(guide_keys[0],guide_keys[1],guide_keys[2],guide_keys[3]), small_text, background_color[0],
                   highlight_text_color)

        if mouse_particle_list:  # if not empty
>>>>>>> BeatRhythm_pyto
            #print(len(mouse_particle_list))
            current_run_time = pygame.time.get_ticks()
            for mouse_particle in mouse_particle_list:
                #draw_particle(screen, mouse_particle)
                mouse_click_time = mouse_particle[0]
                position = mouse_particle[1]
                delta = (current_run_time - (mouse_click_time))/1000
                if  delta >= water_draw_time_mouse:
                    mouse_particle_list.remove(mouse_particle)
                factor = delta / water_draw_time_mouse
                radi = calc_drop_radius(factor, mouse_particle_radius)
                pygame.draw.circle(screen,effect_color, position, radi, particle_width_mouse)



<<<<<<< HEAD
    pygame.display.flip()
    clock.tick(main_loop_render_fps)
=======
        pygame.display.flip()
        clock.tick(main_loop_render_fps)
>>>>>>> BeatRhythm_pyto
