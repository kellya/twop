import json
import re
from datetime import datetime


class task:

    """
    This class is to conver information between taskwarrior and openproject
    """

    def __init__(self, projects={}):
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
            "priority",
            "id"]
        
        for op, tw in projects.items():
            self.mapOPTW[op] = tw
            self.mapTWOP[tw] = op


    def hello(self):
        print("hello")

    def _getOPProject(self, project):
        """
        Given a string, return project name in OpenProject
        """
        if project == '':
            raise Exception("Must not be empty")

        return self.mapTWOP.get(project,'')

    def _getTWProject(self, project):
        """
        Given a string, return project name in TaskWarrior
        """
        if project == '':
            raise Exception("Must not be empty")

        return self.mapOPTW.get(project,'')

    def _readDateFromOP(self, date):
        if date is None:
            return date

        # suporte the Z in the end
        # https://stackoverflow.com/questions/127803/how-do-i-parse-an-iso-8601-formatted-date/49784038#comment94022430_49784038
        date = re.sub(r'Z$', '+00:00', date)

        return datetime.fromisoformat(date)

    def _getTWPriority(self, priority):
        """
            Given a string with OP Priority, convert it to TW Priority, and a boolean to add +NEXT tag
        """

        if priority == 'Low':
            return 'L', False
        elif priority == 'Normal':
            return 'M', False
        elif priority == 'High':
            return 'H', False
        elif priority == 'Immediate':
            return 'H', True
        else:
            return 'M', False

    def _getOPPriority(self, priority, next):
        """
            Given a string with TW Priority and a Boolena, convert it to OP Priority
        """
        if priority == 'L':
            return 'Low', False
        elif priority == 'M':
            return 'Normal', False
        elif priority == 'H' and next is False:
            return 'High'
        elif priority == 'H' and next is True:
            return 'Immediate'
        else:
            return 'Normal'

    def readFromOpenProject(self, wp):
        self.wp = wp
        self.id = str(wp['id'])
        self.uuid = wp['customField1']
        self.entry = self._readDateFromOP(wp['createdAt'])
        self.description = str(wp['subject'])
        self.due = self._readDateFromOP(wp['dueDate'])
        self.scheduled = self._readDateFromOP(wp['startDate'])

        # TODO Need work, never tested
        try:
            self.parent = wp['_embedded']['parent']['id']
        except KeyError:
            self.parent = None

        try:
            self.project = self._getTWProject(
                wp['_embedded']['project']['identifier'])
        except KeyError:
            self.project = None

        try:
            self.priority, self.next = self._getTWPriority(
                wp['_embedded']['priority']['name'])
        except KeyError:
            self.priority = None

        try:
            self.assignee = str(wp['_embedded']['assignee']['id'])
        except KeyError:
            self.assignee = None

        try:
            self.isClosed = wp['_embedded']['status']['isClosed'] == 'true'
        except KeyError:
            self.isClosed = False


    def readFromTaskwarrior(self, task):
        self.wp = None
        self.taskwarrior = task
        self.id = task['id']
        self.uuid = task['uuid']
        self.entry = task['entry']

        self.description = task['description']
        self.due = task['entduery']
        self.scheduled = task['scheduled']

        # TODO Need work, never tested
        try:
            self.parent = task['entry']
        except KeyError:
            self.parent = None

        try:
            self.project = task['project']
        except KeyError:
            self.project = None

        try:
            self.priority = task['priority']
            if "NEXT" in task['tags'].values(): 
                self.next = True
            else
                self.next = False

         except KeyError:
            self.priority = None

        try:
            self.assignee = task['assignee']
        except KeyError:
            self.assignee = None

        try:
            self.isClosed = task['status'] == 'completed' or task['status'] == 'deleted'
        except KeyError:
            self.isClosed = False


    def hasUuid(self):
        if self.uuid is None or self.uuid == '':
            return False
        return True

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, x):
        self._uuid = x

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, x):
        self._id = x
