#! python3
"""
BSD 3-Clause License

Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.

Simulation of zombie attack on family.
"""

import random  # Used for random k6rolls to powerAdvantage resolution
import sys  # Used to quit game on user enter input at choosing zombies number
import time  # Used for delay between zombie hits
from zville_functions import intro_game, user_menu_choice, village_gen, \
    family_gen, yes_or_no, weather, draw_grid_data, gen_grid, speed_round
from zville_functions import fight

story = """A STORY. How shit hit the fun?
An isolated village. 
Great place for testing stuff on human subjects, isn't it?    
Concerns about value of human life, dignity and work ethics since long had 
their own spin-off. 
Something happened, let's call it ... 
LACK OF TRANSPARENCY. 
A viral sample has been released.     
Somewhere in the village, patient zero has been exposed to a sample.  
"""

savedFamily = []  # List of family characters from which each game run will resets family members alive
sim_speed = 1
random_village = True
random_family = True
village = []
familyChar = []
familyStats = []
weather = weather('day')
locations = ['walking in a park', 'packing stuff into a car\'s trunk',
             'watching a big TV in a saloon', 'playing a game of cards',
             'quarreling passionately']
intro_family, spam = family_gen(True)  # random names for game story family spam is to hold trash overflow data returned by function
initial_wave = len(intro_family)
print(intro_family)
patient_zero = random.choice(intro_family)
print(patient_zero)

