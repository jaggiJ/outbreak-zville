#! python 3
"""
BSD 3-Clause License

Copyright (c) 2018, jaggiJ (jagged93 <AT> gmail <DOT> com), Aleksander Zubert
All rights reserved.

Simulation of zombie attack on family.
"""
import random, datetime, sys, math, time  # standard library


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


def fight(grid, zombies, population, pulped, init_pop, rounds_passed):  # grid_data, current_zombies, current_pop, pulped bodies, starting_population
    """ counts infected tiles, amount of zombies and defenders to fight, makes them fight, adds new infected zones based on human casualties
    # example use: grid_data, zombies, population, pulped, round_count = fight(grid=grid_data, zombies=5, population=1495, pulped=0, init_pop=1500, rounds_passed=26)
    :param grid:
    :param zombies:
    :param population:
    :param pulped:
    :param init_pop:
    :param rounds_passed
    :return: updated grid, new zombies amount, new population amount, new pulped amount, new time
    """

    infected_tiles = []
    # area_scan = [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]  # N, NE, E, SE, S, SW, W, NW
    grid_attacked = []  # list of lists with pair of tuples each
    healthy_tiles = 0
    rounds_count = 1

    # counting healthy, infected tiles and tiles that will be attacked this round
    for y in range(len(grid)):

        for x in range(len(grid[y])):

            if grid[y][x] == '▓':  # healthy tile
                healthy_tiles += 1
            if grid[y][x] == '░':  # the infected tile

                infected_tiles.append((y, x))

                # scan around infected tile for healthy tiles, add coord of first one to grid_attacked if not already present
                # in case of out of range make except to ignore error and keep seeking
                # content of grid_attacked makes contact area to determine fights due for the round

                for ry, rx in [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]:  # rx relative x ry relative y
                    try:
                        if ry >= 0 and rx >= 0 and grid[ry][rx] == '▓' and (ry, rx) not in grid_attacked:  # absolute coord must be 0+ otherwise they are out of grid
                            grid_attacked.append((ry, rx))  # appending tuple of coords of attacked healthy tile
                            break
                    except IndexError:
                        pass
                        #print('One was out of range. Except working OK.')
    print(f'infected tiles = {len(infected_tiles)}, {infected_tiles}')
    print(f'healthy tiles = {healthy_tiles}')
    print(f'healthy tiles attacked = {len(grid_attacked)}, {grid_attacked}')
    print(f'population = {population}')
    print(f'zombies = {zombies}')

    # i want calculate fight taking amount of all zombies involved against all population involved until one side die.
    # A. for round_fight in range(len(amount_of_zombies)
    pop_fighting = round(population / healthy_tiles * len(grid_attacked))
    print(f'zombies attacking = {zombies}')
    print(f'homeowners defending = {pop_fighting}')

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
                roll = random.randint(1, 100)
                #print(f'roll is = {roll}')
                if roll <= 60:
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
                                bitten_to_zombie = rounds_count + 3

                elif roll <= 80:  # human dies, zombie raises

                    # how to find if one who died was bitten before ?
                    # pop_fighting = 2
                    # bitten = 1
                    # i = random.randint(1, pop_fighting:2)
                    # if i <= bitten then bitten -= 1
                    if bitten == 1 and pop_fighting == 1:  # when last defender that died was already bitten
                        bitten = 0
                    elif bitten > 0 and pop_fighting > 1 and random.randint(1, pop_fighting) <= bitten:  # check if dead human was bitten before, to remove amount of infected
                        bitten -= 1

                    print('human dies')
                    pop_fighting -= 1
                    population -= 1
                    pile -= 1  # new zombie will raise
                else:
                    print('zombie pulped')
                    pulped += 1  # added to pulped bodies
                    pile += 1  # zombie will be removed
            elif zombies < 1:
                print('DAMN, IMPOSSIBLE HAPPENED AND ZOMBIES LOST THE FIGHT, TELL DEV TO WRITE NEW CODE TO HANDLE THAT :D')
            else:
                print('=' * 79)
                print(f'every defender killed, fight lasted {rounds_count *5} seconds')
                print('=' * 79)
                break
        rounds_count += 1

        # infected turn zombie
        if rounds_count == bitten_to_zombie:
            pile -= bitten
            print(f'{bitten} infected humans are turning into zombies')
            pop_fighting -= bitten
            population -= bitten
            bitten = 0
            bitten_to_zombie = 0
            # need to remove infected turned from pop_fighting
            # need to calculate if dead human is one that was bitten

        zombies -= pile  # adjusting number of zombies by pulped/raised in round
        pile = 0  # resetting pulped pile

    # updating grid with new infected tiles, each full 4 population removed adds one infected tile
    while len(infected_tiles) < int((init_pop - population) / 4):
        if len(grid_attacked) < 1:  # no more attacked tiles to add
            break
        # add random choice from attacked tiles, remove it and check again, if its empty break
        temp_yx = random.choice(grid_attacked)  # tuple with y, x coord
        grid_data[temp_yx[0]][temp_yx[1]] = '░'
        grid_attacked.remove(temp_yx)
    new_time = rounds_passed + rounds_count

    return grid_data, zombies, population, pulped, new_time


