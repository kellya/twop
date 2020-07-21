import json
import sys

import requests as request

# https://docs.openproject.org/api/filters/


class openproject:

    def __init__(self, baseUrl, apiKey, debug=False):
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        self.debug = debug

    def _ppjson(self, json_object):
        """
        Helpper function if need to printy print json string
        """
        json_formatted_str = json.dumps(json_object, indent=2)
        print(json_formatted_str)

    def _callCurl(self, method, path, data={}):
        """
        Basic helpper to have just one place to do all API calls
        """
        auth = ('apikey', self.apiKey)

        resp = ''

        if method == 'GET':
            resp = request.get(self.baseUrl + path, auth=auth)
        elif method == 'PUT':
            resp = request.put(self.baseUrl + path,  data)
        elif method == 'POST':
            resp = request.post(self.baseUrl + path, data)
        elif method == 'DELETE':
            resp = request.delete(self.baseUrl + path, )
        else:
            print("Ups")

        if resp.status_code != 200:
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

    def searchWorkPackage(self, userId, days, projectId):
        """
        Search My Tasks modified in last days
        """
        FILTER = [
            {"subprojectId": {"operator": "*", "values": []}},
            {"assignee": {"operator": "=", "values": [userId]}},
            {"updatedAt": {"operator": ">t-", "values": [days]}}]

        # URI = '/api/v3/projects/outros-projetos/queries/default?'+json.dumps(FILTER)
        URI = "/api/v3/projects/{0}/queries/default?filters={1}".format(
            projectId, json.dumps(FILTER))
        print(URI)
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

    def searchUuid(self, uuid):
        # FILTER='filters=[{"subjectOrId":{"operator":"**","values":["65"]}}]'
        FILTER = 'filters=[{"subprojectId":{"operator":"*","values":[]}},{"customField1":{"operator":"~","values":["454d939d"]}}]'
        # URI = '/api/v3/projects/6/queries/default?'+FILTER
        URI = '/api/v3/projects/outros-projetos/queries/default?'+FILTER
        wp = self._callCurl('GET', URI)
        print(wp)

    def searchEmpty(self):
        FILTER = '[{"subprojectId":{"operator":"*","values":[]}},{"customField1":{"operator":"!*","values":[]}},{"assignee":{"operator":"=","values":["4"]}}]'
        URI = '/api/v3/projects/6/queries/default?'+FILTER
        wp = self._callCurl('GET', URI)
        for element in wp['_embedded']['results']['_embedded']['elements']:
            # print(element)
            print("{0:3d} {1:40s} {2:s} ".format(
                element['id'], element['_type'], element['subject']))


class wp:

    def __init__(self, wp):
        self.all = wp
        self.id = str(wp['id'])
        self.uuid = wp['customField1']
        self.entry = wp['createdAt']
        self.description = wp['subject']
        self.due = wp['dueDate']
        self.scheduled = wp['startDate']

        # if key in array:
        # if wp['parent'] is not None and wp['parent']['id'] is not None:

        try:
            self.parent = wp['_embedded']['parent']['id']
        except KeyError:
            self.parent = None

        try:
            self.project = wp['_embedded']['project']['identifier']
        except KeyError:
            self.project = None

        try:
            self.priority = wp['_embedded']['priority']['name']
        except KeyError:
            self.priority = None

        try:
            self.assignee = wp['_embedded']['assignee']['id']
        except KeyError:
            self.assignee = None

        try:
            self.status = wp['_embedded']['status']['name']
        except KeyError:
            self.status = None

        # testestestestestestes
        @property
        def uuid(self):
            return self.__uuid

        @uuid.setter
        def uuid(self, x):
            self.__uuid = x

