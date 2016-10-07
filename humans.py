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
            is_valid_guess = False
            while not is_valid_guess:
                guessed_card = int(input('Which card do you think %s has?\n' % chosen_player))
                if guessed_card == 1:
                    print("Oops! Can't guess a 1! Try again")
                    is_valid_guess = False
                else:
                    break
            if attacked_player.card_num1 == guessed_card:
                attacked_player.is_in_game = False
                print("%s is out of the game!" % attacked_player.name)
            else:
                print('sorry, %s, your guess is wrong' % current_player.name)
                # TODO add ELSE what happens if wrong? nothing i think. think about it
        elif card_played == 2:
            chosen_player = input('Which player do you want to play this card on? options: %s\n'
                                  % ", ".join([player.name for player in list_self_excluded]))
            attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
            print("%s's card is %s" % (attacked_player.name, attacked_player.card_num1))



    def list_of_available_players(self):
        return [player for player in self.players_list if player.is_in_game and not player.is_in_safe_mode]

    def list_of_active_players(self):
        return [player for player in self.players_list if player.is_in_game]

    def identify_player_by_name(self, active_players_list, name):
        return [player for player in active_players_list if player.name == name][0]

    def check_for_last_standing_winner(self, active_players_list):
        active_players = [player for player in active_players_list if player.is_in_game]
        if len(active_players)==1:
            print("%s won the game!" % active_players[0].name)
            return False
        else:
            return True


    # TODO fix this method to decide on a winner from a list with len >1
    def compare_cards(self):
        active_players = self.list_of_active_players()
        sorted_active_players = sorted(active_players, key=lambda x: x.card_num1, reverse=True)
        print("%s's card is the highest!" % sorted_active_players[0].name)
        return sorted_active_players[0]

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
does_game_continue = True
while len(humans.deck) > 0 and does_game_continue:
    for player in humans.players_list:
        player.card_num2 = player.draw_card(humans.deck)
        humans.update_deck(humans.deck)
        # print(player.card_num1,player.card_num2)
        player_move = player.play_card()
        humans.do_card_action(player_move, player)
        player.discarded.insert(0, player_move)
        player.update_hand()
        if not humans.check_for_last_standing_winner(humans.players_list):
            does_game_continue = False
            break
        print(humans.deck)
        if len(humans.deck) == 0:
            break
if len(humans.deck) == 0:
    print("%s won the game!" % humans.compare_cards().name)l
    m
