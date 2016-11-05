from Core import Constant
import copy

__author__ = 'Evan'


class _Action:

    _check = Constant.Check.Empty

    def __init__(self, check):
        self.check = check
        return

    def set_check(self, check):
        self._check = check
    def get_check(self):
        return self._check

    check = property(get_check, set_check)


class KeepValueAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveValueAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class KeepSuitAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveSuitAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class KeepCardAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class RemoveCardAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class FindHighestCardAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return


class FindLowestCardAction(_Action):
    def __init__(self, check):
        _Action.__init__(self, check)
        return
