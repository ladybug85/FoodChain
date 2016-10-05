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

    def do_card_action(self, card_played, current_player):
        list_self_excluded = [player for player in self.list_of_available_players() if player is not current_player]
        if card_played == 1:
            chosen_player = input('Which player do you want to play this card on? options: %s\n'
                                    % ", ".join([player.name for player in list_self_excluded]))
            attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
            guessed_card = int(input('Which card do you think %s has?\n' % chosen_player))
            if attacked_player.card_num1 == guessed_card:
                attacked_player.is_in_game = False
                print("%s is out of the game!" % attacked_player.name)
                # TODO add ELSE what happens if wrong? nothing i think. think about it 



    def list_of_available_players(self):
        return [player for player in self.players_list if player.is_in_game and not player.is_in_safe_mode]

    def identify_player_by_name(self, active_players_list, name):
        return [player for player in active_players_list if player.name == name][0]

    def check_for_winner(self, active_players_list):
        active_players = [player for player in active_players_list if player.is_in_game]
        if len(active_players)==1:
            print("%s won the game!" % active_players[0].name)
            #TODO need to break our of the loop once a winner is declared



    # def name_players(self):
    #     for player in self.players_list:


    def announce_winner(self, name1, card1, name2, card2):
        if card1>card2:
            print('%s  won!' % name1)
        else:
            print('%s  won!' % name2)

class Player(object):
    def __init__(self):
        self.name = None
        self.card_num1 = None
        self.card_num2 = None
        self.discarded = []
        self.is_in_safe_mode = False
        self.is_in_game = True

    def draw_card(self, deck):
        return deck[0]

    def play_card(self):
        is_valid = False
        while not is_valid:
            print('%s, Which card do you want to play? you have: %s and %s' % (self.name, self.card_num1, self.card_num2))
            player_move = int(input('Please pick one\n'))
            is_valid = self.is_valid_move(player_move)
        return player_move

    def is_valid_move(self, player_move):
        if player_move == 8:
            # TODO Once have names of cards change messages to include card names
            print("Oops! Can't discard the human card (8)! Try again...")
            return False
        elif (self.card_num1 == 7 and self.card_num2 in (5, 6) and player_move == self.card_num2) or \
             (self.card_num2 == 7 and self.card_num1 in (5, 6) and player_move == self.card_num1):
            # TODO Once have names of cards change messages to include card names
            print("Oops! Can't discard 5 or 6 when you have a 7!")
            return False
        else:
            return True

    def update_hand(self):
        if self.discarded[0] == self.card_num1:
            self.card_num1 = self.card_num2
            self.card_num2 = None
        else:
            self.card_num2 = None


# class PlayerList(list):
#     def __init__(self):
        
# class Card(object):
#     def __init__(self, name, number):
#         self.name = name
#         self.number = number

# class Move(object):
#     def __init__(self):

deck1 = [1, 1, 1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 8]
player1 = Player()
player2 = Player()
humans = Game(deck=deck1, players_list=[player1, player2])
humans.prepare_deck(deck1)

print(humans.deck)

if len(humans.deck) == 15:
    for player in humans.players_list:
        player.name = input('please enter your name\n')
        player.card_num1 = player.draw_card(humans.deck)
        humans.update_deck(humans.deck)
        print(humans.deck)
# print(humans.list_of_available_players())
while len(humans.deck) > 0:
    for player in humans.players_list:
        player.card_num2 = player.draw_card(humans.deck)
        humans.update_deck(humans.deck)
        # print(player.card_num1,player.card_num2)
        player_move = player.play_card()
        humans.do_card_action(player_move, player)
        player.discarded.insert(0, player_move)
        player.update_hand()
        humans.check_for_winner(humans.players_list)
        print(humans.deck)
        if len(humans.deck) == 0:
            break
humans.announce_winner(player1.name, player1.card_num1, player2.name, player2.card_num1)