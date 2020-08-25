import json
import sys
import logging
import requests as request
import re
from datetime import datetime
from pprint import pprint # for debugging

# https://docs.openproject.org/api/filters/


class openproject:
    """
    This class is to interact with openproject
    """

    def __init__(self, baseUrl, apiKey, projectId, debug=False):
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        self.debug = debug
        self.projectId = projectId

    def _ppjson(self, json_text):
        """
        Helpper function if need to printy print json string
        """
        # json_object = json.loads(json_text)
        json_formatted_str = json.dumps(json_text, indent=2)
        print(json_formatted_str)

    # borrow from twopTask
    def _readDateFromOP(self, date):
        if date is None:
            return date

        # suporte the Z in the end
        # https://stackoverflow.com/questions/127803/how-do-i-parse-an-iso-8601-formatted-date/49784038#comment94022430_49784038
        date = re.sub(r'Z$', '+00:00', date)

        return datetime.fromisoformat(date)

    def _callCurl(self, method, path, data={}):
        """
        Basic helpper to have just one place to do all API calls
        """
        auth = ('apikey', self.apiKey)

        resp = ''
        method = method.upper()

        if method == 'GET':
            resp = request.get(self.baseUrl + path, auth=auth)
        elif method == 'PUT':
            resp = request.put(self.baseUrl + path, auth=auth, json=data)
        elif method == 'POST':

            # debug
            # https://requests.readthedocs.io/en/master/api/?highlight=debug#api-changes
            # from http.client import HTTPConnection
            # HTTPConnection.debuglevel = 1
            # # You must initialize logging, otherwise you'll not see debug output.
            # logging.basicConfig()
            # logging.getLogger().setLevel(logging.DEBUG)
            # requests_log = logging.getLogger("urllib3")
            # requests_log.setLevel(logging.DEBUG)
            # requests_log.propagate = True
            # print(data)

            resp = request.post(self.baseUrl + path, auth=auth, json=data)
            # print(request)
        elif method == 'DELETE':
            resp = request.delete(self.baseUrl + path, auth=auth)
        elif method == 'PATCH':
            resp = request.patch(self.baseUrl + path, auth=auth, json=data)

        else:
            print("Ups")

        if not (resp.status_code >= 200 and resp.status_code <= 299):
            print(resp.text)
            raise Exception('Unexpected result ' + str(resp.status_code))

        jr = json.loads(resp.text)
        return jr
        # ppjson(jr)
        # print (jr['_embedded']['elements'])

        # print (jr.keys())

        # for key in jr.keys() :
        #     print("{0:30s} {1:s}".format(key,str(jr[key])))

        # return jr['_embedded']['elements']

    def directCall(self, url, method='GET'):
        return self._callCurl(method, url)

    def whoami(self):
        """
        Discover who am I in openproject
        """
        URI = '/api/v3/users/me'
        return self._callCurl('GET', URI)

    def searchWorkPackage(self, userId, days):
        """
        Search My Tasks modified in last days
        """
        FILTER = [
            {"subprojectId": {"operator": "*", "values": []}},
            {"assignee": {"operator": "=", "values": [userId]}},
            {"updatedAt": {"operator": ">t-", "values": [days]}},
            {"type": {"operator": "=", "values": ["1"]}}
        ]

        # URI = '/api/v3/projects/outros-projetos/queries/default?'+json.dumps(FILTER)
        URI = "/api/v3/projects/{0}/queries/default?filters={1}".format(
            self.projectId, json.dumps(FILTER))
        # print(URI)
        ret = self._callCurl('GET', URI)

        # return just results
        return ret['_embedded']['results']['_embedded']['elements']

    def getWorkPackage(self, id):
        URI = '/api/v3/work_packages/'+str(id)
        return self._callCurl('GET', URI)

    def searchChildProjects(self, projectID):
        fProjectID = {"parent_id": {"operator": "=", "values": [projectID]}}
        FILTER = [fProjectID]
        URI = '/api/v3/projects?filters='+json.dumps(FILTER)
        ret = self._callCurl('GET', URI)

        # return just results
        return ret['_embedded']['elements']

    def listAvailableProjects(self):
        """
        List Available projects in OpenProject
        """
        URI = '/api/v3/queries/available_projects'
        projects = self._callCurl('GET', URI)
        ret = []
        for project in projects["_embedded"]["elements"]:
            tmp = {}
            tmp['id'] = project['id']
            tmp['identifier'] = project['identifier']
            tmp['name'] = project['name']
            ret.append(tmp)
        return ret

    def _updateField_uuid(self, task):
        wp = task.wp

        data = {"customField1": task.uuid, "lockVersion": wp['lockVersion']}

        self._callCurl(wp['_links']['updateImmediately']['method'],
                       wp['_links']['updateImmediately']['href'],
                       data)

    def _updateField_status(self, task):
        wp = task.wp

        if task.isClosed:
            strStatus='Closed'
        else:
            strStatus='In progress'

        data = {"_links": {
            "status": {"href": self._getStatusHref(strStatus)}},
            "lockVersion": wp['lockVersion']
        }

        self._callCurl(wp['_links']['updateImmediately']['method'],
                       wp['_links']['updateImmediately']['href'],
                       data)

    def update(self, task, field=None):
        """
            Just update status
            TODO update dependencies
            TODO update project name
            TODO update priority
            TODO soft fail if uuid does not exist
        """

        # just update if previous information is is newer
        if  self._readDateFromOP(task.wp['updatedAt']) > task.modified:
                pass
                print("OpenProject has newer information. Skip")
                return     


        if field is not None:
            update_func = getattr(
                self, '_updateField_{0}'.format(field), lambda x: x)
            return update_func(task)

        statusName = task.wp['_links']['status']['title']
        closedStatus = ['Closed', 'Rejected']

        # if it is closed in TaskWarrior and can be closed, change status
        if task.isClosed:
            if statusName not in closedStatus:
                update_func = getattr(
                    self, '_updateField_{0}'.format('status'), lambda x: x)
                return update_func(task)
        else:
            if statusName in closedStatus:
                update_func = getattr(
                    self, '_updateField_{0}'.format('status'), lambda x: x)
                return update_func(task)

    def searchUuid(self, uuid):
        FILTER = [
            {"subprojectId": {"operator": "*", "values": []}},
            {"customField1": {"operator": "=", "values": [uuid]}},
            {"type": {"operator": "=", "values": ["1"]}}
        ]
        URI = "/api/v3/projects/{0}/queries/default?filters={1}".format(
            self.projectId, json.dumps(FILTER))

        result = self._callCurl('GET', URI)

        if result['_embedded']['results']['count'] != 1:
            return None

        return result['_embedded']['results']['_embedded']['elements'][0]

    def _getStatusHref(self, strStatus):
        status = {"New": "/api/v3/statuses/1",
                  "In progress": "/api/v3/statuses/7",
                  "Closed": "/api/v3/statuses/12"}

        return status[strStatus]

    def _getPriorityHref(self, strPriority):
        priority = {'Low': "/api/v3/priorities/7",
                    "Normal": "/api/v3/priorities/8",
                    'High': "/api/v3/priorities/9",
                    'Immediate': "/api/v3/priorities/10"}

        return priority[strPriority]

    def new(self, task):
        info = task.readToOpenProject()
        # TODO turn it automatic
        data = {
            "subject": info['subject'],
            "description": {
                "format": "textile",
                "raw": "",
                "html": ""
            },
            "_links": {
                # task
                "type": {"href": "/api/v3/types/1"},
                # alwayes new in this case
                "status": {"href": self._getStatusHref('New')},
                "priority": {"href": self._getPriorityHref(info['priority'])},
                # me
                # TODO to do it with config info
                "assignee": {"href": "/api/v3/users/4"}
            },
            "customField1": info['customField1']
        }

        URI = "/api/v3/projects/{0}/work_packages/".format(
            info['project'])
        # print(URI)
        # print(data)
        self._callCurl('POST', URI, data)
        # self._ppjson(result)

    """
    UnUsed Functions from previous testes
    """

    def listProjects(self):
        URI = '/api/v3/projects'
        projects = self._callCurl('GET', URI)
        for project in projects:
            print("{0:3d} {1:20s} {2:s} ".format(
                project['id'], project['identifier'], project['name']))

    def listPriorities(self):
        URI = '/api/v3/priorities'
        priorities = self._callCurl('GET', URI)
        for priority in priorities:
            print("{0:20s} {1:s}".format(
                priority['name'], priority['_links']['self']['href']))

    def searchEmpty(self):
        FILTER = '[{"subprojectId":{"operator":"*","values":[]}},{"customField1":{"operator":"!*","values":[]}},{"assignee":{"operator":"=","values":["4"]}}]'
        URI = '/api/v3/projects/6/queries/default?'+FILTER
        wp = self._callCurl('GET', URI)
        for element in wp['_embedded']['results']['_embedded']['elements']:
            # print(element)
            print("{0:3d} {1:40s} {2:s} ".format(
                element['id'], element['_type'], element['subject']))