while True:  # MAIN LOOP

    while True:  # Handles user menu choices before game starts
        main_choice = user_menu_choice()  # Main game menu returns integer

        if main_choice == 0:  # Intro game
            intro_game(story)  # Intro story
            random_family = True
            random_village = True
            familyChar, familyStats = family_gen(random_family)
            village = village_gen(random_village)
            sim_speed = 2  # Speed is set slower because its probably first game
            break

        elif main_choice == 5:  # Set Sim Speed
            while True:
                sim_speed = input('Set sim speed between 0.2(slowest) to'
                                  ' 10.0 (ultra fast). Default is 1')
                if sim_speed.isdecimal() and float(sim_speed) < 10.1:
                    if float(sim_speed) < 0.1:
                        sim_speed = 1
                    print('sim speed set =', sim_speed)
                    sim_speed = 1/float(sim_speed)
                    break
            continue

        elif main_choice == 1:  # Start Random Sim
            random_family = True  # Not implemented
            random_village = True
            familyChar, familyStats = family_gen(random_family)
            village = village_gen(random_village)
            break

        elif main_choice == 2:  # Start Designed Sim, make checks whether family
            # or village are designed by user and asks for confirmation

            if not random_family and not random_village:
                print('Family: ' + ''.join(familyChar), '\n', village[:-1], 'sim'
                      ' speed =', sim_speed)
            elif not random_family and random_village:
                print('Family: ' + ' '.join(familyChar), '\nVillage name and '
                                                         'size '
                      'will be random and sim speed =', sim_speed)
            elif random_family and not random_village:
                print('Village: '+' '.join(village[:-1]), '\nFamily members '
                      'will be random and sim speed =', sim_speed)
            else:
                print('Nothing designed yet.')
                continue

            if yes_or_no('Do you want to start game with those'
                         ' settings?') == 'no':
                continue
            else:
                print('Setting village and family to random.')
                random_family = True
                random_village = True
                break

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

    print('='*79)
    # Do not worry. That is just a list of strings :D.

    story = ['Village ', village[0], ' ', village[2],  # prints village name and date
             '\npopulation size ', str(village[1]), '\nIt is ', weather[0],  # prints population size and weather
             ' and ', weather[1], '. Also ', weather[2], ' and ', weather[3],
             '.\n+', '='*77, '+\n', 'There ', 'is ' if len(intro_family) == 1  # separating == line and random family names doing random thing
             else 'are ', ', '.join(intro_family), ' ',
             random.choice(locations), '.\n', 'All of sudden ', patient_zero,
             ' falls on ground, pale like snow'
             ' and is all in tremors...\n', 'TWIST']
    twist_a = '%s are shocked...\n%s ' \
                   'crouches trying to help. Something terrific happens.\n' \
                   '%s turns into a zombie and bites his benefactor.\n' \
                   'Blood rushes forth.\n' \
                   'There are %d zombies to brave new world...\n' \
                   % (', '.join(intro_family), random.choice(intro_family), patient_zero, initial_wave)
    twist_b = 'There is nobody at hand to help. After a minute someone notices ' \
                   'lying body\n... and runs away.\nMeanwhile %s arises as a' \
                   ' zombie and seeks for his first victim.\nThere is' \
                   ' just this one zombie to brave new world...\n' % patient_zero

    timer = 0
    for item in story:
        if item == 'TWIST' and len(intro_family) != 1:
            intro_family.remove(patient_zero)
            item = twist_a

        elif item == 'TWIST':
            item = twist_b

        for letter_item in item:
            print(letter_item, end='')
            time.sleep(timer)
            if letter_item in '.?!+':
                time.sleep(0)  # DEBUGGING set 0.2 for release
                continue
            elif letter_item in '=':
                timer = 0
            else:
                timer = 0  # DEBUGGING set 0.01 for release
                continue

    #print('=' * 79)
    # print('TEST')print('TEST2') print('TEST3')  # DEBUGGING
    #fighting_instances = count_fighting_instances()  # 1 for each pair of infected-healthy tiles that touch each other
    pulped_body = 0
    grid_data, houses_number   = gen_grid(village[1])  # takes: population size, returns: grid_data (list of lists) and houses_number(integer)
    family_house    = random.randint(1, houses_number)
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

    # how much rounds it take to move the swarm to next fight ?
    countdown_set = int(25 / zed_speed) + 1  # 25 meters to go / zombie game speed + 1 because we round up to prevent exception if 0

    # choosing random grid for start of infection
    temp_x = random.randint(0, len(grid_data)-1)
    grid_data[temp_x][random.randint(0, len(grid_data[temp_x])-1)] = '░'

    # printing some initial info
    #print('pop_size =', village[1])
    #print('houses_number =', houses_number, type(houses_number))
    #print('family home number =', family_house)
    #print('initial infected =', initial_wave)
    #print('family attacked by wave size =', wave_size)

    print('=' * 79)
    print('zombie speed =', zed_speed_kmh, 'kmh')
    print('population of humans = {current}/{total}'.format(current=current_pop,
                                                            total=village[1]))
    print('virus incubation time = 60 seconds')
    #print('population of zombies =', current_zombies)  # redundancy with in fight() print
    #print('town size =', town_size, 'square meters')
    #print('houses ravaged =', houses_dead)
    #print(f'zombie game speed = {zed_speed} meters per game round')
    print('=' * 79)
    draw_grid_data(grid_data)
    print('=' * 79)
    print('Zombies head toward first house. Victims are unsuspecting...')
    input('Press any key to start apocalypse')

    while True:  # main loop for virus spread, each iteration is 5 seconds real time
        # in one round there is 50 % for bite and 55% for instant death of human and 45 % for zombie kill
        # after bite human turns to zombie in incubation_time

        #print('iteration', round_count, ' ', timer, 'seconds')


        #print('family attacked by wave size =', wave_size)
        # print(f'houses ravaged = {houses_dead}/{houses_number}')

        if countdown_set == 0:
            print('=' * 79)
            print(
                f'siege is broken, {current_zombies} zombies swarming the living...')
            print('=' * 79)
            time.sleep(0.5)
            grid_data, current_zombies, current_pop, pulped_body, round_count = fight(
                grid_data, current_zombies, current_pop, pulped_body,
                village[1], round_count)
            # after each fight draw new grid data
            draw_grid_data(grid_data)
            # how much rounds it take to move the swarm to next fight ?
            countdown_set = int(
                25 / zed_speed) + 1  # 25 meters to go / zombie game speed + 1 because we round up to prevent exception if 0
            print('population of humans = {current}/{total}'.format(
                current=current_pop,
                total=village[1]))
            print('population of zombies =', current_zombies)
            print(f'pulped = {pulped_body}')
            # input('press any key')
            time.sleep(0.5)

        # print(f'countdown to next attack = {countdown_set}')
        time.sleep(0.02)
        countdown_set -= 1

        if current_pop < 1:
            break
        # updating time and iteration
        round_count += 1
        timer[1] += 5
        if timer[1] == 60:
            timer[1] = 0
            timer[0] += 1
        # print(f'{timer[0]}:{timer[1]} min passed')

    print(f'zombies wiped out the village in {timer[0]}:{timer[1]} min')
    break


