# test taskWarrior API
import re
import sys
from tasklib import TaskWarrior, Task


class taskwarrior:

    def __init__(self, maps={}):
        self.tw = TaskWarrior()
        self.mapTWOP = {}
        self.mapOPTW = {}
        self.fields = [
            "status",
            "uuid",
            "description",
            "due",
            "scheduled",
            "parent",
            "project",
            "priority"
        ]

        for op, tw in maps.items():
            self.mapOPTW[op] = tw
            self.mapTWOP[tw] = op

        print(self.mapTWOP)
        print(self.mapOPTW)

    def listProjects(self):
        tmp = self.tw.execute_command(['projects'])
        ret = {}
        for line in tmp:
            m = re.search(r'^(\w+)(\s*)(\d+)$', line)
            if m is not None:
                ret[m.group(1)] = m.group(3)

        return ret

    def new(self, wp):
        newTask = Task(self.tw)
        for field in self.fields:
            if getattr(wp,field) is not None:
                val = self.'convert_'+field()
                # getattr(wp,field)
                print(val)
            else:
                print("Field Empty: "+field)

        print(newTask)
        print(newTask['uuid'])


    def convert_status(self,str):
        print(str)

    def convert_uuid(self,str):
        print(str)

    def convert_description(self,str):
        print(str)

    def convert_due(self,str):
        print(str)

    def convert_scheduled(self,str):
        print(str)

    def convert_parent(self,str):
        print(str)

    def convert_project(self,str):
        print(str)

    def convert_priority(self,str):
        print(str)
