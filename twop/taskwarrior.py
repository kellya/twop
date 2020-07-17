# test taskWarrior API
import re
from tasklib import TaskWarrior

class taskwarrior:

    def __init__(self):
        self.tw = TaskWarrior()

    def listProjects(self):
        tmp = self.tw.execute_command(['projects'])
        ret = { }
        for line in tmp:
            m = re.search(r'^(\w+)(\s*)(\d+)$', line)
            if m is not None:
                ret[m.group(1)]=m.group(3)

        return ret

    def hello(self):
        x=self.tw.tasks.pending()
        print(x)
        