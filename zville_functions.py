#! python 3
"""
BSD 3-Clause License

Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.

Simulation of zombie attack on family.
"""
import random, datetime, sys, time  # standard library


def draw_grid_data(grid_data):
    """
    Prints grid data.
    :param grid_data: list of lists that are grid
    :return: None
    """
    for x_list in grid_data:  # grid has amount of lists exual to len(grid_data)
        counter = 0  # to track when print next line (end=)

        for y_value in x_list:  # each list has values amount len(grid_data[x_list])
            print(' ', end='')  # ads extra spece between character in same row to match visuals with default big spaces between columns

            if counter == len(x_list) - 1:
                print(y_value)
            else:
                print(y_value, end='')

            counter += 1


def fight(grid, zombies, population, pulped, init_pop, rounds_passed):
    """ counts infected tiles, amount of zombies and defenders to fight, makes them fight, adds new infected zones based on human casualties
    # example use: grid_data, zombies, population, pulped, round_count = fight(grid=grid_data, zombies=5, population=1495, pulped=0, init_pop=1500, rounds_passed=26)
    :param grid:
    :param zombies:
    :param population:
    :param pulped:
    :param init_pop:
    :param rounds_passed will be concatenated with rounds_count and returned as new_time
    :return: updated grid, new zombies amount, new population amount, new pulped amount, new time
    """

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

            if grid[y][x] == '▓':  # 1. counts healthy tiles,
                healthy_tiles += 1
            if grid[y][x] == '░':  # 2 & 3

                infected_tiles.append((y, x))  # 2. makes list of infected tiles coord eg [(1, 4), (2, 3)]

                # scan around infected tile for healthy tiles, add coord of first one to grid_attacked if not already present
                # area_scan = [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]  # N, NE, E, SE, S, SW, W, NW
                for ry, rx in [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]:  # rx relative x ry relative y
                    try:
                        if ry >= 0 and rx >= 0 and grid[ry][rx] == '▓' and (ry, rx) not in grid_attacked:  # absolute coord must be 0+ otherwise they are out of grid
                            grid_attacked.append((ry, rx))  # 3. makes list of grid_attacked coord eg [(1, 4), (2, 3)]
                            break  # why it breaks ? Because infected tile found his victim healthy tile
                    except IndexError:  # in case searched coord is of out of range, except ignores error
                        pass

    # removing attacked tiles if not enough zombies to maintain siege eg 1 + (3 * per extra cell)
    print(f'initial grid attacked = {len(grid_attacked)}')  # DEBUGGING
    zombies_needed_for_siege = 1 + (3 * len(grid_attacked))
    print(f'zombies needed for siege = {zombies_needed_for_siege}')  # DEBUGGING

    while len(grid_attacked) > 1 and zombies_needed_for_siege > zombies:
        print(f'grid attacked {grid_attacked}')
        del grid_attacked[random.randint(0, len(grid_attacked) - 1)]
        print(f'one less cell will be attacked due to insufficient amount of zeds')  # DEBUGGING
        zombies_needed_for_siege -= 3
        print(f'zombies needed for siege = {zombies_needed_for_siege}')  # DEBUGGING

    # DEBUGGING

    print(f'infected tiles = {len(infected_tiles)}')  # DEBUGGING
    #print(f'healthy tiles = {healthy_tiles}')
    print(f'healthy tiles attacked = {len(grid_attacked)}, {grid_attacked}')  # DEBUGGING

    # figuring out population fighting versus zombies

    pop_fighting = int(population / healthy_tiles * len(grid_attacked))
    # i want leave minimum population out of fight that is healthy tiles - attacked tiles * 4

    # loop trimming population due to fight, to prevent leaving empty houses at end
    print(f'DEFENDERS before loop = {pop_fighting}')  # DEBUGGING
    while population - pop_fighting < (healthy_tiles - len(grid_attacked)) * 4 and pop_fighting > len(grid_attacked):
        pop_fighting -= 1
    # while populationNotFighting (1116) < housesAtPeace (287) * 4 (1148)   AND  popFighting > tilesAttacked

    print(f'DEFENDERS after loop = {pop_fighting}')  # DEBUGGING

    if pop_fighting < 1:  # minimum 1 stand to defend home
        print('# minimum 1 stand to defend home')  # DEBUGGING
        pop_fighting = 1

    if healthy_tiles == len(grid_attacked):  # last stand, every villager turns into defender
        print('last stand, every villager turns into defender')
        pop_fighting = population

    print(f'DEFENDERS final = {pop_fighting}')  # DEBUGGING

    pile = 0  # amount of zombies pulped in one round
    bitten = 0  # amount of bitten, each 12 rounds that turns to zombies and resets
    bitten_to_zombie = 0

    while zombies > 0 and pop_fighting > 0 or pop_fighting == 0 and bitten > 0:

        #print(f'round number = {rounds_count}')
        #print(f'zombies for round = {zombies}')
        #print(f'defenders for round = {pop_fighting}')
        for i in range(zombies):  #  one round, each zombie attack defender
            #print(f'bitten ={bitten}')

            if pop_fighting > 0:
                if zombies > 1:
                    roll = random.randint(1, 100)
                else:  # let's increase chances of survival for last zombie by 4 times
                    roll = random.randint(1, 2)
                    if roll == 1:
                        roll = random.randint(1, 65)
                    else:
                        roll = random.randint(66, 90)  # human dead 66 - 85 or zombie pulped 86 - 90 # zombie doubles his chances
                        print('ONLY ONE ZOMBIE LEFT, his choice roll is ', roll)  # DEBUGGING
                #print(f'roll is = {roll}')
                if roll <= 65:
                    pass
                    #print('one draws')

                    # 40% for adding a bite when not already bitten
                    if pop_fighting > 1 and bitten < pop_fighting and random.randint(1, 100) <= 40:
                        # bitten = 1
                        # fighting = 2
                        # i = random(bitten: 1, fighting: 2)
                        # if i > bitten then bitten += 1
                        if random.randint(bitten, pop_fighting) > bitten:
                            bitten += 1
                            #print('I am bitten !')
                            if bitten_to_zombie == 0:  # adding infection counter if not already running
                                #print(f'first human bit, adding infection counter')
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

                    print('human dies ', end='')
                    #time.sleep(0.001)
                    pop_fighting -= 1
                    population -= 1
                    pile -= 1  # new zombie will raise

                else:  # roll 86 - 100 zombie pulped
                    print('zombie pulped ', end='')
                    #time.sleep(0.001)

                    pulped += 1  # added to pulped bodies
                    pile += 1  # zombie will be removed

        rounds_count += 1

        # infected turn zombie
        if rounds_count == bitten_to_zombie:
            pile -= bitten
            print(f'\n{bitten} infected humans are turning into zombies !!!')
            pop_fighting -= bitten
            population -= bitten
            bitten = 0
            bitten_to_zombie = 0
            # need to remove infected turned from pop_fighting
            # need to calculate if dead human is one that was bitten

        zombies -= pile  # adjusting number of zombies by pulped/raised in round
        pile = 0  # resetting pulped pile
        if zombies < 1:
            print('Zombies has been stopped. Humanity is saved')
            sys.exit()

    print('\n' + '=' * 79)
    print(f'zombies swarmed through defenders in {rounds_count *5} seconds')
    print('=' * 79)
    time.sleep(1)

    # ADDING NEW INFECTED TILES
    # rule of thumb total infected tiles = population_removed / 4 | (pulped + zombies) / 4
    # minimum one infected tile should be added
    # infected tile should be added until rule of thumb is met or grid_attacked pool is depleted

    infected_tiles_amount = len(infected_tiles)
    infected_added_this_fight = 0
    while True:
        if population == 0:  # end game condition, turning all into infected
            # example of grid_attacked is [(4, 1), (4, 0)]
            print('HEALTHY EQUAL TO ATTACKED, ALL GRID SHOULD TURN INFECTED OR EDIT CODE FOR BETTER ALGORITM')
            print(f'grid attacked is = {grid_attacked}')
            print('algoritm used to add it is grid[y][x] == \'░\'')
            for y, x in grid_attacked:
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
    print(f'infected tiles added this fight = {infected_added_this_fight}')  # DEBUGGING
    new_time = rounds_passed + rounds_count
    return grid, zombies, population, pulped, new_time


