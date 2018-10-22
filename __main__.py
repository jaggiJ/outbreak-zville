#! python3
"""
Simulation of zombie attack on family.
User input is names of family members as well as number of zombies to pit them against.
"""

# importing functions used in program
import random  # Used for random k6rolls to powerAdvantage resolution
import sys  # Used to quit game on user enter input at choosing zombies number
import time  # Used for delay between zombie hits


savedFamily = []  # List of family characters from which each game run will resets family members alive

while True:  # MAIN LOOP

    """
    FAMILY GENERATION. 
    Lists of family names and corresponding lists of their randomised stats are created.
    List of family is retained in tuple from which each game iteration is stat list generated
    as default (no names choosing is necessary each game).
    """

    if not savedFamily:  # returns names of family from user input
        while True:
            name = input('Type family member name or enter:  ')
            if name:
                savedFamily.append(name)
                name = False
            elif not name and savedFamily:  # Second condition prevents quiting loop in case that user didnt type any family name at all. Error prevention.
                savedFamily = tuple(savedFamily)
                break
    familyChar = list(savedFamily)  # names of family members
    familyStats = []  # stats of family members [physical, mental, HP, morale]

    for i in familyChar:  # returns stats of family members (semi-randomised)
        physical = random.randint(2, 5)
        mental = random.randint(2, 5)
        HP = physical*2  # HP is double of physical
        morale = 3  # not used in game
        familyStats.append([physical, mental, HP, morale])

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

        print('\nStart of round: ', roundNumber, '\n')  # Number of round
        print(zombieChar, '\n', familyChar,
              '\n')  # Zombies and Family characters going to fight that round

        """
        FIGHTING ROUND LOOP
        """
        for strZombie in zombieChar:  # All zombies attack chosen family member in sequence. That is one round of fight.

            time.sleep(0.2)  # Time delay between each zombie hit

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
            print(casualties, 'has been killed in this round')

            for dead in casualties:  # iterating through list of strings that contains current round casualties
                if dead in zombieChar:
                    del zombieStats[zombieChar.index(dead)]  # remove dead zombie statistics
                    zombieChar.remove(dead)  # remove dead zombie from string list

        roundNumber += 1  # rounds counter

    """ 
    END GAME RESOLUTION.    
    Prints how long fight lasted and all survivors from either team.
    """

    print('\nThe fight lasted ', roundNumber * 3, 'seconds\n')
    print('Survivors are: ')
    for x in familyChar:
        print(x)
    for x in zombieChar:
        print(x)
