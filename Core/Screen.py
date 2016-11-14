__author__ = 'Evan'


class Screen(object):
    def __init__(self):
        self.ui_list = []
        return

    def add_ui_element(self, ui_element):
        self.ui_list.append(ui_element)
        return

    def remove_ui_element(self, ui_element):
        if ui_element in self.ui_list:
            self.ui_list.remove(ui_element)
        return

    def remove_all_ui_elements(self):
        self.ui_list = []
        return

    def enter(self):
        for ui_element in self.ui_list:
            ui_element.visible = True
        return

    def exit(self):
        for ui_element in self.ui_list:
            ui_element.visible = False
        return