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
from zville_functions import intro_game, user_menu_choice, village_gen,\
    family_gen



savedFamily = []  # List of family characters from which each game run will resets family members alive
sim_speed = 1  # ilosc sekund na runde

while True:  # MAIN LOOP

    while True:  # Handles user menu choices before game starts
        main_choice = user_menu_choice()  # Main game menu returns integer

        if main_choice == 0:  # Intro game
            intro_game()  # Intro story
            random_family = True  # not implemented, change to True when done
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

        elif main_choice == 2:  # Start Designed Sim
            print('You are about to start New Simulation with family or village'
                  'designed by user.')
            if input('(y)es or (n)o ?').lower()[0] == 'n':
                continue
            print('Do you want family that was (d)esigned or (r)andom family?')
            TODO

            break

        elif main_choice == 3:  # Design Village
            random_village = False
            village = village_gen(random_village)
            continue

        elif main_choice == 6:  # Exit Sim
            sys.exit()

    """
    # ADVERSARIES GENERATION. Their numbers and stats are generated each simulation.
    """

    while True:  # Loop iterates until input is between 1-20
        adversaryNumber = (input('\nType number of zombies ~max_20~ '
                                 'or (Enter) to quit simulation  : '))
        if not adversaryNumber:
            sys.exit()
        elif adversaryNumber in [str(iNT) for iNT in range(1, 21)]:
            adversaryNumber = int(adversaryNumber)
            break

    # lists of zombie characters and zombie stats of those characters
    zombieChar = ['zombie' + str(i + 1) for i in range(adversaryNumber)]
    zombieStats = []  # stats of all zombies in game instance: physical mental health morale

    for i in range(len(zombieChar)):  # appends stats for all number of zombies user defined
        zombieStats.append([3, 2, 6, 3])

    # list of strings with names of all characters in game

    roundNumber = 1  # starting round counter value

    """
    COMBAT LOOP.    
    Spans all combat rounds. 
    """

    while familyChar != [] and zombieChar != []:  # Fighting loop continues until one of teams is defeated

        time.sleep(0.2)  # Time delay between each round.
        casualties = []  # Append here casualties from below for loop as they happen.

        print('='*78, '\nStart of round: ', roundNumber, '\n' + '='*78)  # Number of round
        print(zombieChar, '\n', familyChar, '\n' + '='*78)  # Zombies and Family characters going to fight that round

        """
        FIGHTING ROUND LOOP
        """
        for strZombie in zombieChar:  # All zombies attack chosen family member in sequence. That is one round of fight.

            time.sleep(sim_speed)  # Time delay between each zombie hit

            # Establishing who attacks who in this round:
            currentZombieStats = zombieStats[zombieChar.index(strZombie)]  # current zombie stats based on index number of the zombie name currently iterated

            # now stats of random family member
            # found right string in family list (step1)
            if familyChar:  # Checks if there is someone left alive from family.
                currentRandomFamilyName = familyChar[random.randint
                                                     (0, len(familyChar) - 1)]
            else:  # No living family members
                break

            # step 2 assigning value as list found by index of step1 string
            currentRandomFamilyStats = familyStats[familyChar.index
                                                   (currentRandomFamilyName)]
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
                    del familyStats[familyChar.index(currentRandomFamilyName)]  # remove dead family from stats list
                    familyChar.remove(currentRandomFamilyName)  # removing dead family from string list
                    casualties.append(currentRandomFamilyName)
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
                    casualties.append(strZombie)  # Appends dead zombie into list of casualties.
                else:  # Zombie hit but survived
                    # Print HP left if zombie survived
                    print(' (HP left=', currentZombieStats[2], ').', sep='')

            else:  # Nobody has power advantage.
                print(' misses.')  # Counts as miss which is printed out.

        """
        MANIUPULATING IN CASUALTIES WARNING
        Family members cannot be removed at end round since they must be removed immediately
        to prevent next zombies that still not attacked in the round from attacking dead member.
        Adds next round to counter. If dead zombies are removed immediately it will screw sequence
        of zombie attacks for given round. They have to be removed at end of round.
        """

        if casualties:  # Prints round casualties and removes zombies fallen in that round
            print('='*78, '\n', casualties, 'has been killed in this round')

            for dead in casualties:  # iterating through list of strings that contains current round casualties
                if dead in zombieChar:
                    del zombieStats[zombieChar.index(dead)]  # remove dead zombie statistics
                    zombieChar.remove(dead)  # remove dead zombie from string list

        roundNumber += 1  # rounds counter

    """ 
    END GAME RESOLUTION.    
    Prints how long fight lasted and all survivors from either team.
    """

    print('='*78, '\nThe fight lasted ', roundNumber * 3, 'seconds\n'+'='*78)
    print('Survivors are: ')
    for x in familyChar:
        print('', x)
    for x in zombieChar:
        print('', x)
    print('=' * 78, end='')
