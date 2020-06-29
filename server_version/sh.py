from __future__ import print_function, unicode_literals
from PyInquirer import prompt
import random
import os
import shutil
import utils
import je

os.system('cls' if os.name == 'nt' else 'clear')
rows = shutil.get_terminal_size((100, 25))[1]
columns = shutil.get_terminal_size((100, 25))[0]

players = []

def printCentered(str):
    print(' '*int((columns - len(str)) / 2) + str)

# def getPlayers():
#     questions = [
#         {
#             'type': 'input',
#             'name': 'playerName',
#             'message': 'Inpur a new player name (input \'quit\' when done)',
#         }
#     ]
# 
#     new_players = []
# 
#     new_player = prompt(questions)
#     while new_player['playerName'] != 'quit':
#         if new_player['playerName'] not in new_players and len(new_player['playerName']) != 0:
#             new_players.append(new_player['playerName'])
#         elif new_player['playerName'] in new_players:
#             print('%s is already in the game. Please choose a new one.' % new_player['playerName'])
#         elif len(new_player['playerName']) == 0:
#             print('Please enter a name or quit')
#         new_player = prompt(questions)

#     players = new_players

def askIfNeedInstructions():
    questions = [
        {
            'type': 'confirm',
            'message': 'Do you all know how to play the game already?',
            'name': 'known',
            'default': True,
        }
    ]

    knowRules = prompt(questions)

    if knowRules['known'] is True:
        print('\n')
        printCentered('All right, then get ready to play!')
    else:
        print('\n')
        printCentered('Sucks, \'cause I don\'t want to write them all down right now!')

def printDetails():
    numLines = 28
    deck = je.getValue('deck')

    os.system('cls' if os.name == 'nt' else 'clear')

    deck_display = utils.tcolors.blue + 'deck: [ '
    for i in deck:
        deck_display += '# '
    for i in range(je.getValue('num_total_cards') - len(deck)):
        deck_display += '_ '
    deck_display += ']'

    discard = je.getValue('discard')

    discard_display = utils.tcolors.green + 'discard: [ '
    for i in discard:
        discard_display += '# '
    for i in range(je.getValue('num_total_cards') - len(discard)):
        discard_display += '_ '
    discard_display += ']'

    firstLine = deck_display + ' '*int(int(columns) / 2 - len(deck_display)) + discard_display
    print(firstLine)

    printFascists()

    printFailedElections()

    printLiberals()
        
def printFascists():
    played_fascists = je.getValue('played_fascists')
    fascist_string = ("""""")
    card_height = utils.cardHeight
    card_width = utils.cardWidth
    board_size = je.getBoardSize()
    board = je.getValue('fascist_cards')[board_size]
    board_size = len(board)
    card_separator = ' -> '
    cards_to_play = []

    print('\n' + utils.tcolors.red)
    printCentered('FASCISTS')

    for c in range(played_fascists):
        cards_to_play.append(utils.getCard('fascist'))
    for n in range(played_fascists, board_size):
        cards_to_play.append(utils.getCard(board[n]))

    for i in range(card_height):
        total_line = ' '*int((columns - (board_size * card_width) - (len(card_separator) * (board_size - 1))) / 2)
        current_line_card_separator = card_separator if i == int(card_height / 2) else ' '*len(card_separator)
        for c in cards_to_play:
            total_line += c.splitlines()[i]
            total_line += current_line_card_separator if c != utils.getCard('fascist_end') else ''

        fascist_string += total_line + '\n'

    print(fascist_string)


def printFailedElections():
    fail_dots = je.getValue('allowable_failures')
    num_failed = je.getValue('failed_elections')

    print(utils.tcolors.yellow)
    printCentered('FAILURE TRACKER')

    fs = 'Failures: '
    for i in range(fail_dots):
        if i == num_failed:
            fs += '● '
        else:
            fs += '○ '
        if i != fail_dots - 1:
            fs += '-▶ '

    fs += ' A card will be overturned.'
    printCentered(fs)

def printLiberals():
    played_liberals = je.getValue('played_liberals')
    liberal_string = ("""""")
    card_height = utils.cardHeight
    card_width = utils.cardWidth
    board_size = je.getValue('liberal_board_length')
    card_separator = ' -> '
    cards_to_play = []

    print('\n' + utils.tcolors.blue)
    printCentered('LIBERALS')

    for c in range(played_liberals):
        cards_to_play.append(utils.getCard('liberal'))
    for n in range(played_liberals, board_size - 1):
        cards_to_play.append(utils.getCard('blank'))
    cards_to_play.append(utils.getCard('liberal_end'))

    for i in range(card_height):
        total_line = ' '*int((columns - (board_size * card_width) - (len(card_separator) * (board_size - 1))) / 2)
        current_line_card_separator = card_separator if i == int(card_height / 2) else ' '*len(card_separator)
        for c in cards_to_play:
            total_line += c.splitlines()[i]
            total_line += current_line_card_separator if c != utils.getCard('liberal_end') else ''

        liberal_string += total_line + '\n'

    print(liberal_string)

def nominateChancellor(is_special_election):

    chancellor_chooser = [
        {
            'type': 'input',
            'name': 'chancellor',
            'message': 'Type in the name of the chancellor that you chose: ',
        }
    ]

    new_chancellor = prompt(chancellor_chooser)['chancellor']

    while new_chancellor not in players or new_chancellor == je.getValue('last_chancellor') or new_chancellor == je.getValue('last_president') or new_chancellor == je.getValue('current_president'):
        if new_chancellor not in players:
            print("%s is not a player in the current game. Choose a new one. " % new_chancellor)
        else:
            if is_special_election is True:
                break
            print("%s is not eligible to be chancellor. Choose a new one. " % new_chancellor)
        new_chancellor = prompt(chancellor_chooser)['chancellor']

    if_passed = [
        {
            'type': 'confirm',
            'message': 'Let the rest of the players vote now on if they want this player as their chancellor. Did the vote pass?',
            'name': 'passed',
            'default': True,
        }
    ]

    passed = prompt(if_passed)['passed']

    if passed is True:
        je.insert('current_chancellor', new_chancellor)

        if je.getValue('failed_elections') >= 3:
            if je.getValue('players')[new_chancellor]['personal_loyalty'] == 'hitler':
                printCentered('Unfortunately, you just fell right into Hitler\'s trap. You elected Hitler as chancellor')
                input('Click any key when you are ready to quit.')
                quit(' '*int((columns - len('THANKS FOR PLAYING!')) / 2) + 'THANKS FOR PLAYING!')
            else:
                input('%s is NOT hitler! Be careful, though, they could still be a fascist. Press enter to continue...')
        
        return True
    else:
        je.insert('failed_elections', je.getValue('failed_elections') + 1)
        return False

players = je.getValue('players')

nominateChancellor(False)
printDetails()
# print(int((rows - len(str)) / 2))

