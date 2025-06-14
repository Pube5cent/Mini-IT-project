#handling music files 
#.wav and .mp3 can be accepted?

import pygame
import os,sys
from variables import *


pygame.mixer.init()

mixer_channel_num = 8

current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))

MUSIC_FOLDER = current_dir+'/cc_musics/'
SOUND_EFFECT = current_dir+'/sound_effects/'

# sound effects, for flair and funsies
mouseClick = pygame.mixer.Sound(SOUND_EFFECT+"mouse_click.mp3")
hitSound = pygame.mixer.Sound(SOUND_EFFECT+"hit2.wav")
gameStartSound = pygame.mixer.Sound(SOUND_EFFECT+"game_start.mp3")

def hit_sound():
    if sound_effect[0]:
        hitSound.play()

def game_start_sound():
    if sound_effect[0]:
        gameStartSound.play()

def mouse_click_sound():
    if sound_effect[0]:
        mouseClick.play()
        
def music_Q(music_file,repeat = False): #set the "set_playing_sound to true if you want to check the currently playing song"
    global MUSIC_FOLDER
    try:
            full_path = os.path.join(MUSIC_FOLDER, '%s.mp3'%music_file)
            pygame.mixer.music.load(full_path)
    except:
            full_path = os.path.join(MUSIC_FOLDER, '%s.wav'%music_file)
            pygame.mixer.music.load(full_path)
        
    SONG_START_TIME = 0 #set at what time teh song start, though idk why you want it but you can
    pygame.mixer.music.set_volume(1)
        
    if repeat:
            pygame.mixer.music.play(-1)
    else:
            pygame.mixer.music.play()
            
    return SONG_START_TIME #its in milliseconds
    
def get_musics():
    global MUSIC_FOLDER
    full_path = os.path.join(MUSIC_FOLDER, 'music_list.txt')
    list_ = []
    #print("%s"%full_path)
    with open("%s"%full_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            list_.append(line.strip())
    return list_

def get_music_info(song_name):
    APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))+'/CC_musics/'
    full_path = os.path.join(APP_FOLDER, '%s.txt'%song_name)
    try:
        with open("%s"%full_path, "r") as f:
            credit = f.readlines()
            print(credit)
            max_len = 60
            for i in range(len(credit)):
                line = credit[i].strip()
                cnt = 0
                del credit[i]
                while len(line) > max_len:
                    shortened_front = line[:max_len]
                    credit.insert(i+cnt,shortened_front)
                    line = line[max_len:]
                    cnt+=1
                    #print(i+cnt)
                credit.insert(i + cnt, line)
    except FileNotFoundError:
        credit=['No credit']
    #print(credit)
    return credit

def add_musics():
    music_name = input('Enter music name: ')
    full_path = os.path.join(MUSIC_FOLDER, 'music_list.txt')

    with open("%s"%full_path, "a") as f:
        f.write(music_name+'\n')

def check_music_exists():
    pass

def check_music_ended(song_start_time):
    #print(song_start_time)
    if song_start_time == -1: # not started
        return False
    # return True if music is still going. returns False if music is paused or ended.
    return not pygame.mixer.music.get_busy()


a=[]

def msc_list():
    global MUSIC_FOLDER
    with open('music_list.txt','r') as file:
        for a in file:
            a.append()
    print (a)
    return
