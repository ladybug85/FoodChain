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

    def update_deck(self):
        self.deck.pop(0)

    def do_card_action(self, card_played, current_player):
        list_self_excluded = [player for player in self.list_of_available_players() if player is not current_player]
        if len(list_self_excluded) == 0 and card_played in (1, 2, 3, 6):
            return None
        else:
            if card_played == 1:
                chosen_player = input('Which player do you want to play this card on? options: \n%s\n'
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
                chosen_player = input('Which player do you want to play this card on? options: \n%s\n'
                                  % ", ".join([player.name for player in list_self_excluded]))
                attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
                print("%s's card is %s" % (attacked_player.name, attacked_player.card_num1))
                self.update_deck()
            elif card_played == 3:
                chosen_player = input('Which player do you want to play this card on? options: \n%s\n'
                                  % ", ".join([player.name for player in list_self_excluded]))
                attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
                winner_of_comparison = self.compare_cards([current_player, attacked_player])
                if winner_of_comparison == current_player:
                    attacked_player.is_in_game = False
                else:
                    current_player.is_in_game = False
            elif card_played == 4:
                current_player.is_in_safe_mode = True
                print('%s is now in safe mode' % current_player.name)
            elif card_played == 5:
                list_self_excluded.append(current_player)
                chosen_player = input('Which player do you want to play this card on? options: \n%s\n'
                                      % ", ".join([player.name for player in list_self_excluded]))
                attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
                if attacked_player == current_player:
                    if current_player.card_num1 == card_played and current_player.card_num2 != 8:
                        print('%s forced discarded a %s' % (current_player.name, current_player.card_num2))
                        current_player.discarded.append(current_player.card_num2)
                        current_player.card_num2 = current_player.draw_card(self.deck)
                        print('%s new card is %s' % (current_player.name, current_player.card_num2))
                        self.update_deck()
                    elif current_player.card_num2 == card_played and current_player.card_num1 != 8:
                        print('%s forced discarded a %s' % (current_player.name, current_player.card_num1))
                        current_player.discarded.append(current_player.card_num1)
                        current_player.card_num1 = current_player.draw_card(self.deck)
                        print('%s new card is %s' % (current_player.name, current_player.card_num1))
                        self.update_deck()
                    else:
                        print('Silly you! You have just committed suicide!')
                        current_player.is_in_game = False
                else:
                    if attacked_player.card_num1 == 8:
                        print('%s was forced to discard an 8! Therefor, %s is out of the game!' %
                              (attacked_player.name, attacked_player.name))
                        attacked_player.is_in_game = False
                    else:
                        attacked_player.discarded.append(attacked_player.card_num1)
                        attacked_player.card_num1 = attacked_player.draw_card(self.deck)
                        self.update_deck()
            elif card_played == 6:
                chosen_player = input('Which player do you want to play this card on? options: \n%s\n'
                                      % ", ".join([player.name for player in list_self_excluded]))
                attacked_player = self.identify_player_by_name(list_self_excluded, chosen_player)
                current_get_this_card = attacked_player.card_num1
                if card_played == current_player.card_num1:
                    attacked_player.card_num1 = current_player.card_num2
                    current_player.card_num2 = current_get_this_card
                else:
                    attacked_player.card_num1 = current_player.card_num1
                    current_player.card_num1 = current_get_this_card

    def list_of_available_players(self):
        for player in self.players_list:
            if len(player.discarded) != 0:
                if player.discarded[0] == 4:
                    player.is_in_safe_mode = True
                else:
                    player.is_in_safe_mode = False
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

    def compare_cards(self, players_to_compare):
        sorted_active_players = sorted(players_to_compare, key=lambda x: x.card_num1, reverse=True)
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
        humans.update_deck()
        print(humans.deck)
# print(humans.list_of_available_players())
does_game_continue = True
while len(humans.deck) > 0 and does_game_continue:
    for player in humans.players_list:
        player.card_num2 = player.draw_card(humans.deck)
        humans.update_deck()
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
    print("%s won the game!" % humans.compare_cards(humans.list_of_active_players()).name)

