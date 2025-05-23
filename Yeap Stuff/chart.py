#this module is to have the game red charts
# time offset in ms and line number is taken nto account, need to double check the tutorial


import pygame
import os, sys
from chart_builder import *

def check_chart_exists(path):
    if os.path.isfile(path):
        return True
    else:
        return False


def get_chart_info(song_name):
    APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))+'/charts/'
    full_path = os.path.join(APP_FOLDER, '%s.txt'%song_name)

    if not check_chart_exists(full_path):
        return 0,0,0,0,0

    with open("%s"%full_path, "r") as f:
        lines = f.readlines()
        first_line = lines[0]
        first_line.rstrip()
        first_line = first_line.split(',')
        song_length = int(first_line[0])
        song_bpm = int(first_line[1])  # milli-seconds per beat
        song_difficulty = int(first_line[2])
        total_points = int(first_line[3])
        recommended_fps = int(first_line[4])

    return song_bpm, song_length, song_difficulty, total_points, recommended_fps

def get_chart(song_name):
    APP_FOLDER = os.path.dirname(os.path.realpath(sys.argv[0]))+'/charts/'
    full_path = os.path.join(APP_FOLDER, '%s.txt'%song_name)

    if not check_chart_exists(full_path):
        return 0,0,0,0,0,[]

    request = []

    with open("%s"%full_path, "r") as f:
        lines = f.readlines()
        first_line = lines[0]
        first_line.rstrip()
        first_line = first_line.split(',')
        song_length = int(first_line[0])
        song_bpm = int(first_line[1])  # milli-seconds per beat
        song_difficulty = int(first_line[2])
        total_points = int(first_line[3])
        recommended_fps = int(first_line[4])

        lines = lines[1:]

        for line in lines:
            line.rstrip()
            data = line.split(',')

            request.append(data) # just feed a raw information


    print("Current song: %s"%song_name)
    print("BPM: %d" %song_bpm)
    print("Total Points: %d"%total_points)
    print("Difficulty: %d"%song_difficulty)
    print("Recommended_fps: %d"%recommended_fps)

    return total_points, song_difficulty, song_length, song_bpm, recommended_fps, request