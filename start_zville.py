#! python3
"""
BSD 3-Clause License
Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.
Simulation of zombie virus in village.
"""

import random  # Used for random k6rolls to powerAdvantage resolution
import sys  # Used to quit game on user enter input at choosing zombies number
import time  # Used for delay between zombie hits
from zville_functions import intro_game, user_menu_choice, village_gen, \
    family_gen, yes_or_no, f_weather, draw_grid_data, gen_grid, speed_round
from zville_functions import fight, family_fight, press_enter

story = """How shit hit the fun?
An isolated village. 
Great place for testing stuff on human subjects, isn't it?    
Concerns about value of human life, dignity and work ethics since long had 
their own spin-off. 
Something happened, let's call it ... 
Lack of transparency for government spending. 
A viral sample has been released.     
Somewhere in the village, patient zero has been exposed to a sample.  
"""

sim_speed = 2
random_village = True
random_family = True
village = []
familyChar = []
familyStats = []
weather = f_weather('day')
locations = ['walking in a park', 'packing stuff into a car\'s trunk',
             'watching a big TV in a saloon', 'playing a game of cards',
             'quarreling passionately']
intro_family, spam = family_gen(True)  # random names for game story family spam is to hold trash overflow data returned by function
initial_wave = len(intro_family)
# print(intro_family) DEBUGGING
patient_zero = random.choice(intro_family)
# print(patient_zero) DEBUGGING

