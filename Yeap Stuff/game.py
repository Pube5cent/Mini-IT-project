import pygame
from variables import *
from tiles import *
from verifier_class import *
from distributer_class import *
from music_ import *
from text_writer import *
from image_processor import *
from score_viewer import *
from chart import *
from utility_functions import *
import moviepy.editor # pip install moviepy==1.0.3


def exit_game(screen, clock, song_name, score,song_difficulty,total_points):
    global change_background_color
    change_background_color[0] = 0  # set back to normal
    view_score_menu(screen, clock, song_name, score,song_difficulty,total_points)

def get_ready(screen,clock,song_name,total_points):
    global change_background_color, creater_mode
    game_run = True
    exit_outer_game = False
    score = [0]
    pygame.mixer.music.stop()

    seconds_to_count = 3  # 3
    if creater_mode: # start right away
        seconds_to_count = 0

    count = seconds_to_count
    start_time = pygame.time.get_ticks()

    # load highlight
    highlight = load_highlight()
    reverse_highlight = load_reverse_highlight()


    while game_run:
        time_passed_milli = pygame.time.get_ticks() - start_time
        count = seconds_to_count - time_passed_milli//1000
        if count <= 0:
            game_run = False
            exit_outer_game = False
            break

        screen.fill(background_color[change_background_color[0]])

        # Event handling
        keys = pygame.key.get_pressed()  
        if keys[pygame.K_f]:
            highlight_line(screen, highlight, 1)
        if keys[pygame.K_g]:
            highlight_line(screen, highlight, 2)
        if keys[pygame.K_h]:
            highlight_line(screen, highlight, 3)
        if keys[pygame.K_j]:
            highlight_line(screen, highlight, 4)
            #print(judgement_line)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT: 
                game_run = False
                exit_outer_game = True
                break

            if event.type == pygame.MOUSEMOTION:  
                # point.pos = pygame.mouse.get_pos()
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                (xp, yp) = pygame.mouse.get_pos()
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # esc button press
                    game_run = False
                    exit_outer_game = True
                    break

                if event.key == pygame.K_f:
                    highlight_line(screen, highlight, 1)
                if event.key == pygame.K_g:
                    highlight_line(screen, highlight, 2)
                if event.key == pygame.K_h:
                    highlight_line(screen, highlight, 3)
                if event.key == pygame.K_j:
                    highlight_line(screen, highlight, 4)


        write_text(screen, width//2, (info_length//2)//2, 'Song: %s'%(song_name), small_text, background_color[change_background_color[0]], highlight_text_color)
        write_text(screen, width // 2, (info_length // 2) // 2 + (info_length // 2), f"Score: {'0':<6} / {total_points:>4}", small_text, background_color[change_background_color[0]],
                   highlight_text_color)


        # draw basic frame with lines
        draw_frame(screen)

        # get ready count
        write_text(screen, width // 2, height//2, '%d' % (count), giant_text,
                   background_color[change_background_color[0]],
                   red_highlight_text_color)

        # ESC
        write_text(screen, width // 2, 3*(height//4), 'Press ESC to QUIT', tiny_text,
                   background_color[change_background_color[0]],
                   red_highlight_text_color)



        # guide key shown
        draw_guide_key(screen)

        pygame.display.flip()
        clock.tick(main_loop_render_fps)

    return exit_outer_game


def calc_song_progress_percent(song_length,song_start_time,current_time):  # return in percent
    if song_start_time == -1: # If song hasn't started
        return 0 # no progress!
    delta = current_time - song_start_time
    progress = 100*(delta/song_length)
    return progress


def run_FGHJ(screen,clock,song_name,stage_speed,offset,judgement_shown,guide_line_shown,high_quality_verifying_graphics):
    global bar_color, wait_delay, change_background_color

    game_run = True
    score = [0]
    chart_info = get_chart(song_name)
    total_points = chart_info[0]
    song_difficulty = chart_info[1]
    song_length = chart_info[2]  # in milliseconds!
    song_bpm = chart_info[3]
    game_fps = chart_info[4]

    # screen pause effect
    screen_freeze = False
    first_pause_time = song_length + 100 # no pause == pause after the end of the song
    letter_color = highlight_text_color

    nodes_on_screen = []
    holds_on_screen = []
    beat_lines = []
    tiles_off_screen = []


    if get_ready(screen,clock,song_name,total_points): # if exit outer game is true
        game_run = False
        view_score_menu(screen, clock, song_name, score, song_difficulty, total_points)
        return

    # load highlight
    highlight = load_highlight()
    reverse_highlight = load_reverse_highlight()

    # custom press setting for HHM fan music!
    hhm_list = []
    if song_name == 'Hmm Heu Ming Remix (Rcol)':
        print("Now playing Hmm Heu Ming!")
        hmm = load_image('hmm')
        hu = load_image('hu')
        ming = load_image('ming')
        zoa = load_image('zoa')
        hhm_list.append(hmm)
        hhm_list.append(hu)
        hhm_list.append(ming)
        hhm_list.append(zoa)


    verifier = Verifier(screen,score,stage_speed,judgement_shown,song_bpm,high_quality_verifying_graphics, game_fps)


    bar_pos = (width // 2, info_length//4)
    song_progress = 0

    song_start_time = -1
    need_music = True

    if chart_info[5]==[]:
        print(chart_info)
        print("Chart has no nodes. Finishing the game.")
        exit_game(screen, clock, song_name, score, song_difficulty, total_points)
        game_run = False
    else:
        distributer = Distributer(stage_speed,offset,screen,chart_info[5],song_name,song_bpm,game_fps, beat_line_request=guide_line_shown)

    # clip.preview()
    pygame.display.set_mode((width, height))
    while game_run:
        if need_music and distributer.ready:
            music_Q(song_name)
            need_music = False
            song_start_time = pygame.time.get_ticks()

        screen.fill(background_color[change_background_color[0]])


        events = pygame.event.get()
        # Event handling
        keys = pygame.key.get_pressed() # SHOULD BE CALLED AFTER pygame.event.get()!

        if keys[pygame.K_f]:
            highlight_line(screen, highlight, 1)
            if hhm_list:
                draw_hhm_key(screen, hhm_list, 0)
        if keys[pygame.K_g]:
            highlight_line(screen, highlight, 2)
            if hhm_list:
                draw_hhm_key(screen, hhm_list, 1)
        if keys[pygame.K_h]:
            highlight_line(screen, highlight, 3)
            if hhm_list:
                draw_hhm_key(screen, hhm_list, 2)
        if keys[pygame.K_j]:
            highlight_line(screen, highlight, 4)
            if hhm_list:
                draw_hhm_key(screen, hhm_list, 3)

        for event in events:
            if event.type == pygame.QUIT:  # quit button, what else
                exit_game(screen, clock, song_name, score,song_difficulty,total_points)
                game_run = False
                break

            if event.type == pygame.MOUSEMOTION:   #if player want sto get mouse movement input, remove the #
                # point.pos = pygame.mouse.get_pos()
                pass

            if event.type == pygame.MOUSEBUTTONUP:
                (xp, yp) = pygame.mouse.get_pos()
                pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  #esc button press
                    exit_game(screen, clock, song_name, score,song_difficulty,total_points)
                    game_run = False
                    break

                if event.key == pygame.K_f:
                    highlight_line(screen, highlight, 1)
                    if hhm_list:
                        draw_hhm_key(screen, hhm_list, 0)
                if event.key == pygame.K_g:
                    highlight_line(screen, highlight, 2)
                    if hhm_list:
                        draw_hhm_key(screen, hhm_list, 1)
                if event.key == pygame.K_h:
                    highlight_line(screen, highlight, 3)
                    if hhm_list:
                        draw_hhm_key(screen, hhm_list, 2)
                if event.key == pygame.K_j:
                    highlight_line(screen, highlight, 4)
                    if hhm_list:
                        draw_hhm_key(screen, hhm_list, 3)

        if not game_run:
            break

        distributer.distribute(nodes_on_screen,holds_on_screen,beat_lines)
        


        #for on screen tiles
        for tile in nodes_on_screen+holds_on_screen:
            tile.move(stage_speed)
            tile.draw(screen)

        #for off screen tiles
        for tile in tiles_off_screen:
            tile.move(stage_speed)


        if guide_line_shown:
            verifier.draw_guide_lines(nodes_on_screen,holds_on_screen,screen)

            for hori in beat_lines:
                hori.move(stage_speed)
                hori.draw(screen)
                
        # verifier.node_check(nodes_on_screen, events) 
        verifier.node_check(nodes_on_screen, tiles_off_screen, keys)
        verifier.hold_check(holds_on_screen, tiles_off_screen, keys)
        verifier.draw_judgement()
        
        for tile in tiles_off_screen:
            
            if tile.special:
                if (tile.y >= judgement_line): # after passing judgement line
                    #print('special found after judgement line')
                    special_effect = tile.special_effect()

                    # 3.2 do the special effect
                    if special_effect == 'wait':
                        first_pause_time = pygame.time.get_ticks()
                        screen_freeze = True

                        ####### change background color! ########
                        change_background_color[0] = 1
                        highlight = reverse_highlight
                        letter_color = (0,0,0)

                        screen.fill(background_color[change_background_color[0]])
                        tile.fix_loc()
                        verifier.draw_judgement()
                        for T in tiles_off_screen + nodes_on_screen + holds_on_screen:
                            T.freeze()
                            T.draw(screen,screen_freeze)
                        draw_frame(screen)
                        write_text(screen, width // 2, (info_length // 2) // 2, 'Song: %s' % (song_name), small_text,
                                   background_color[change_background_color[0]], letter_color)
                        pygame.display.flip()
                        ####### change background color! ########
                        #pygame.time.delay(wait_delay)

                        tiles_off_screen.remove(tile)
                        break
        current_time = pygame.time.get_ticks()  # in milliseconds
        song_progress = calc_song_progress_percent(song_length, song_start_time, current_time)
        draw_progress_bar(screen, song_progress, bar_pos[0], bar_pos[1])

        current_score = round(score[0], 2)

        write_text(screen, width // 2, (info_length // 2) // 2, 'Song: %s' % (song_name), small_text,
                   bar_color, letter_color)
        write_text(screen, width // 2, (info_length // 2) // 2 + (info_length // 2), f"Score: {current_score:<6} / {total_points:>4}", small_text, background_color[change_background_color[0]],
                   letter_color)


    
        # draw basic frame with lines
        draw_frame(screen)

        # 6. hit effect
        verifier.draw_hit_effects(screen)


        if not screen_freeze:
            pygame.display.flip()
        else: # check when the screen update should be true
            screen_cur_time = pygame.time.get_ticks()
            if (screen_cur_time - first_pause_time) >= freeze_delay:
                screen_freeze = False
                if song_name == 'BadApple': # keep the inverted color
                    pass
                else:
                    change_background_color[0] = 0  # set back to normal

        clock.tick_busy_loop(game_fps)

        if check_music_ended(song_start_time):
            game_run = False
            exit_game(screen, clock, song_name, score,song_difficulty,total_points)
            break

def draw_progress_bar(screen, song_progress, x,y):
    global bar_color
    bar_width = width
    bar_height = info_length//2

    #draw_bar_frame(screen, x, y, bar_width, bar_height, color) # don't need frames here
    draw_bar(screen,x,y,bar_width,bar_height, song_progress, bar_color)


def draw_frame(screen):
    global frame_alpha,frame_alpha_max,frame_phase,frame_grad_color,change_background_color
    frame_line_width = 4
    frame_line_half = frame_line_width//2

    judgement_line_width = 4
    # pygame.draw.line(screen, judgement_line_color, [0, judgement_line-judgement_line_width//2], [width, judgement_line-judgement_line_width//2], judgement_line_width)
    pygame.draw.line(screen, judgement_line_color, [0, judgement_line],
                     [width, judgement_line], judgement_line_width)

    # fill in unsused lines
    pygame.draw.rect(screen, background_color[change_background_color[0]],
                     [0-frame_line_half, info_length+frame_line_half, line_width, height-info_length])
    pygame.draw.rect(screen, background_color[change_background_color[0]],
                     [width-line_width, info_length+frame_line_half, line_width, height-info_length])

    fill_color = (frame_grad_color,frame_grad_color,frame_grad_color)

    if frame_alpha == frame_alpha_max:
        frame_phase = -1/frame_cycle
    elif frame_alpha == 0:
        frame_phase = 1/frame_cycle
    frame_alpha = (frame_alpha + frame_phase)
    if (frame_alpha-int(frame_alpha)) < 1/(2*frame_cycle) :  # 이 주기일때만 업데이트
        frame_grad_color = min(40+int(frame_alpha),255)

    pygame.draw.rect(screen, fill_color,
                     [0-frame_line_half, info_length+frame_line_half, line_width, height-info_length])
    pygame.draw.rect(screen, fill_color,
                     [width-line_width, info_length+frame_line_half, line_width, height-info_length])

    pygame.draw.line(screen, line_color, [0,info_length//2], [width,info_length//2], frame_line_width)
    pygame.draw.line(screen, line_color, [0, info_length], [width, info_length], frame_line_width)

    for i in range((line_number-1)):
        pygame.draw.line(screen, line_color, [line_width*(i+1)-frame_line_half, info_length], [line_width*(i+1)-frame_line_half, height], frame_line_width)


def draw_guide_key(screen):
    global frame_grad_color,change_background_color
    for i in range((guide_key_size)):
        write_text(screen,guide_x_loc+line_width*i, guide_y_loc , guide_keys[i], small_text, background_color[change_background_color[0]],
                   (color_safe(200-frame_grad_color),color_safe(200-frame_grad_color),color_safe(200-frame_grad_color)))


def draw_hhm_key(screen, hhm_list,idx):
    global hmm_x_loc, hmm_y_loc
    if not hhm_list:
        pass
    screen.blit(hhm_list[idx], [hmm_x_loc+line_width*idx, hmm_y_loc])


