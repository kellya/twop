# test taskWarrior API
from taskw import TaskWarrior


w = TaskWarrior(marshal=True)
#  x=w.get_task(uuid="99582f29-5b4d-4db7-aef3-8b149eb948fa")
x=w.get_task()
print(x)