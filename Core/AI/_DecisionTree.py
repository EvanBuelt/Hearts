from Core import Constant


class Check:
    Empty = 0
    TrickPile = 1
    PlayerHand = 2


class ComparisonType:
    Empty = 0
    Equal = 1
    LessThan = 2
    LessThanOrEqual = 3
    GreaterThan = 4
    GreaterThanOrEqual = 5


class _Action:

    _check = Check.Empty

    def __init__(self, check):
        return

    def set_check(self, check):
        self._check = check

    def get_check(self):
        return self._check

    check = property(get_check, set_check)


class KeepValue(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveValue(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class KeepSuit(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveSuit(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class KeepCard(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveCard(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class _Node:

    _pass_node = None
    _fail_node = None
    _check = Check.Empty

    def __init__(self, pass_node, fail_node, check):
        self.pass_node = pass_node
        self.fail_node = fail_node
        self.check = check
        return

    def process(self, player, possible_cards, trick_pile):
        return

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

    pass_node = property(get_pass_node, set_fail_node)
    fail_node = property(get_fail_node, set_fail_node)
    check = property(get_check, set_check)


class ValueCheckNode(_Node):

    _comparison_value = 0
    _comparison_type = ComparisonType.Empty

    def __init__(self, comparison_value, comparison_type, check, pass_node=None, fail_node=None):
        _Node.__init__(self, pass_node, fail_node, check)
        self.comparison_value = comparison_value
        self.comparison_type = comparison_type
        return

    def process(self, player, possible_cards, trick_pile):
        new_card_list = []
        if self.comparison_type == ComparisonType.Equal:
            return
        elif self.comparison_type == ComparisonType.GreaterThan:
            return
        elif self.comparison_type == ComparisonType.GreaterThanOrEqual:
            return
        elif self.comparison_type == ComparisonType.LessThan:
            return
        elif self.comparison_type == ComparisonType.LessThanOrEqual:
            return
        return

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
        return

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
        return

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


class HighestValueLeaf:
    def __init__(self):
        return


class LowestValueLeaf:
    def __init__(self):
        return
