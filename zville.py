#!/usr/bin/env python3

"""
BSD 3-Clause License
Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.
Simulation of zombie virus in village.
"""

import random
import datetime
import sys
import time
# import logging


def draw_grid_data(grid_data):
    """
    Prints grid data.
    :param grid_data: list of lists that are grid
    :return: None
    """
    for y in range(len(grid_data)):  # grid has amount of lists equal to len(grid_data)

        for x in range(len(grid_data[y])):  # each list has values amount len(grid_data[x_list])

            print(' ', end='')  # ads extra space between character in same row to match visuals with default big spaces between columns
            cell = grid_data[y][x]

            if x == len(grid_data[y]) - 1:  # last cell printed with default newline \n
                print(cell)

            else:
                print(cell, end='')


def family_fight(family_cache, familyChar, familyStats, sim_speed, population, zombies):
    """
    family members are not included in population
    family_fight() triggers after fight() when family_coord is in infected cell and family is still alive (family_custom != 'dead')
    family home will be reflected on grid only visually, it will serve as trigger and no other functionality on main grid
    outcome of family fight will affect zombies amount and pulped amount
    if family survives (returns family_custom == 'continue'), they will fight next round with new wave
    :param family_cache: integer, amount of zombies that attacked single cell in previous general fight
                                  used as amount of zombies that will attack the family
    :param familyChar: [Anna, Mark, Tina...]
    :param familyStats: list of lists of integers that are family members personal statistics [(3,3,3,6), (3,3,3,6), ...]
    :param sim_speed: int e.g. 2
    :param population: int 200-2500; needed to check if release of all zombies left is needed when pop=0
    :param zombies: int e.g. 15
    :return: family_custom, familyChar, familyStats, zombiesPulped
    """
    if family_cache > zombies or population < 1:  # no more zombies can attack the family than total zombies
        family_cache = zombies                    # if no population left all zombies attack

    print('=' * 78)
    print(f'The Family has been attacked by {family_cache} zombies.')
    print(f'{familyChar} prepare to defend perimeter.')
    print('=' * 78)

    time.sleep(2) if sim_speed == 2 else time.sleep(0)  # delay at end of each fighting round

    roundNumber = 1  # starting round counter value
    zombiesPulped = 0  # tracks how many zombies family pulped to remove them from global later
    family_casualties = []

    # ADVERSARIES GENERATION. Their numbers and stats are generated each simulation.
    adversaryNumber = family_cache

    # lists of zombie characters and zombie stats of those characters
    zombieChar = ['zombie' + str(i + 1) for i in range(adversaryNumber)]
    zombieStats = []  # stats of all zombies in game instance: physical mental health morale

    for i in range(len(zombieChar)):  # appends stats for all number of zombies user defined
        zombieStats.append([3, 2, 6, 3])

    # COMBAT LOOP
    while familyChar != [] and zombieChar != []:  # Fighting loop continues until one of teams is defeated

        # time delay at end of fight
        if sim_speed == 1:
            print('\n')
            press_enter()
        time.sleep(2) if sim_speed == 2 else time.sleep(0)  # delay at end of each fighting round

        casualties = []  # Append here casualties from below for loop as they happen.

        print('=' * 78, '\nStart of round: ', roundNumber,
              '\n' + '=' * 78)  # Number of round
        print(zombieChar, '\n', familyChar,
              '\n' + '=' * 78)  # Zombies and Family characters going to fight that round

        # FIGHTING ROUND LOOP, each zombie strikes once, then round ends
        for strZombie in zombieChar:  # All zombies attack chosen family member in sequence. That is one round of fight.

            # time delay after each zombie attack
            if sim_speed == 1:
                time.sleep(0.3)
            elif sim_speed == 2:
                time.sleep(0.5)
            else:
                time.sleep(0)

            # Establishing who attacks who in this round:
            currentZombieStats = zombieStats[zombieChar.index(
                strZombie)]  # current zombie stats based on index number of the zombie name currently iterated

            # now stats of random family member
            # found right string in family list (step1)
            if familyChar:  # Checks if there is someone left alive from family.
                currentRandomFamilyName = familyChar[random.randint(0, len(familyChar) - 1)]

            else:  # No living family members
                break

            # step 2 assigning value as list found by index of step1 string
            currentRandomFamilyStats = familyStats[familyChar.index(currentRandomFamilyName)]
            # Prints who attacks who.
            print(strZombie, 'attacks', currentRandomFamilyName, 'and', end=' ')
            # Counting power, comparing and applying damage
            # counting power by physical + k6roll, comparing and adjusting HP
            zombiePower = currentZombieStats[0] + random.randint(1, 6)
            familyPower = currentRandomFamilyStats[0] + random.randint(1, 6)

            if zombiePower > familyPower:  # Zombie hits family
                # decrease HP by amount of power advantage
                powerAdvantage = zombiePower - familyPower  # (phys+k6)-(phys+k6)
                currentRandomFamilyStats[2] -= powerAdvantage  # decrease HP
                # ...adds amount of damage dealt msg...
                print('deals', powerAdvantage, 'damage', end='')

                if currentRandomFamilyStats[2] < 1:  # Family dead
                    del familyStats[familyChar.index(
                        currentRandomFamilyName)]  # remove dead family from stats list
                    familyChar.remove(
                        currentRandomFamilyName)  # removing dead family from string list
                    casualties.append(currentRandomFamilyName)  # for ongoing tracking by round
                    family_casualties.append(currentRandomFamilyName)  # for final summary
                    print(' (', currentRandomFamilyName, ' killed).', sep='')  # ...adds kills who? msg

                else:  # Family hit but survived
                    # Print HP left if family survived
                    print(' (HP left=', currentRandomFamilyStats[2], ').', sep='')

            elif zombiePower < familyPower:  # Family hits zombie
                powerAdvantage = familyPower - zombiePower  # (phys+k6)-(phys+k6)
                currentZombieStats[2] -= powerAdvantage  # decrease HP
                print('suffers', powerAdvantage, 'damage', end='')

                if currentZombieStats[2] < 1:  # Zombie dead
                    print(' (', strZombie, 'killed).', sep='')
                    casualties.append(
                        strZombie)  # Appends dead zombie into list of casualties.

                else:  # Zombie hit but survived
                    # Print HP left if zombie survived
                    print(' (HP left=', currentZombieStats[2], ').', sep='')

            else:  # Nobody has power advantage.
                print(' misses.')  # Counts as miss which is printed out.

        # COMBAT ROUND ENDS, prints round casualties and removes zombies fallen in that round
        if casualties:
            print('=' * 78, '\n', casualties, 'has been killed in this round')

            for dead in casualties:  # iterating through list of strings that contains current round casualties
                if dead in zombieChar:
                    del zombieStats[
                        zombieChar.index(dead)]  # remove dead zombie statistics
                    zombieChar.remove(dead)  # remove dead zombie from string list
                    zombiesPulped += 1

        roundNumber += 1  # rounds counter, loop back up to next round of fight

    # PRINTING END FIGHT SUMMARY
    print('=' * 78, '\nThe fight lasted ', roundNumber * 3,
          'seconds\n' + '=' * 78)
    print('Survivors are: ')
    for x in familyChar:
        print('', x)
    for x in zombieChar:
        print('', x)
    print(f'zombies pulped in this fight {zombiesPulped}. '
          f'Family members killed: {family_casualties}')
    print('=' * 78)

    # time delay at end of fight
    if sim_speed == 1:
        press_enter()
    time.sleep(4) if sim_speed == 2 else time.sleep(0)  # delay at end of each fighting round

    if len(familyChar) > 0:
        family_custom = 'continue'  # when family survived carry them into next family fight
    else:
        family_custom = 'dead'  # when no more family_fight() to trigger

    return family_custom, familyChar, familyStats, zombiesPulped


