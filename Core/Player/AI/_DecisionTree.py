from Core import Constant
import copy

__author__ = 'Evan'


class _Node(object):
    _pass_node = 0
    _fail_node = 0
    _check = 0

    _pass_action_list = []
    _fail_action_list = []
    _enter_action_list = []

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
        if self._pass_node is not None:
            for action in self.pass_action_list:
                action.process(player, possible_cards, trick_pile)
            return self._pass_node.process(player, possible_cards, trick_pile)
        else:
            return None

    def _process_fail_node(self, player, possible_cards, trick_pile):
        if self._fail_node is not None:
            for action in self.fail_action_list:
                action.process(player, possible_cards, trick_pile)
            return self._fail_node.process(player, possible_cards, trick_pile)
        else:
            return None

    def get_pass_node(self):
        return self._pass_node
    def set_pass_node(self, new_pass_node):
        self._pass_node = new_pass_node

    def get_fail_node(self):
        return self._fail_node
    def set_fail_node(self, new_fail_node):
        self._fail_node = new_fail_node

    def get_check(self):
        return self._check
    def set_check(self, new_check):
        self._check = new_check

    def get_pass_action_list(self):
        return copy.deepcopy(self._pass_action_list)
    def set_pass_action_list(self, new_action_list):
        self._pass_action_list = copy.deepcopy(new_action_list)

    def get_fail_action_list(self):
        return copy.deepcopy(self._fail_action_list)
    def set_fail_action_list(self, new_action_list):
        self._fail_action_list = copy.deepcopy(new_action_list)

    def get_enter_action_list(self):
        return copy.deepcopy(self._enter_action_list)
    def set_enter_action_list(self, new_action_list):
        self._enter_action_list = copy.deepcopy(new_action_list)

    pass_node = property(get_pass_node, set_pass_node)
    fail_node = property(get_fail_node, set_fail_node)
    check = property(get_check, set_check)

    pass_action_list = property(get_pass_action_list, set_pass_action_list)
    fail_action_list = property(get_fail_action_list, set_fail_action_list)
    enter_action_list = property(get_enter_action_list, set_enter_action_list)


class _LeafNode(_Node):
    def __init__(self):
        _Node.__init__(self, None, None, Constant.Check.Empty)


class ValueCheckNode(_Node):

    _comparison_value = 0
    _comparison_type = 0

    def __init__(self, comparison_value, comparison_type, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.comparison_value = comparison_value
        self.comparison_type = comparison_type
        return

    def process(self, player, possible_cards, trick_pile):
        passed = False
        new_card_list = []
        for card in possible_cards:
            if self.comparison_type == Constant.ComparisonType.Equal:
                if card.value == self.comparison_value:
                    passed = True
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.GreaterThan:
                if card.value > self.comparison_value:
                    passed = True
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.GreaterThanOrEqual:
                if card.value >= self.comparison_value:
                    passed = True
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.LessThan:
                if card.value < self.comparison_value:
                    passed = True
                    new_card_list.append(card)
            elif self.comparison_type == Constant.ComparisonType.LessThanOrEqual:
                if card.value <= self.comparison_value:
                    passed = True
                    new_card_list.append(card)

        if passed:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def get_comparison_type(self):
        return self._comparison_type
    def set_comparison_type(self, new_comparison_type):
        self._comparison_type = new_comparison_type

    def get_comparison_value(self):
        return self._comparison_value
    def set_comparison_value(self, new_comparison_value):
        self._comparison_value = new_comparison_value

    comparison_type = property(get_comparison_type, set_comparison_type)
    comparison_value = property(get_comparison_value, set_comparison_value)


class SuitCheckNode(_Node):

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self._suit = suit
        return

    def process(self, player, possible_cards, trick_pile):
        passed = False
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                passed = True
                new_card_list.append(card)

        if passed:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def get_suit(self):
        return self._suit
    def set_suit(self, new_suit):
        self._suit = new_suit

    suit = property(get_suit, set_suit)


class CardCheckNode(_Node):

    _suit = 0
    _value = 0

    def __init__(self, suit, value, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        self.value = value
        return

    def process(self, player, possible_cards, trick_pile):
        passed = False
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                if card.value == self.value:
                    passed = True
                    new_card_list.append(card)

        if passed:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def get_suit(self):
        return self._suit
    def set_suit(self, new_suit):
        self._suit = new_suit

    def get_value(self):
        return self._value
    def set_value(self, new_value):
        self._value = new_value

    suit = property(get_suit, set_suit)
    value = property(get_value, set_value)


class NumberInSuitCheckNode(_Node):

    _suit = 0
    _comparison_number = 0

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        self.comparison_number = 3

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                new_card_list.append(card)

        if 0 < len(new_card_list) <= self.comparison_number:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)

    def get_suit(self):
        return self._suit
    def set_suit(self, new_suit):
        self._suit = new_suit

    def get_comparison_number(self):
        return self._comparison_number
    def set_comparison_number(self, new_comparison_number):
        self._comparison_number = new_comparison_number

    suit = property(get_suit, set_suit)
    comparison_number = property(get_comparison_number, set_comparison_number)


class SelectHighestValueLeaf(_LeafNode):
    def __init__(self):
        _LeafNode.__init__(self)
        return

    def process(self, player, possible_cards, trick_pile):

        highest_card = None
        # print "Finding highest value"
        for card in possible_cards:
            if highest_card is None:
                # print "Found a higher card"
                highest_card = card
            elif card.value > highest_card.value:
                # print "Found a higher card"
                highest_card = card

        return highest_card


class SelectLowestValueLeaf(_LeafNode):
    def __init__(self):
        _LeafNode.__init__(self)
        return

    def process(self, player, possible_cards, trick_pile):

        lowest_card = None
        for card in possible_cards:
            if lowest_card is None:
                lowest_card = card
            elif card.value < lowest_card.value:
                lowest_card = card

        return lowest_card


class SelectCardLeaf(_LeafNode):

    def __init__(self, suit, value):
        _LeafNode.__init__(self)
        self.suit = suit
        self.value = value
        return

    def process(self, player, possible_cards, trick_pile):

        # print possible_cards

        for card in possible_cards:
            if card.value == self.value:
                if card.suit == self.suit:
                    return card

        return None
