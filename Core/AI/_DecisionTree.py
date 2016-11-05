from Core import Constant
import copy

__author__ = 'Evan'


class _Node:

    _pass_node = None
    _fail_node = None
    _pass_action_list = None
    _fail_action_list = None
    _enter_action_list = None
    _check = Constant.Check.Empty

    def __init__(self, pass_node, fail_node, check):
        self.pass_node = pass_node
        self.fail_node = fail_node
        self.check = check

        self.pass_action_list = []
        self.fail_action_list = []
        self.enter_action_list = []

        return

    def process(self, player, possible_cards, trick_pile):
        return

    def _process_pass_node(self, player, possible_cards, trick_pile):
        for action in self.pass_action_list:
            xrange(0, 1)
        return self.pass_node.process(player, possible_cards, trick_pile)

    def _process_fail_node(self, player, possible_cards, trick_pile):
        for action in self.fail_action_list:
            xrange(0, 1)
        return self.fail_node.process(player, possible_cards, trick_pile)

    def set_pass_node(self, pass_node):
        self._pass_node = pass_node
    def get_pass_node(self):
        return self._pass_node

    def set_fail_node(self, fail_node):
        self._fail_node = fail_node
    def get_fail_node(self):
        return self._fail_node

    def set_check(self, check):
        self._check = check
    def get_check(self):
        return self._check

    def set_pass_action_list(self, pass_action_list):
        self._pass_action_list = copy.deepcopy(pass_action_list)
    def get_pass_action_list(self):
        return copy.deepcopy(self._pass_action_list)

    def set_fail_action_list(self, fail_action_list):
        self._fail_action_list = copy.deepcopy(fail_action_list)
    def get_fail_action_list(self):
        return copy.deepcopy(self._fail_action_list)

    def set_enter_action_list(self, enter_action_list):
        self._enter_action_list = copy.deepcopy(enter_action_list)
    def get_enter_action_list(self):
        return copy.deepcopy(self._enter_action_list)

    pass_node = property(get_pass_node, set_fail_node)
    fail_node = property(get_fail_node, set_fail_node)
    check = property(get_check, set_check)
    pass_action_list = property(get_pass_action_list, set_pass_action_list)
    fail_action_list = property(get_fail_action_list, set_fail_action_list)
    enter_action_list = property(get_enter_action_list, set_enter_action_list)


class ValueCheckNode(_Node):

    _comparison_value = 0
    _comparison_type = Constant.ComparisonType.Empty

    def __init__(self, comparison_value, comparison_type, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.comparison_value = comparison_value
        self.comparison_type = comparison_type
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []
        for card in possible_cards:
            if self.comparison_type == Constant.ComparisonType.Equal:
                if card.value == self.comparison_type:
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.GreaterThan:
                if card.value > self.comparison_type:
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.GreaterThanOrEqual:
                if card.value >= self.comparison_type:
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.LessThan:
                if card.value < self.comparison_type:
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.LessThanOrEqual:
                if card.value <= self.comparison_type:
                    new_card_list.append(card)

        if len(new_card_list) is 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def set_comparison_value(self, comparison_value):
        self._comparison_value = comparison_value
    def get_comparison_value(self):
        return self._comparison_value

    def set_comparison_type(self, comparison_type):
        self._comparison_type = comparison_type
    def get_comparison_type(self):
        return self._comparison_type

    comparison_value = property(get_comparison_value, set_comparison_value)
    comparison_type = property(get_comparison_type, set_comparison_type)


class SuitCheckNode(_Node):

    _suit = None

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                new_card_list.append(card)

        if len(new_card_list) is 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def set_suit(self, suit):
        self._suit = suit
    def get_suit(self):
        return self._suit

    suit = property(get_suit, set_suit)


class CardCheckNode(_Node):

    _suit = Constant.Suit.Empty
    _value = Constant.Value.Empty

    def __init__(self, suit, value, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        self.value = value
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                if card.value == self.value:
                    new_card_list.append(card)

        if len(new_card_list) is 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def set_suit(self, suit):
        self._suit = suit
    def get_suit(self):
        return self._suit

    def set_value(self, value):
        self._value = value
    def get_value(self):
        return self._value

    suit = property(get_suit, set_suit)
    value = property(get_value, set_value)


class NumberInSuitCheckNode(_Node):

    _suit = None
    _comparison = 0

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                new_card_list.append(card)

        if len(new_card_list) <= self.comparison:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def set_suit(self, suit):
        self._suit = suit
    def get_suit(self):
        return self._suit

    def set_comparison(self, comparison):
        self._comparison = comparison
    def get_comparison(self):
        return self._comparison

    suit = property(get_suit, set_suit)
    comparison = property(get_comparison, set_comparison)


class SelectHighestValueLeaf:
    def __init__(self):
        return

    def process(self, player, possible_cards, trick_pile):

        highest_card = None

        for card in possible_cards:
            if highest_card is None:
                highest_card = card
            elif card.value > highest_card.value:
                highest_card = card

        return highest_card


class SelectLowestValueLeaf:
    def __init__(self):
        return

    def process(self, player, possible_cards, trick_pile):

        lowest_card = None

        for card in possible_cards:
            if lowest_card is None:
                lowest_card = card
            elif card.value < lowest_card.value:
                lowest_card = card

        return lowest_card


class SelectCardLeaf:
    def __init__(self):
        return