def gen_grid(population):
    """ Generates grid data and number of houses (each house is one grid cell)
    built-in min() function, to find the element which has the minimum distance from the specified number.
    min(myList, key=lambda x:abs(x-myNumber))
    :param population: int(numberOfPopulation)
    :return: list of lists (grid data x number of lists
             with values y), int(numberOfHouses)
    """
    houses = round((population / 4 * (11 / 10 if random.randint(0, 1) == 0 else 9 / 10)))  # based on population and random factor 10%
    # ABC are different algoritms used to calculate grid, one is picked based on how close the algorithm will match to houses
    gridA = int(math.sqrt(houses)) * int(math.sqrt(houses))
    gridB = int(math.sqrt(houses)) * (int(math.sqrt(houses)) + 1)
    gridC = (int(math.sqrt(houses)) + 1) * (int(math.sqrt(houses)) + 1)
    #print(gridA, gridB, gridC)
    #print(houses)

    win_algorithm = min([gridA, gridB, gridC], key=lambda x: abs(x-houses))
    #print(win_algorithm)
    x_grid = 0
    y_grid = 0
    if gridA == win_algorithm:
        x_grid = int(math.sqrt(houses))
        y_grid = int(math.sqrt(houses))
    elif gridB == win_algorithm:
        x_grid = int(math.sqrt(houses))
        y_grid = int(math.sqrt(houses)) + 1
    elif gridC == win_algorithm:
        x_grid = int(math.sqrt(houses)) + 1
        y_grid = int(math.sqrt(houses)) + 1

    return [['▓'] * y_grid for item in range(x_grid)], x_grid * y_grid


def intro_game():  # Runs when user choose Intro Game
    """ Text intro for game take and returns nothing
    :return: None
    """

    story = """ A STORY. How shit hit the fun?
    An isolated village. 
    Great place for testing stuff on human subjects, isn't it?
    Somewhere THEY have been attached to the idea. 
    Concerns about value of human life, dignity and work ethics since long had 
    their own spin-off. 
    They simply admit such an experiment because they CAN get away with it.
    Let's call it ... 
    LACK OF TRANSPARENCY. 
    A viral sample has been released. 
    Something bad, creepy stuff take my word. 
    Somewhere in the village, patient zero has been exposed to a sample. 
    ================================================================================
    NOW. 

    XX:XX
    village_name, pop_size
    """

    for item in story:
        print(item, end='', sep='')
        if item in '.?!':
            time.sleep(1)
            continue
        time.sleep(0.05)


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

    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return [village_name.title(), pop_size, time]


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
    :param  True or False - random or custom genration
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

    return familyChar, familyStats


def fight(grid):

    infected_tiles = 0
    infected_tiles_contact = []  # list of tuples with x,y coord
    # area_scan = [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]  # N, NE, E, SE, S, SW, W, NW
    grid_attacked = []  # list of lists with pair of tuples each

    for y in range(len(grid)):

        for x in range(len(grid[y])):

            if grid[y][x] == '░':  # the infected tile
                infected_tiles += 1
                print(f'I am infected ={(y,x)}')
                # scan around infected tile for healthy tiles, add coord of first one to grid_attacked if not already present
                # in case of out of range make except to ignore error and keep seeking
                # content of grid_attacked makes contact area to determine fights due for the round

                for ry, rx in [(y-1, x), (y-1,x+1), (y,x+1), (y+1,x+1), (y+1,x), (y+1,x-1), (y,x-1), (y-1,x-1) ]:  # rx relative x ry relative y
                    #try:
                    # how to find N of the infected tile grid[y][x] ?
                    # i must grid[y-1][x] # how to do it ? # I cant make 8 elif with appropriate grid indices or make iterable list that somehow pick them up
                    if ry >= 0 and rx >= 0 and grid[ry][rx] == '▓' and (ry, rx) not in grid_attacked:  # absolute coord must be 0+ otherwise they are out of grid
                        grid_attacked.append((ry, rx))  # appending tuple of coords of attacked healthy tile
                        break
                    #except IndexError:
                    #    print('One was out of range. Except working OK.')

    print(f'amount of infected tiles = {infected_tiles}')
    print(f'tiles attacked in the round = {len(grid_attacked)}')
    print(f'we are attacked ={grid_attacked}')
    #print()




def speed_round(kmh, delay, round_sec):
    """
    Calculates speed in meters per game round
    # How many meters zombies move in 5 sec game round at speed 1kmh ?
    # How many meters per second is 1 kilometer per hour = 1000 in 3600 =  10m in 36s = 10/36 in 1s = 10/36*5 in 1 round = 1.38m per round(5sec)
    # 1kmh = 1000m in 3600 seconds = 1000 in 720 game rounds = 1000/720m in 1 round = 1.38m per round(5sec)
    # answer is = 1.38m/round, so if zombies have speed 3.22kmh their game speed is 3.22 * 1.38mpr = 4.44 meters per 5 second round
    :param kmh: speed in kilometers per hour
    :param delay: delay caused by some stuff eg besieging houses, kmh=1/delay
    :param round: length of game round/iteration per second
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
