from otree.api import *


doc = """
A group of two players. 
One players assigned a certain endowment. 
    They decide how much to send to second player.
Second players receive the tripled amount.
    They decide how much to send back to the first player.
Results:
    Player 1: Endowment - sent amount + got back amount
    Player 2: Tripled amount -sent back amount
"""


class C(BaseConstants):
    NAME_IN_URL = 'trustgame'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ENDOWMENT = cu(10)
    MULTIPLE_FACTOR = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    sent_amount = models.CurrencyField(
        min = 0,
        max = C.ENDOWMENT,
        label="How much do you want to send to other player?",
        doc="""Amount of money sent by player 1"""
    )

    sent_back_amount = models.CurrencyField(
        label="How much do you want to send back to other player?",
        doc="""Amount of money sent back by player 2"""
    )


class Player(BasePlayer):
    pass

#FUCNTION------------------------------------------------

def sent_back_amount_choices(group: Group):
    return currency_range(0, group.sent_amount * C.MULTIPLE_FACTOR, 1)

def set_payoffs(group: Group):
    print("Run after all players arrive function")
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)

    print("Start to get payoff")
    p1.payoff = C.ENDOWMENT - group.sent_amount + group.sent_back_amount
    p2.payoff = group.sent_amount * C.MULTIPLE_FACTOR - group.sent_back_amount

    print("Finish after all players arrive function")


# PAGES-------------------------------------------------
class SentPage(Page):
    form_model = "group"
    form_fields = ["sent_amount"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 1


class WaitForP1(WaitPage):
    pass

class SendBack(Page):
    form_model = "group"
    form_fields = ["sent_back_amount"]

    @staticmethod
    def is_displayed(player: Player):
        return player.id_in_group == 2

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group

        return dict(tripled_amount = group.sent_amount * C.MULTIPLE_FACTOR)

class WaitForP2(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        set_payoffs(group)

class Results(Page):
    pass



page_sequence = [SentPage, WaitForP1, SendBack, WaitForP2, Results]
