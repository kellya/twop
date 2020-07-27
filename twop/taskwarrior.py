# test taskWarrior API
import re
import sys
import tasklib

class taskwarrior:
    """
    This class is to interact with taskwarrior
    """

    def __init__(self, maps={}):
        self.tw = tasklib.TaskWarrior()

    def listProjects(self):
        tmp = self.tw.execute_command(['projects'])
        ret = {}
        for line in tmp:
            m = re.search(r'^(\w+)(\s*)(\d+)$', line)
            if m is not None:
                ret[m.group(1)] = m.group(3)

        return ret

    def update(self,task):
        """
            Just update status
            TODO update dependencies
            TODO update project name
            TODO update priority
            TODO soft fail if uuid does not exist
        """


        twTask = self.tw.tasks.get(uuid=task.uuid)
        
        # if it is closed in OpenProject and can be closed, mark as done
        if task.isClosed:
            if twTask.waiting or twTask.pending:
                twTask.done()
                twTask.save()
        else:
            # if already marked as done, return to active
            if twTask.completed or twTask.deleted:
                twTask["status"]='pending'
                twTask.save()


    def new(self,task):
        localTask = tasklib.Task(self.tw)
        localTask['description'] = task.description
        localTask['due'] = task.due
        localTask['wait'] = task.scheduled
        localTask['priority'] = task.priority
        localTask['project'] = task.project
        if task.next:
            localTask['tags'] = ['NEXT']

        localTask.save()
        task.uuid = localTask['uuid']


    def searchTasks(self,days):
        filterdate = "today-{0:d}days".format(int(days))
        return self.tw.tasks.filter(modified__after=filterdate)