def family_gen(random_family):
    """ Generates/User input family names and random generates stats for them.
    :param  random_family: True or False - designed)
    :return: [familyChar], [familyStats]
    """
    familyChar = []

    if not random_family:  # user defined family names

        while True:
            name = input('Type family member name or enter to finish:  ')
            if name:
                familyChar.append(name.title())

            elif not name and not familyChar:
                print('Must be at least one name.')
                continue

            elif len(name) > 20:
                print('Name too large. Use no more than 20 characters.')
                continue

            else:  # minimum one name and user hit enter
                break

    elif random_family:  # family size 1 - 8 , most likely  3-6 family , other ranges less likely
        k100_roll = random.randint(1, 100)
        size_f = 0

        if k100_roll in range(1, 51):
            size_f = random.randint(3, 5)  # 3 or 4 or 5 family members
        elif k100_roll in range(51, 81):
            size_f = int(random.choice('126'))  # 1 or 2 or 6 family members
        elif k100_roll in range(81, 101):
            size_f = int(random.choice('78'))  # 7 or 8 family members

        m_txt = open('dictio//names_male.txt')
        f_txt = open('dictio//names_female.txt')
        male_names = m_txt.read().split('\n')  # all male names list
        female_names = f_txt.read().split('\n')  # all female names list

        while True:
            if size_f == 2:
                if random.randint(1, 100) < 80:  # if family 2 members there is 80 % gender is opposite
                    familyChar.append(random.choice(male_names))
                    familyChar.append(random.choice(female_names))
                    break

            for index in range(size_f):
                gender = random.choice('mf')

                if gender == 'm':
                    familyChar.append(random.choice(male_names))

                elif gender == 'f':
                    familyChar.append(random.choice(female_names))
            break

        m_txt.close()
        f_txt.close()

    familyStats = []  # stats of family members [physical, mental, HP, morale]

    for i in familyChar:  # returns random stats of family members
        physical = random.randint(2, 5)
        mental = random.randint(2, 5)
        HP = physical * 2  # HP is double of physical
        morale = 3  # not implemented
        familyStats.append([physical, mental, HP, morale])

    assert len(familyChar) > 0, 'FAMILY_CHAR LIST IS EMPTY'

    return familyChar, familyStats


