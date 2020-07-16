# test taskWarrior API
from taskw import TaskWarrior

class taskwarrior:

    def __init__(self):
        self.db = TaskWarrior(marshal=True)

    def hello(self):
        #  x=w.get_task(uuid="99582f29-5b4d-4db7-aef3-8b149eb948fa")
        x=self.db.get_task()
        print(x)