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

now = datetime.datetime.now()
log_file = Logger('Hearts_' + str(now.year) + '_' + str(now.month) + '_' + str(now.day) + '_' + str(now.hour) +
                  '_' + str(now.minute) + '_' + str(now.second) + '.txt')