def fight(grid, zombies, population, pulped, rounds_passed, sim_speed):
    """ counts infected tiles, amount of zombies and defenders to fight, makes them fight, adds new infected zones based on human casualties
    # example use: grid_data, zombies, population, pulped, round_count = fight(grid=grid_data, zombies=5, population=1495, pulped=0, init_pop=1500, rounds_passed=26)
    :param grid: grid data list of lists with ASCII graph values that are single cell representation
    :param zombies: int e.g. 15
    :param population: int in range(200, 2501)
    :param pulped: int, 'dead' zombies
    :param rounds_passed will be concatenated with rounds_count and returned as new_time
    :param sim_speed in [1,2,3], int
    :return: updated grid, new zombies amount, new population amount, new pulped amount, new time
    """
    zombies_start_amount = zombies  # for tracking zombie&human casualties for printing out
    humans_start_amount = population

    # healthy_tiles, infected_tiles coord, grid_attacked coord

    infected_tiles = []  # expected format tuples of coord eg [(1, 4), (2, 3)]
    grid_attacked = []  # expected format tuples of coord eg [(1, 4), (2, 3)]
    healthy_tiles = 0
    rounds_count = 1  # tracks time of fight, each round 5 seconds, returns concatenated with rounds_passed parameter

    for y in range(len(grid)):  # iterates through each list contained in grid # y is instance of list
        """
        1. it searches grid to find infected tile
        2. when it find infected it search all 8 tiles around for healthy tile
        3. if healthy and not already in list, appends healthy into list and breaks
        # 1. counts healthy tiles,
        # 2. makes list of infected tiles coord eg [(1, 4), (2, 3)]
        # 3. makes list of grid_attacked coord eg [(1, 4), (2, 3)]
        """
        for x in range(len(grid[y])):  # iterates through all values contained in list instance y # x is instance of value

            if grid[y][x] in ['▓', '█']:  # 1. counts healthy tiles,
                healthy_tiles += 1
            if grid[y][x] == '░':  # 2 & 3

                infected_tiles.append((y, x))  # 2. makes list of infected tiles coord eg [(1, 4), (2, 3)]

                # scan around infected tile for healthy tiles, add coord of first one to grid_attacked if not already present
                # area_scan = [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]  # N, NE, E, SE, S, SW, W, NW
                for ry, rx in [(y-1, x), (y-1, x+1), (y, x+1), (y+1, x+1), (y+1, x), (y+1, x-1), (y, x-1), (y-1, x-1)]:  # rx relative x ry relative y
                    try:  # ref 'fry65' affected by chosen family tile graphical representation
                        if ry >= 0 and rx >= 0 and grid[ry][rx] in ['▓', '█'] and (ry, rx) not in grid_attacked:  # absolute coord must be 0+ otherwise they are out of grid
                            grid_attacked.append((ry, rx))  # 3. makes list of grid_attacked coord eg [(1, 4), (2, 3)]
                            break  # why it breaks ? Because infected tile found his victim healthy tile
                    except IndexError:  # in case searched coord is of out of range, except ignores error
                        pass

    # REMOVING ATTACKED TILES IF NOT ENOUGH ZOMBIES - to maintain siege needed 1 + (3 * per extra cell)
    zombies_needed_for_siege = 1 + (3 * len(grid_attacked))

    while len(grid_attacked) > 1 and zombies_needed_for_siege > zombies:

        del grid_attacked[random.randint(0, len(grid_attacked) - 1)]
        zombies_needed_for_siege -= 3

    # HOW MANY ZOMBIES ATTACKED SINGLE CELL - needed as argument for family_fight(), that many zombies will attack the family
    family_cache = round(zombies / len(grid_attacked))  # average number of zombies per attacked cell

    # DEFENDERS AGAINST ZOMBIES
    pop_fighting = int(population / healthy_tiles * len(grid_attacked))

    if pop_fighting < 1:  # minimum 1 stand to defend home
        print('# minimum 1 stand to defend home')  # DEBUGGING
        pop_fighting = 1

    if healthy_tiles == len(grid_attacked):  # last stand, every villager turns into defender
        print('last stand, every villager turns into defender')
        pop_fighting = population

    print(f'                 {pop_fighting} defenders       {len(grid_attacked)} homes affected')  # 17 spaces to match "siege is broken, "
    print('=' * 79)
    if sim_speed in [2]:
        time.sleep(3)

    # MAIN FIGHT
    pile = 0  # amount of zombies pulped in one round
    bitten = 0  # amount of bitten, each 12 rounds that turns to zombies and resets
    bitten_to_zombie = 0

    if sim_speed == 1:
        press_enter()

    while zombies > 0 and pop_fighting > 0 or pop_fighting == 0 and bitten > 0:

        for i in range(zombies):  # one round, each zombie attack defender
            if pop_fighting > 0:
                if zombies > 1:
                    roll = random.randint(1, 100)

                else:  # let's increase chances of survival for last zombie by 2 times
                    roll = random.randint(1, 2)

                    if roll == 1:
                        roll = random.randint(1, 65)

                    else:
                        roll = random.randint(66, 90)  # human dead 66 - 85 or zombie pulped 86 - 90 # zombie doubles his chances

                if roll <= 65:
                    pass

                    # 40% for adding a bite when not already bitten
                    if pop_fighting > 1 and bitten < pop_fighting and random.randint(1, 100) <= 40:
                        # bitten = 1
                        # fighting = 2
                        # i = random(bitten: 1, fighting: 2)
                        # if i > bitten then bitten += 1
                        if random.randint(bitten, pop_fighting) > bitten:
                            bitten += 1

                            if bitten_to_zombie == 0:  # adding infection counter if not already running
                                bitten_to_zombie = rounds_count + 11  # infected turn into zombies each 60 seconds since first of them is bitten

                elif roll <= 85:  # roll 66 - 85 human dies, zombie raises
                    # how to find if one who died was bitten before ?
                    # pop_fighting = 2
                    # bitten = 1
                    # i = random.randint(1, pop_fighting:2)
                    # if i <= bitten then bitten -= 1
                    if bitten == 1 and pop_fighting == 1:  # when last defender that died was already bitten
                        bitten = 0

                    elif bitten > 0 and pop_fighting > 1 and random.randint(1, pop_fighting) <= bitten:  # check if dead human was bitten before, to remove amount of infected
                        bitten -= 1

                    print('human dies ', end='\n')
                    time.sleep(0.01) if sim_speed in [1, 2] else time.sleep(0)
                    pop_fighting -= 1
                    population -= 1
                    pile -= 1  # new zombie will raise

                else:  # roll 86 - 100 zombie pulped
                    print('zombie pulped ', end='\n')
                    time.sleep(0.01) if sim_speed in [1, 2] else time.sleep(0)

                    pulped += 1  # added to pulped bodies
                    pile += 1  # zombie will be removed

        rounds_count += 1

        # infected turn zombie
        if rounds_count == bitten_to_zombie:
            pile -= bitten
            print(f'\n{bitten} infected humans are turning into zombies !!!')
            time.sleep(0.5) if sim_speed in [1, 2] else time.sleep(0)
            pop_fighting -= bitten
            population -= bitten
            bitten = 0
            bitten_to_zombie = 0

        zombies -= pile  # adjusting number of zombies by pulped/raised in round
        pile = 0  # resetting pulped pile

        # time delay between rounds
        time.sleep(0.2) if sim_speed in [1, 2] else time.sleep(0)  # delay at end of each fighting round

        if zombies < 1:  # new game condition
            print('\nZombies has been stopped. Humanity is saved')
            family_cache = 'humans_won'
            return '', '', '', '', '', family_cache  # empty values matching expected return

    # ADDING NEW INFECTED TILES
    # rule of thumb total infected tiles = population_removed / 4 | (pulped + zombies) / 4
    # minimum one infected tile should be added
    # infected tile should be added until rule of thumb is met or grid_attacked pool is depleted
    infected_tiles_amount = len(infected_tiles)
    infected_added_this_fight = 0
    while True:
        if population == 0:  # end game condition, turning all into infected

            for y, x in grid_attacked:  # e.g. [(4, 1), (4, 0)]
                grid[y][x] = '░'
                infected_added_this_fight += 1
            break

        # turn random choice tile from grid_attacked into infected
        temp_yx = random.choice(grid_attacked)  # tuple with y, x coord
        grid[temp_yx[0]][temp_yx[1]] = '░'
        grid_attacked.remove(temp_yx)
        infected_tiles_amount += 1
        infected_added_this_fight += 1

        # break loop when rule of thumb met or pool depleted
        if len(grid_attacked) == 0 or infected_tiles_amount >= round((pulped + zombies) / 4):  # RULE OF FUCKING THUMB MET
            break

    print('\n' + '=' * 79)
    print(f'Homes seized = {infected_added_this_fight}  Time = {rounds_count *5}s   '
          f'Zombie increase = {(zombies_start_amount - zombies) * -1}   '
          f'Human dead = {humans_start_amount - population}')
    print('=' * 79)
    new_time = rounds_passed + rounds_count

    # time delay at end of fight
    if sim_speed == 1:
        press_enter()
    time.sleep(4) if sim_speed == 2 else time.sleep(0)  # delay at end of each fighting round
    assert population >= 0, 'Population amount to return in fight() -> less than zero.'

    return grid, zombies, population, pulped, new_time, family_cache


