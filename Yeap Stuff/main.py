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
#will put as 800,600
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

    while run:
        
        music_list, music_pointer, song_name =song_selection_screen(screen,clock,stage_speed, offset, judgement_shown, guide_line_shown, high_quality_verifying_graphics)
        #run_FGHJ(screen, clock, song_name, stage_speed, offset, judgement_shown, guide_line_shown,
        #                     high_quality_verifying_graphics)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run, meta_run = exit()
                pygame.quit()
            if event.type == pygame.MOUSEMOTION:
                 # point.pos = pygame.mouse.get_pos()
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                (xp, yp) = pygame.mouse.get_pos()
                mouse_particle_list.append((pygame.time.get_ticks(),(xp, yp)))
                mouse_click_sound()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    run, meta_run = exit()
                    pygame.quit()

                elif event.key == pygame.K_RETURN:
                    run = False
                    music_list, music_pointer, song_name = song_selection_screen(screen, clock, stage_speed, offset,
                                                                                 judgement_shown, guide_line_shown,
                                                                                 high_quality_verifying_graphics)
                    pygame.quit()

       

        if not run:
                break
        screen.fill(background_color[0])
            
        if creater_mode:
            write_text(screen, width // 2, small_text*2, '- This is a creater mode -', small_text, background_color[0],
                   debug_color)

            
        write_text(screen, width//2, height//8 , 'Beat Rhythm', big_text, background_color[0], highlight_text_color)

 
        write_text(screen, width // 2, height-small_text*4, 'How to play: ', small_text, background_color[0],
                   highlight_text_color)
        write_text(screen, width // 2, height-small_text*2, 'press %s,%s,%s,%s in appropriate timing!'%(guide_keys[0],guide_keys[1],guide_keys[2],guide_keys[3]), small_text, background_color[0],
                   highlight_text_color)

        if mouse_particle_list:  # if not empty
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



        pygame.display.flip()
        clock.tick(main_loop_render_fps)
