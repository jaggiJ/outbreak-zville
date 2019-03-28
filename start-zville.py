#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulation of zombie virus in village.

BSD 3-Clause License

Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime  # new game with village designed before
import logging  # debugging module
import random  # random numbers and choices
import sys  # sys.exit() sys.argv
import time  # time delays time.sleep()

import data  # zville database
import zville  # zville functions

# SETTING UP

# debugging setup #levels:debug, info, warning, error, critical
# logging to file
# logging.basicConfig(filename='debug_zville.txt', level=logging.DEBUG,
#                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')  # DEBUG to file
# logging to console
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')  # DEBUG to console
# logging levels to disable
logging.disable(logging.DEBUG)  # disables all logging messages at <LEVEL> or lover level

# variables setup
sim_speed = 2  # need to be saved between simulations so its outside loop
saved_family = ()  # tuple here will store designed family
saved_village = ()  # tuple here will store designed village
random_village = True
random_family = True

# MAIN LOOP
while True:
    # SETTING_UP VARIABLES
    logging.info('Started main loop, # setting up variables')
    familyChar = []
    familyStats = []
    village_name = ''
    village_pop = 0

    # set up second game that had family or village designed
    if not random_family:
        familyChar = list(saved_family[0])  # tuple to list
        familyStats = list(saved_family[1])  # tuple to list
    if not random_village:
        village_name = saved_village[0]
        village_pop = saved_village[1]
        real_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    real_time = None

    intro_family, spam = zville.family_gen(True)
    initial_wave = len(intro_family)
    patient_zero = random.choice(intro_family)
    zombies_win = False  # useful for end game code

    # MAIN MENU CODE
    logging.info('User menu loop')
    while True:  # Handles user menu choices before game starts
        # zville.user_menu_choice(), # Main game menu returns integer
        main_choice = zville.user_menu_choice()

        if main_choice == 0:  # Intro game
            zville.intro_sim(data.STORY)  # Intro story
            random_family = True
            random_village = True
            village_name, village_pop, real_time = zville.village_gen(random_village)
            familyChar, familyStats = zville.family_gen(random_family)
            sim_speed = 1
            break

        elif main_choice == 5:  # Set Sim Speed
            while True:
                try:
                    print(' Set sim speed: '.center(50, '='))
                    print('Choose digit to set simulation speed')
                    print('\n1 - controlled by user pressing or holding enter key\n\n'
                          '2 - controlled by time intervals (default speed)\n\n3 - instant '
                          'simulation running to the end')
                    sim_speed = int(input())
                    if sim_speed not in [1, 2, 3]:
                        raise ValueError
                    print_s = ' SPEED SET = {sim_speed} '.format(sim_speed=sim_speed)
                    print(print_s.center(50, '+'))
                    break
                except ValueError:
                    print('Type an integer in range 1-3'.center(50, '='))
            continue

        elif main_choice == 1:  # Start Random Sim, will reset designed village and designed family
            random_family = True
            random_village = True
            familyChar, familyStats = zville.family_gen(random_family)
            village_name, village_pop, real_time = zville.village_gen(random_village)
            break

        elif main_choice == 2:  # Start Designed Sim, make checks whether family
            # or village are designed by user and asks for confirmation
            if not random_family and not random_village:
                print('Family: ' + ' '.join(familyChar), '\nvillage is: ', village_name,
                      village_pop, 'sim speed =', sim_speed)
            elif not random_family and random_village:
                print('Family: ' + ' '.join(familyChar), '\nVillage name and size will be random '
                      'and sim speed =', sim_speed)
                village_name, village_pop, real_time = zville.village_gen(random_village)  # case where only village is random,
                # if above is not generated here causes IndexError: list index out of range at introduction
            elif random_family and not random_village:
                print('Village: ', village_name, village_pop, '\nFamily members will be random and '
                      'sim speed =', sim_speed)
                familyChar, familyStats = zville.family_gen(random_family)
            else:
                print('Nothing designed yet.')
                continue
            if zville.yes_or_no('Do you want to start simulation with those settings?') == 'no':
                print('\nSetting village and family to random.')
                random_family = True
                familyChar = []
                familyStats = []
                random_village = True
                village_name, village_pop, real_time = None, None, None
                continue
            else:
                break  # in case user accept custom settings game starts with them

        elif main_choice == 3:  # Design Village
            random_village = False
            village_name, village_pop, real_time = zville.village_gen(random_village)
            saved_village = (village_name, village_pop)  # retaining village data for next games
            continue
        elif main_choice == 4:  # Design Family
            random_family = False
            familyChar, familyStats = zville.family_gen(random_family)
            saved_family = (tuple(familyChar), tuple(familyStats))  # saves family for next game, must be tuple to NOT reference familyChar familyStats lists
            continue
        elif main_choice == 6:  # Exit Sim
            sys.exit()

    # BEGINNING SCENE
    logging.info('Beginning scene.')
    print('='*79)
    story2 = (
        'Village {Yeovil}  {date_time}\npopulation size {p1530}\n{r_weather}\nThere {are}'
        '{John_and_Mark}\n...{doing_shopping}.\nAll of sudden {patient_zero} falls on the '
        'ground, pale like snow and is all in tremors...\n').format(
            Yeovil=village_name, date_time=real_time, p1530=str(village_pop),
            r_weather=zville.f_weather('day'), are='is ' if len(intro_family) == 1 else 'are ',
            John_and_Mark=', '.join(intro_family), doing_shopping=random.choice(data.LOCATIONS),
            patient_zero=patient_zero)

    twist_a = (
        'Everybody are shocked.\n{random_intro_family} crouches trying to help and '
        'something terrific happens...\n{patient_zero} turns into a zombie and attacks '
        'the living!\nBlood rushes forth...\n'
        'Soon there are {initial_wave} zombies shuffling toward nearest house...\n\n')\
        .format(random_intro_family=random.choice(intro_family),
                patient_zero=patient_zero, initial_wave=initial_wave)

    twist_b = (
        'There is nobody at hand to help. After a minute someone notices '
        'lying body\n... and runs away.\nMeanwhile {patient_zero} arises as a'
        ' zombie and shuffles toward nearest house.\nThere is'
        ' just this one zombie to brave new world...\n\n').format(patient_zero=patient_zero)

    # how fast story is printed out
    if sim_speed == 1:
        story2_delay = 0.03
    elif sim_speed == 2:
        story2_delay = 0.02
    else:
        story2_delay = 0

    # printing out above story with correct twist
    narration = story2
    while True:
        for item in narration:
            print(item, end='')
            time.sleep(story2_delay)
        if narration in [twist_a, twist_b]:
            break
        elif len(intro_family) != 1:
            intro_family.remove(patient_zero)
            narration = twist_a
        else:
            narration = twist_b

    # time delay after intro scene
    zville.press_enter() if sim_speed in [1, 2] else time.sleep(0)

    # NOW BUNCH OF VARIABLES FOR COMING SIMULATION
    logging.info('Bunch of variables after beginning scene.')
    pulped_body = 0
    grid_data, houses_number   = zville.gen_grid(village_pop)             # takes: population size, returns: grid_data (list of lists) and houses_number(integer)
    family_custom = False                                                 # Is family customised and saved by user ? Used for zville.family_fight()
    incubation_time = 12                                                  # x5 seconds (one round) Virus latency, how long until infected turns zombie
    current_pop     = village_pop - initial_wave                          # amount of population now, integer
    current_zombies = initial_wave                                        # amount of zombies now, integer

    # various speed parameters

    zed_speed_kmh   = 3.22                                              # set zeds speed here
    # how hard for zombies is to move forward (home fortifications), used to calculate average zeds speed
    obstacle_level  = 4
    # how many seconds are in one round
    round_sec = 5
    # zville.speed_round() - average zombie speed per round
    zed_speed       = zville.speed_round(zed_speed_kmh, obstacle_level, round_sec)
    # last amount of zombies per cell attacked, also used for human win condition check (turns to string and ends game)
    family_cache = 0
    # rounds counter
    round_count     = 1
    timer = [0, 0]  # minutes, seconds
    # how much rounds it take to move the swarm to next fight ?
    countdown_set = int(25 / zed_speed) + 1  # 25 meters distance / zed speed decreased + 1 because we round up to prevent exception if 0

    # CHOOSING RANDOM TILES FOR PATIENT ZERO AND FAMILY HOUSE LOCATION
    logging.info('# CHOOSING RANDOM TILES FOR PATIENT ZERO AND FAMILY HOUSE LOCATION')
    # first infected cell
    temp_x = random.randint(0, len(grid_data)-1)
    grid_data[temp_x][random.randint(0, len(grid_data[temp_x])-1)] = '#'

    # family-cell location
    while True:  # loop asserts family-cell not infected
        int_y = random.randint(0, len(grid_data) - 1)  # (y coord),(eg 5) represent list number in grid data
        int_x = random.randint(0, len(grid_data[0]) - 1)  # x coord eg 0 represent value number in random list inside grid_data
        family_coord = (int_y, int_x)  # tuple (y, x) eg (5, 0) < - list 5 value 0 of grid_data, is checked after fight and when is '#' triggers family_fight()

        if grid_data[int_y][int_x] != '#':  # checking if chosen coord doesn't contain infected tile
            grid_data[int_y][int_x] = '~'  # turning grid representation to family icon if not infected tile
            break

    # INITIAL DATA PRINTED OUT
    logging.info('# INITIAL DATA PRINTED OUT')
    print('=' * 79)
    print('zombie speed =', zed_speed_kmh, 'kmh')
    print('population of humans = {current_pop}'.format(current_pop=current_pop))
    print('virus incubation time = 60 seconds')
    print_s = ' {village_name}  {village_pop} villagers '\
        .format(village_name=village_name.upper(), village_pop=village_pop)
    print(print_s.center(79, '='))  # Prints village name and population above grid

    # draws grid for first time with one infected cell and with family location in bright cell
    zville.draw_grid_data(grid_data)
    print('=' * 79)

    print('Zombies head toward first house. Victims are unsuspecting...\n')

    # first game help message
    if main_choice == 0:
        print('=' * 79)
        print('On village map grid there is one most bright cell. When infection zone reaches\n'
              'that spot, family fight is triggered. One family is chosen as example, to\n'
              'represent simulation in more personal and detailed way.')
        print('=' * 79)

    # time delay after printing grid for the first time
    if sim_speed in [1, 2]:
        zville.press_enter(text='PRESS ENTER TO START APOCALYPSE')
    else:
        time.sleep(0)

    # MAIN LOOP FOR VIRUS SPREAD, iteration 5 sec
    logging.info('# MAIN LOOP FOR VIRUS SPREAD')
    while True:
        # ZOMBIES vs VILLAGERS FIGHT INSTANCE
        if countdown_set == 0:
            print('=' * 79)
            print('defences shattered, {current_zombies} zombies attack !'
                  .format(current_zombies=current_zombies))
            print('=' * 79)

            # zville.fight() and its arguments
            grid_data, current_zombies, current_pop, pulped_body, round_count, family_cache = \
                zville.fight(grid_data, current_zombies, current_pop, pulped_body, round_count,
                             sim_speed)
            if family_cache == 'humans_won':  # check for end game condition
                break

            # after each fight draw new grid data
            zville.draw_grid_data(grid_data)

            # FAMILY FIGHT SECTION zville.family_fight()
            logging.debug(' # FAMILY FIGHT SECTION')
            # checks if family alive and if family tile in infected cell, if yes triggers zville.family_fight()
            if family_custom != 'dead' and grid_data[family_coord[0]][family_coord[1]] == '#':

                # FAMILY_FIGHT() FUNCTION RUNS HERE !
                family_custom, familyChar, familyStats, zombiesPulped = \
                    zville.family_fight(family_cache, familyChar, familyStats, sim_speed,
                                        current_pop, current_zombies)

                current_zombies -= zombiesPulped  # reducing amount of zombies by those pulped by family
                pulped_body += zombiesPulped
                if current_zombies < 1:
                    print('Family involvement helped to stop the apocalypse. Humans won !')
                    break
            # FAMILY FIGHT SECTION ENDS

            # how much rounds it take to move the swarm to next fight ?
            countdown_set = int(25 / zed_speed) + 1  # 25 meters to go / zombie game speed + 1 because we round up to prevent exception if 0

            print('\npopulation of humans  = {current_pop}'.format(current_pop=current_pop))
            print('population of zombies = {current_zombies}     pulped bodies = {pulped_body}\n'
                  .format(current_zombies=current_zombies, pulped_body=pulped_body))

            # time delay at end of fight
            if sim_speed == 1:
                zville.press_enter()
            time.sleep(4) if sim_speed == 2 else time.sleep(0)

        # VARIOUS
        logging.debug('# VARIOUS')
        countdown_set -= 1

        if current_pop < 1:  # check for new game condition
            zombies_win = True
            break

        # iteration + 1 counter update
        round_count += 1

        # updating time 5 seconds per iteration, translating 60s to 1m,
        timer[1] += 5  # seconds
        if timer[1] == 60:
            timer[1] = 0
            timer[0] += 1  # minutes

        # time delay for zombies moving
        time.sleep(0.05) if sim_speed in [1, 2] else time.sleep(0)
        print('{timer_min}:{timer_sec} min passed'.format(timer_min=timer[0], timer_sec=timer[1]))

    if zombies_win:
        print('The village has been wiped out in {timer_m}:{timer_s} min'.format(timer_m=timer[0],
                                                                                 timer_s=timer[1]))
        print('Zombies are crawling among smoldering ruins of {village_name}.'
              .format(village_name=village_name))
        print('Pulped corpses left for eating = {pulped_body}.'.format(pulped_body=pulped_body))

    # PLAY AGAIN ?
    logging.info('# PLAY AGAIN ?')
    answer = zville.yes_or_no('Do you want to run simulation again ?')

    if answer == 'no' and current_zombies > 1:  # no, zombies won
        print(' ZOMBIES '.center(80, '+'), '\n')
        time.sleep(0.5)
        print(' M O A N '.center(80, '@'))
        break
    elif answer == 'no':  # no, humans won
        break

    else:  # user choose new game, intro game speed will change to default
        if sim_speed == 1:
            sim_speed = 2