def gen_grid(population):
    """ Generates grid data (each house is one grid cell)
    example use: grid = gen_grid(1125); print(f'lists = {len(grid)}, values = {len(grid[0])}, population = {len(grid)*len(grid[0]*4)}')
    :param population: eg 1125
    :return: grid_data eg [[▓,▓,▓], [▓,▓,▓]]
             houses_number eg 289
    """
    # grid amount must be less or equal to population eg grid_x * grid_y * 4 <= population

    y_example, x_example = 7, 7  # minimum grid covers population 200 (196)
    y_lists = 7
    x_values = 7

    iteration = 0  # to check parzyste / nieparzyste
    while True:
        iteration += 1
        #print(iteration)  # DEBUGGING

        if y_example * x_example * 4 > population:  # checks if next operation WON'T exceed allowable amount
            break
        else:
            y_lists, x_values = y_example, x_example  # example passed check, return values updated

        if iteration % 2:  # if nieparzyste
            x_example += 1
        elif not iteration % 2:  # if parzyste
            y_example += 1

        # print(f'y_example = {y_example}, x_example = {x_example}')  # DEBUGGING

    grid = [['▓'] * x_values for i in range(y_lists)]  # list comprehension returns grid which y * x * 4 are as close as possible to population while not exceeding it eg grid 7 * 7 is most close to population 200
    houses_number = x_values * y_lists
    # print(f'lists = {len(grid)}, values = {len(grid[0])}, population = {len(grid)*len(grid[0]*4)}')  # DEBUGGING

    return grid, houses_number