def gen_grid(population):
    """ Generates grid data (each house is one grid cell)
    :param population: eg 1125
    :return: grid_data eg [[▓,▓,▓], [▓,▓,▓]], houses_number e.g. 289
    """
    # grid amount must be less or equal to population eg grid_x * grid_y * 4 <= population
    y_example, x_example = 7, 7  # minimum grid covers population 200 (196), that is why gen_village has forced 200 population minimum
    y_lists = 7
    x_values = 7

    iteration = 0  # evens odds checks
    while True:
        iteration += 1
        if y_example * x_example * 4 > population:  # checks if next operation WON'T exceed allowable amount
            break
        else:
            y_lists, x_values = y_example, x_example  # example passed check, return values updated

        if iteration % 2:  # if odds
            x_example += 1
        elif not iteration % 2:  # if evens
            y_example += 1

    # list comprehension returns grid which (y * x * 4) == nearest <=population_size, e.g. grid (7 * 7) is most close and <= population 200
    grid = [['▓'] * x_values for i in range(y_lists)]
    houses_number = x_values * y_lists

    return grid, houses_number


def intro_sim(story):  # Runs when user choose Intro Game
    """ Text intro for game take story string and prints it out by letter
    :return: None
    """
    # printing out the story by letter at speed defined in time.sleep below
    print('=' * 79)

    for item in story:
        print(item, end='', sep='')
        if item in '.?!':
            time.sleep(0.5)
            continue
        time.sleep(0.03)

    print('=' * 79)
    time.sleep(2)


