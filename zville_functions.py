#! python 3
import random, time


def into_game():  # Runs when user choose option for Intro Game
    story = """ A STORY. How shit hit the fun?
    An isolated village. 
    Great place for testing stuff on human subjects, isn't it?
    Somewhere THEY have been attached to the idea. 
    Concerns about value of human life, dignity and work ethics since long had 
    their own spin-off. 
    They simply admit such an experiment because THEY c_a_n get away with it.
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

    for item in STORY:
        print(item, end='', sep='')
        if item in '.?!':
            time.sleep(1)
            continue
        time.sleep(0.05)


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


def village_gen(custom):
    """ GENERATES RANDOM VILLAGE OR USER CUSTOMISED
    :takes True|False (whether user wants random or custom generated values)
    :returns village_name, pop_size, time
    """
    if not custom:
        village_name = random.choice(VILLAGES)
        pop_size = random.randint(100, 2500)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    elif custom:
        pass       # customised choices for later

    return village_name, pop_size, time


def family_gen(custom):
    """ Generates random family or user defined
    :param custom: True or False
    :return: list of family names
    """
    if custom:  # user defined family names

        while True:
            name = input('Type family member name or enter:  ')
            if name:
                savedFamily.append(name)
                name = False
            elif not name and savedFamily:  # Second condition prevents quiting loop in case that user didnt type any family name at all. Error prevention.
                savedFamily = tuple(savedFamily)
                break
        familyChar = list(savedFamily)  # names of family members