def intro_game(story):  # Runs when user choose Intro Game
    """ Text intro for game take story string and prints it out by letter
    :return: None
    """
    # printing out the story by letter at speed defined in time.sleep below
    print('=' * 79)
    for item in story:
        print(item, end='', sep='')
        if item in '.?!':
            time.sleep(0)  # DEBUGGING change for 1 for release
            continue
        time.sleep(0)  # DEBUGGING temporary ultra speed , change for 0.03 for release
    print('=' * 79)
    input('PRESS A KEY')


def village_gen(random_village):
    """ GENERATES RANDOM VILLAGE OR USER CUSTOMISED
    :takes True|False random True or custom False
    :returns village_name, pop_size, time
    """
    if not random_village:  # user designed village
        while True:  # return village name and correct size

            try:
                village_name, pop_size = input(
                    'Enter village name and population size '
                    'between 200 and 2500 eg. Yeovil '
                    '1500').split()
                if not pop_size.isdecimal():
                    print('Wrong format for population size. Enter integer.')
                    continue
                if not pop_size or int(pop_size) not in range(100, 2501):
                    continue

            except:
                print('Something went wrong')
            else:
                print('Your choice is ', village_name, pop_size, 'Is that '
                                                                 'correct? '
                                                                 '(y)|(n)')
                spam = input()
                if spam.lower() == 'y':
                    break
                else:
                    continue

    elif random_village:
        spam = open('dictio//names_village.txt')
        village_name = random.choice(spam.read().split('\n'))
        spam.close()
        pop_size = random.randint(100, 2500)

    timeX = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return [village_name.title(), pop_size, timeX]


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


def family_gen(random_family):
    """ Generates/User input family names and random generates stats for them.
    :param  random_family True or False - random or custom genration
    :return: [familyChar], [familyStats]
    """
    familyChar = []

    if not random_family:  # user defined family names
        while True:
            name = input('Type family member name or enter:  ')
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
        elif k100_roll in range(82, 101):
            size_f = int(random.choice('78'))  # 7 or 8 family members

        m_txt = open('dictio//names_male.txt')
        f_txt = open('dictio//names_female.txt')
        male_names = m_txt.read().split('\n')  # all male names list
        female_names = f_txt.read().split('\n')  # all female names list
        bubu = ''  # exception quick fix

        if size_f == 2:
            if random.randint(1, 100) < 80:  # if family 2 members there is 80 % gender is opposite
                familyChar.append(random.choice(male_names))
                familyChar.append(random.choice(female_names))
            else:
                bubu = 'xxx'  # to prevent error when size_f is 2 and >=80
        if bubu == 'xxx' or size_f != 2:
            for index in range(size_f):
                gender = random.choice('mf')

                if gender == 'm':
                    familyChar.append(random.choice(male_names))
                elif gender == 'f':
                    familyChar.append(random.choice(female_names))

        m_txt.close()
        f_txt.close()

    familyStats = []  # stats of family members [physical, mental, HP, morale]

    for i in familyChar:  # returns stats of family members (semi-randomised)
        physical = random.randint(2, 5)
        mental = random.randint(2, 5)
        HP = physical * 2  # HP is double of physical
        morale = 3  # not used in game
        familyStats.append([physical, mental, HP, morale])
    if len(familyChar) < 1:
        print('FAMILY_CHAR LIST IS EMPTY WHILE GENERATING FAMILY CHARS WITH TRUE CONDITION - 427 line in functions')
        raise ValueError

    return familyChar, familyStats


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

def weather(daytime):
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
                   ('dry', 'dry', 'damp', 'light rain', 'rains'), ('is warm',
                    'is cool', 'is hot', 'is cold', 'is moderately warm'))
        return [random.choice(weather[0]), random.choice(weather[1]),
                random.choice(weather[2]), random.choice(weather[3])]



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











# FOR EXPORT (doesn't belong to simulation)


def letters_correction(a_list):  # an example that removes all newlines from list items
    """    Removes unwanted characters from strings
    example: spam = ['zajebany \njabol', 'akuku\n kurwa']
             print(letters_correction(spam))
             -> ['zajebany jabol', 'akuku kurwa']
    :param a_list: list data type
    :return: corrected list
    """
    a_list_corrected = []

    for item in a_list:
        if '\n' in item:  # for custom changes
            item = ''.join([letter for letter in item if letter != '\n'])  # for custom changes
            a_list_corrected.append(item)
            continue
        a_list_corrected.append(item)
    return a_list_corrected