def press_enter(text='PRESS ENTER'):
    """ Prints PRESS ENTER repeatedly until user presses enter, then breaks from loop
        if argument is provided in format text='something' it is used instead of default PRESS ENTER
    """
    while True:
        spam = input(text)
        if not spam:
            break


def village_gen(random_village):
    """ GENERATES RANDOM VILLAGE OR USER CUSTOMISED
    :takes True|False random True or custom False
    :returns village_name, pop_size, time
    """
    if not random_village:  # user designed village

        while True:  # return village name and correct size

            try:
                village_name, pop_size = input(
                    '\nEnter village name and population size '
                    'between 200 and 2500\nfor example: Yeovil 1500\n').split()
                if not pop_size.isdecimal():
                    print('Wrong format for population size. Enter integer.')
                    continue
                if not pop_size or int(pop_size) not in range(200, 2501):
                    continue
            except ValueError:
                print('Something went wrong. Try again.')
                continue

            else:
                print('Your choice is ', village_name, pop_size, 'Is that '
                                                                 'correct? '
                                                                 '(y)|(n)')
                spam = input()
                if spam.lower() == 'y':
                    pop_size = int(pop_size)  # must be turned to integer to prevent TypeError: '>' not supported between instances of 'int' and 'str' in gen_grid()
                    break
                else:
                    continue
        assert pop_size in range(200, 2501), 'population not 200-2500 NOT-RANDOM'
        assert village_name, 'user defined village has no name'

    else:  # random village
        spam = open('dictio//names_village.txt')
        village_name = random.choice(spam.read().split('\n'))
        spam.close()
        pop_size = random.randint(200, 2500)  # must be between 200 - 2500 for code consistency with alg1:min 4 pop per home alg2: chooses x,y grid size

    assert village_name, 'village name missing in gen function'
    assert pop_size, 'no population size generated in gen function'
    time_x = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return [village_name.title(), pop_size, time_x]


