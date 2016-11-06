from Core import Constant

__author__ = 'Evan'


class _Node:

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
        if self.pass_node is not None:
            for action in self.pass_action_list:
                xrange(0, 1)
            return self.pass_node.process(player, possible_cards, trick_pile)
        else:
            return None

    def _process_fail_node(self, player, possible_cards, trick_pile):
        if self.fail_node is not None:
            for action in self.fail_action_list:
                xrange(0, 1)
            return self.fail_node.process(player, possible_cards, trick_pile)
        else:
            return None


class _LeafNode(_Node):
    def __init__(self):
        _Node.__init__(self, None, None, Constant.Check.Empty)


class ValueCheckNode(_Node):

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

        if len(new_card_list) > 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)


class SuitCheckNode(_Node):

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                new_card_list.append(card)

        if len(new_card_list) > 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)


class CardCheckNode(_Node):

    def __init__(self, suit, value, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        self.value = value
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        # print ""
        # print Constant.suit_str[self.suit]
        # print Constant.value_str[self.value]
        # print ""
        for card in possible_cards:
            if card.suit == self.suit:
                if card.value == self.value:
                    new_card_list.append(card)

        if len(new_card_list) > 0:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)


class NumberInSuitCheckNode(_Node):

    def __init__(self, suit, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.suit = suit
        self.comparison = 3

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []

        for card in possible_cards:
            if card.suit == self.suit:
                new_card_list.append(card)

        if 0 < len(new_card_list) <= self.comparison:
            return self._process_pass_node(player, new_card_list, trick_pile)
        else:
            return self._process_fail_node(player, possible_cards, trick_pile)


class SelectHighestValueLeaf(_LeafNode):
    def __init__(self):
        _LeafNode.__init__(self)
        return

    def process(self, player, possible_cards, trick_pile):

        highest_card = None
        # print "Finding highest value"
        for card in possible_cards:
            if highest_card is None:
                print "Found a higher card"
                highest_card = card
            elif card.value > highest_card.value:
                print "Found a higher card"
                highest_card = card

        return highest_card


class SelectLowestValueLeaf(_LeafNode):
    def __init__(self):
        _LeafNode.__init__(self)
        return

    def process(self, player, possible_cards, trick_pile):

        lowest_card = None
        # print "Finding lowest value"
        for card in possible_cards:
            if lowest_card is None:
                # print "Found a lower card"
                lowest_card = card
            elif card.value < lowest_card.value:
                # print "Found a lower card"
                lowest_card = card

        return lowest_card


class SelectCardLeaf(_LeafNode):

    def __init__(self, suit, value):
        _LeafNode.__init__(self)
        self.suit = suit
        self.value = value
        return

    def process(self, player, possible_cards, trick_pile):

        # print "Finding card"
        print possible_cards

        for card in possible_cards:
            print card.value, self.value
            print card.suit, self.suit
            if card.value == self.value:
                if card.suit == self.suit:
                    # print "Found a card"
                    return card

        return None
