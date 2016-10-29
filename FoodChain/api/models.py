from django.db import models
import jsonfield


class Turn(models.Model):
    round_id = models.ForeignKey('Round')
    played_by = models.ForeignKey('Player')
    turn_seq = models.PositiveIntegerField()
    had_card = models.ForeignKey('Card')
    drew_card = models.ForeignKey('Card')
    played_card = models.ForeignKey('Card')
    card_after_turn = models.ForeignKey('Card')
    played_against = models.ForeignKey('Player')
    kicked_out_player = models.ForeignKey('Player')
    turn_time = models.DateTimeField()
    deck_before_round = jsonfield.JSONField()
    deck_after_round = jsonfield.JSONField()


class Card(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)


class Round(models.Model):
    ROUND_TYPE = (('MP', 'Multi Player Game'), ('AI', 'Play Against The Computer'),)
    STATUS_ENUM = (('waiting_for_player', 'waiting for player'), ('ended', 'ended'), ('abandoned', 'abandoned'),)

    type = models.CharField(max_length=2, choices=ROUND_TYPE)
    player_count = models.PositiveSmallIntegerField()
    player_list = jsonfield.JSONField()
    status = models.CharField(max_length=50, choices=STATUS_ENUM)
    start_deck = jsonfield.JSONField()
    removed_card = jsonfield.JSONField()
    winner_player = models.ForeignKey('Player')
    turn_list = jsonfield.JSONField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()