def user_menu_choice():
    """  MAIN MENU
    Can exit game on user choice 6
    :return: integer representing user choice from main menu
    """
    print('='*80)
    print('+' * 30 + ' OUTBREAK IN ZVILLE ' + '+' * 30)
    menu_choices = ['Intro Game', 'Start Random Sim', 'Start Designed Sim',
                    'Design Village', 'Design Family', 'Set Sim Speed', 'Exit']

    for item in menu_choices:
        print(str(menu_choices.index(item)) + '. ' + item +
              ' '.join(['' for i in range(21 - len(item))]) + '+')

    main_choice = []
    while main_choice not in range(len(menu_choices)):
        main_choice = input()
        if main_choice == str(menu_choices.index('Exit')):  # quits game if user chose '1'
            sys.exit()
        elif main_choice.isdigit() and int(main_choice) \
                in range(len(menu_choices)):  # user choses number in range of options available
            return int(main_choice)
        else:
            print('Choose number corresponding to an option')


def speed_round(kmh, delay, round_sec):
    """
    Calculates speed in meters per game round
    # How many meters zombies move in 5 sec game round at speed 1kmh ?
    # How many meters per second is 1 kilometer per hour = 1000 in 3600 =  10m in 36s = 10/36 in 1s = 10/36*5 in 1 round = 1.38m per round(5sec)
    # 1kmh = 1000m in 3600 seconds = 1000 in 720 game rounds = 1000/720m in 1 round = 1.38m per round(5sec)
    # answer is = 1.38m/round, so if zombies have speed 3.22kmh their game speed is 3.22 * 1.38mpr = 4.44 meters per 5 second round
    :param kmh: speed in kilometers per hour
    :param delay: delay caused by some stuff eg besieging houses, kmh=1/delay
    :param round_sec: length of game round/iteration per second
    :return: float (speed in meters per game iteration/round)
    """
    speed = (kmh * 1000 / 3600) / delay * round_sec
    return speed


def f_weather(daytime):
    """
    Generates list of strings depicting weather depending on time of day.
    :param daytime: 'day'|'night'
    :return: list of strings [wind strength, brightness, is_rain]
    """
    if daytime == 'day':
        weather = (('calm', 'calm', 'calm', 'light breeze', 'light breeze',
                    'light breeze', 'windy', 'windy', 'strong wind'),
                   ('sunshine', 'bright', 'bright', 'cloudy', 'cloudy',
                    'cloudy', 'dark'),
                   ('dry', 'dry', 'damp', 'light rain', 'rains'), ('is warm', 'is cool', 'is hot',
                                                                   'is cold', 'is moderately warm'))
        
        r_weather = (f'It is {random.choice(weather[0])} and {random.choice(weather[1])}. Also '
                     f'{random.choice(weather[2])} and {random.choice(weather[3])}.')

        return r_weather


def yes_or_no(question):  # Returns 'yes' or 'no' based on first letter of user input.

    while True:
        item = input(question)
        if not item or item[0].lower() not in ['y', 'n']:
            print('(y)es or (n)o are valid answers')
            continue
        elif item[0].lower() == 'y':
            return 'yes'
        elif item[0].lower() == 'n':
            return 'no'