while True:  # MAIN LOOP

    # MAIN MENU CODE
    while True:  # Handles user menu choices before game starts
        main_choice = user_menu_choice()  # Main game menu returns integer

        if main_choice == 0:  # Intro game
            intro_game(story)  # Intro story
            random_family = True
            random_village = True
            village = village_gen(random_village)
            familyChar, familyStats = family_gen(random_family)
            sim_speed = 1  # Speed is set slower because its probably first game
            break

        elif main_choice == 5:  # Set Sim Speed
            print("""       sim_speed determines:
            printing speed of  introductory scene, 
            delay speed of main fight summaries,
            printing speed main fight fighting, 
            delay speed of family fight summaries,
            printing speed of family fighting, 
            """)
            while True:
                try:
                    print(' Set sim speed: '.center(50, '='))
                    print('\n1 - controlled by user pressing or holding enter key\n\n'
                          '2 - controlled by time intervals (default speed)\n\n3 - instant simulation running to the end')
                    sim_speed = int(input())
                    if sim_speed not in [1, 2, 3]:
                        raise ValueError
                    print(f' SPEED SET = {sim_speed} '.center(50, '+'))
                    break
                except ValueError:
                    print('Type an integer in range 1-3'.center(50, '='))
            continue

        elif main_choice == 1:  # Start Random Sim
            random_family = True
            random_village = True
            familyChar, familyStats = family_gen(random_family)
            village = village_gen(random_village)
            break

        elif main_choice == 2:  # Start Designed Sim, make checks whether family
            # or village are designed by user and asks for confirmation

            if not random_family and not random_village:
                print('Family: ' + ' '.join(familyChar), '\nvillage is: ', village[0], village[1], 'sim'
                      ' speed =', sim_speed)
            elif not random_family and random_village:
                print('Family: ' + ' '.join(familyChar), '\nVillage name and size will be random and sim speed =', sim_speed)
                village = village_gen(random_village)  # case where only village is random, if not generated here causes IndexError: list index out of range at introduction

            elif random_family and not random_village:
                print('Village: ', village[0], village[1], '\nFamily members will be random and sim speed =', sim_speed)
                familyChar, familyStats = family_gen(random_family)
            else:
                print('Nothing designed yet.')
                continue

            if yes_or_no('Do you want to start game with those'
                         ' settings?') == 'no':
                print('\nSetting village and family to random.') # when user not satisfied with designed settings family and village are reset to random
                random_family = True
                familyChar = []
                familyStats = []
                random_village = True
                village = []
                continue
            else:
                break  # in case user accept custom settings game starts with them

        elif main_choice == 3:  # Design Village
            random_village = False
            village = village_gen(random_village)
            continue
        elif main_choice == 4:  # Design Family
            random_family = False
            familyChar, familyStats = family_gen(random_family)
            continue

        elif main_choice == 6:  # Exit Sim
            sys.exit()

    # BEGINNING SCENE
    print('='*79)

    # LULZ. I did it for lulz
    story2 = ['Village ', village[0], ' ', village[2],  # prints village name and date
              '\npopulation size ', str(village[1]), '\nIt is ', weather[0],  # prints population size and weather
              ' and ', weather[1], '. Also ', weather[2], ' and ', weather[3],
              '.\n+', '='*77, '+\n', 'There ', 'is ' if len(intro_family) == 1  # separating == line and random family names doing random thing
              else 'are ', ', '.join(intro_family), ' ',
              random.choice(locations), '.\n', 'All of sudden ', patient_zero,
              ' falls on ground, pale like snow'
              ' and is all in tremors...\n', 'TWIST']

    twist_a = (f'Everybody are shocked...\n{random.choice(intro_family)} crouches trying to help. '
               f'Something terrific happens.\n{patient_zero} turns into a zombie and attacks '
               f'the living.\nBlood rushes forth...\n'               
               f'Soon there are {initial_wave} zombies to brave new world...\n\n')

    twist_b =  'There is nobody at hand to help. After a minute someone notices ' \
               'lying body\n... and runs away.\nMeanwhile %s arises as a' \
               ' zombie and seeks for his first victim.\nThere is' \
               ' just this one zombie to brave new world...\n\n' % patient_zero

    timer = 0
    for item in story2:
        if item == 'TWIST' and len(intro_family) != 1:
            intro_family.remove(patient_zero)
            item = twist_a

        elif item == 'TWIST':
            item = twist_b

        for letter_item in item:
            print(letter_item, end='')
            time.sleep(timer)
            if letter_item == '\n':  # because windows command line doesn't print by letter break will be every newline instead #''.?!+':
                if sim_speed in [1, 2]:
                    time.sleep(1)  # set 1 for release if windows command line
                else:
                    time.sleep(0)
                continue
            elif letter_item in '=':
                timer = 0
            else:
                if sim_speed == 1:
                    timer = 0.01  # set 0 for DEBUGGING and 0.01 RELEASE
                elif sim_speed == 2:
                    timer = 0.01  # set 0 for DEBUGGING and 0.01 RELEASE
                else:
                    timer = 0
                continue


    # time delay after intro scene
    press_enter() if sim_speed in [1, 2] else time.sleep(0)

    # NOW BUNCH OF VARIABLES FOR COMING SIMULATION
    #print('=' * 79)
    # print('TEST')print('TEST2') print('TEST3')  # DEBUGGING
    #fighting_instances = count_fighting_instances()  # 1 for each pair of infected-healthy tiles that touch each other
    pulped_body = 0
    grid_data, houses_number   = gen_grid(village[1])  # takes: population size, returns: grid_data (list of lists) and houses_number(integer)
    family_custom = False  # Is family customised and saved by user ?
    incubation_time = 12                                                        # x5 seconds (one round)
    current_pop     = village[1] - initial_wave                                 # amount of population now, integer
    current_zombies = initial_wave                                              # amount of zombies now, integer
    zed_speed_kmh   = 3.22
    zed_speed       = speed_round(kmh=3.22, delay=4, round_sec=5)               # zombies speed per game round assuming 3.22kmh speed delay rate(average delay caused by eg breaking to home
    town_size       = houses_number * 25                                        # house is 25square meters, in square meters
    houses_dead     = round((village[1] - current_pop) / 4)                                         # amount of houses ravaged by zombies
    wave_size       = round(current_zombies / (houses_number - houses_dead)+1)  # size of next wave that hits family
    round_count     = 1                                                         # how many 5 sec rounds passed
    timer = [0, 0]  # minutes, seconds
    family_cache = 0  # last amount of zombies per cell attacked

    # how much rounds it take to move the swarm to next fight ?
    countdown_set = int(25 / zed_speed) + 1  # 25 meters to go / zombie game speed + 1 because we round up to prevent exception if 0

    # CHOOSING RANDOM TILES FOR PATIENT ZERO AND FAMILY HOUSE LOCATION
    # start of infection
    temp_x = random.randint(0, len(grid_data)-1)
    grid_data[temp_x][random.randint(0, len(grid_data[temp_x])-1)] = '░'

    # family_home location
    while True:  # chosen family coord cannot be infected
        int_y = random.randint(0, len(grid_data) - 1)  # (y coord),(eg 5) represent list number in grid data
        int_x = random.randint(0,len(grid_data[0]) - 1)  # x coord eg 0 represent value number in random list inside grid_data
        family_coord = (int_y, int_x)  # tuple (y, x) eg (5, 0) < - list 5 value 0 of grid_data, is checked after fight and when is '░' triggers family_fight()
        #print(f'I was chosen to be family home {grid_data[int_y][int_x]}, {family_coord}')  #DEBUGGING
        if grid_data[int_y][int_x] != '░':  # checking if chosen coord doesn't contain infected tile
            grid_data[int_y][int_x] = '█'  # turning grid representation to family icon if not infected tile
            break

    #print(f'family coord looks now like = {grid_data[int_y][int_x]}')  # DEBUGGING

    # INITIAL DATA PRINTED OUT
    #print('pop_size =', village[1])
    #print('houses_number =', houses_number, type(houses_number))
    #print('family home number =', family_house)
    #print('initial infected =', initial_wave)
    #print('family attacked by wave size =', wave_size)

    print('=' * 79)
    print('zombie speed =', zed_speed_kmh, 'kmh')
    print(f'population of humans = {current_pop}')
    print('virus incubation time = 60 seconds')
    #print('population of zombies =', current_zombies)  # redundancy with in fight() print
    #print('town size =', town_size, 'square meters')
    #print('houses ravaged =', houses_dead)
    #print(f'zombie game speed = {zed_speed} meters per game round')

    # PRINTING GRID FOR USER FOR FIRST TIME
    print(f' {village[0].upper()}  {village[1]} villagers '.center(79, '='))  # Prints village name and population above grid
    draw_grid_data(grid_data)  # draws first village grid (extended ascii graphic characters), with one infected cell and the family location
    print('=' * 79)
    print('Zombies head toward first house. Victims are unsuspecting...\n')

    # intro game explanation of family cell
    if main_choice == 0:
        print('=' * 79)
        print('On village map grid there is one most bright cell. When infection zone reaches that '
              'spot, family fight is triggered. One family is chosen as example, to represent '
              'simulation in more personal and detailed way.')
        print('=' * 79)

    # time delay after printing grid for the first time
    if sim_speed in [1, 2]:
        press_enter(text='PRESS ENTER TO START APOCALYPSE')
    else:
        time.sleep(0)

    while True:  # main loop for virus spread, each iteration is 5 seconds real time
        # in one round there is 50 % for bite and 55% for instant death of human and 45 % for zombie kill
        # after bite human turns to zombie in incubation_time

        #print('iteration', round_count, ' ', timer, 'seconds')
        #print('family attacked by wave size =', wave_size)
        # print(f'houses ravaged = {houses_dead}/{houses_number}')

        # FIGHT INSTANCE & FAMILY FIGHT INSTANCE INSIDE
        if countdown_set == 0:
            print('=' * 79)
            print(
                f'siege is broken, {current_zombies} zombies attack !')
            print('=' * 79)

            # MAIN FIGHT CALL fight() and its arguments
            grid_data, current_zombies, current_pop, pulped_body, round_count, family_cache = fight(
                grid_data, current_zombies, current_pop, pulped_body,
                village[1], round_count, sim_speed)

            # after each fight draw new grid data
            draw_grid_data(grid_data)

            # FAMILY FIGHT SECTION STARTS
            # after fight check if family_fight() is triggered
            if family_custom != 'dead' and grid_data[family_coord[0]][family_coord[1]] == '░':  # checks if family alive and if family tile in infected cell, if yes triggers family_fight()

                # FAMILY_FIGHT() FUNCTION RUNS HERE !
                family_custom, familyChar, familyStats, zombiesPulped = family_fight(family_cache, familyChar, familyStats, sim_speed, current_pop, current_zombies)

                current_zombies -= zombiesPulped  # reducing amount of zombies by those pulped by family
                pulped_body += zombiesPulped
                if current_zombies < 1:
                    print('Family involvement helped to stop the apocalypse. Humans won !')
                    sys.exit()
            # FAMILY FIGHT SECTION ENDS

            # how much rounds it take to move the swarm to next fight ?
            countdown_set = int(
                25 / zed_speed) + 1  # 25 meters to go / zombie game speed + 1 because we round up to prevent exception if 0

            print(f'\npopulation of humans  = {current_pop}')
            print(f'population of zombies = {current_zombies}     pulped bodies = {pulped_body}\n')

            # time delay at end of fight
            if sim_speed == 1:
                press_enter()
            time.sleep(4) if sim_speed == 2 else time.sleep(0)

        # VARIOUS
        #print(f'countdown to next attack = {countdown_set}')
        countdown_set -= 1

        if current_pop < 1:
            break
        # updating time and iteration
        round_count += 1
        timer[1] += 5
        if timer[1] == 60:
            timer[1] = 0
            timer[0] += 1

        # time delay for zombies moving
        time.sleep(0.05) if sim_speed in [1, 2] else time.sleep(0)
        print(f'{timer[0]}:{timer[1]} min passed')

    print(f'The village has been wiped out in {timer[0]}:{timer[1]} min')
    print('Zombies are crawling among smoldering ruins of {village[0]}.')
    print(f'There are still {pulped_body} pulped corpses left for eating.')

    # PLAY AGAIN ?
    answer = yes_or_no('Do you want to play again ?')
    if answer == 'no':
        print(' ZOMBIES '.center(80, '+'), '\n')
        time.sleep(1)
        print(' S A Y '.center(80), '\n')
        time.sleep(1)
        print(' - T H A N K  Y O U - '.center(80, '$'))
        time.sleep(1)
        break
    else:  # user choose new game, resetting values
        if sim_speed == 1:  # intro game speed will change to default, other speeds won't change
            sim_speed = 2
        random_village = True
        random_family = True
        village = []
        familyChar = []
        familyStats = []
        weather = f_weather('day')
        intro_family, spam = family_gen(True)
        initial_wave = len(intro_family)
        patient_zero = random.choice(intro_family)



