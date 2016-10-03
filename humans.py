from random import Random
import re


class Game(object):
    def __init__(self, deck, players_list):
        self.deck = deck
        self.players_list = players_list

    def prepare_deck(self, deck):
        game = Random()
        card_out = game.randint(0, len(deck))
        game.shuffle(deck)
        deck.pop(card_out)
        return deck

    def update_deck(self, deck):
        deck.pop(0)
        return deck

    # def name_players(self):
    #     for player in self.players_list:


    def announce_winner(self, card1, card2):
        if card1>card2:
            print('Player 1 won!')
        else:
            print('Player 2 won!')

class Player(object):
    def __init__(self):
        self.name = None
        self.card_num1 = None
        self.card_num2 = None
        self.discarded = []

    def draw_card(self, deck):
        return deck[0]

    def play_card(self, card1, card2):
        is_valid = False
        while not is_valid:
            print('Which card do you want to play? you have: %s and %s' % (card1, card2))
            player_move = int(input('Please pick one\n'))
            is_valid = self.is_valid_move(player_move, card1, card2)
        return player_move

    def is_valid_move(self, player_move, card1, card2):
        if player_move == 8:
            # TODO Once have names of cards change messages to include card names
            print("Oops! Can't discard the human card (8)! Try again...")
            return False
        elif (card1 == 7 and card2 in (5, 6) and player_move == card2) or \
             (card2 == 7 and card1 in (5, 6) and player_move == card1):
            # TODO Once have names of cards change messages to include card names
            print("Oops! Can't discard 5 or 6 when you have a 7!")
            return False
        else:
            return True

    def update_hand(self, card1, card2, discarded):
        if discarded[0] == card1:
            self.card_num1 = card2
            self.card_num2 = None
        else:
            self.card_num1 = card1
            self.card_num2 = None


# class PlayerList(list):
#     def __init__(self):
        
# class Card(object):
#     def __init__(self, name, number):
#         self.name = name
#         self.number = number

# class Move(object):
#     def __init__(self):

deck1 = ['1', '1', '1', '1', '1', '2', '2', '3', '3', '4', '4', '5', '5', '6', '7', '8']
player1 = Player()
player2 = Player()
humans = Game(deck=deck1, players_list=[player1, player2])
humans.prepare_deck(deck1)

print (humans.deck)

if len(humans.deck) == 15:
    for player in humans.players_list:
        player.card_num1 = player.draw_card(humans.deck)
        humans.update_deck(humans.deck)
        print(humans.deck)
while len(humans.deck) > 0:
    for player in humans.players_list:
        player.card_num2=player.draw_card(humans.deck)
        humans.update_deck(humans.deck)
        # print(player.card_num1,player.card_num2)
        player.discarded.insert(0, (player.play_card(player.card_num1, player.card_num2)))
        player.update_hand(player.card_num1, player.card_num2, player.discarded)
        print(humans.deck)
        if len(humans.deck) == 0:
            break
humans.announce_winner(player1.card_num1, player2.card_num1)
