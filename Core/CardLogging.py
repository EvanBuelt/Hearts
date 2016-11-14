import datetime


class Logger:
    def __init__(self, file_name, enabled=True):
        self.file_name = file_name
        self.number = 1
        self.enabled = enabled

    def log(self, data):
        if self.enabled:
            if not not data:
                with open(self.file_name, "a") as _file:
                    _file.write(str(self.number) + '. ' + data + '\n')
                    self.number += 1

_now = datetime.datetime.now()
log_file = Logger('Core\Logs\Hearts_' + str(_now.year) + '_' + str(_now.month) + '_' + str(_now.day) + '_' +
                  str(_now.hour) + '_' + str(_now.minute) + '_' + str(_now.second) + '.txt')
