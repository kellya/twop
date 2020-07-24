import json
import sys
import logging
import requests as request

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
            from http.client import HTTPConnection
            HTTPConnection.debuglevel = 1
            # You must initialize logging, otherwise you'll not see debug output.
            logging.basicConfig()
            logging.getLogger().setLevel(logging.DEBUG)
            requests_log = logging.getLogger("urllib3")
            requests_log.setLevel(logging.DEBUG)
            requests_log.propagate = True
            print(data)


            resp = request.post(self.baseUrl + path, auth=auth, json=data)
            print(request)
        elif method == 'DELETE':
            resp = request.delete(self.baseUrl + path, auth=auth)
        elif method == 'PATCH':
            resp = request.patch(self.baseUrl + path, auth=auth, json=data)

        else:
            print("Ups")

        if not (resp.status_code >= 200 and resp.status_code <= 299) :
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

    def update(self, task, field=None):

        if field is not None:
            update_func = getattr(
                self, '_updateField_{0}'.format(field), lambda x: x)
            return update_func(task)

        # TODO Generic update, finding fields to be updated

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

    def new(self, task):
        task.hello()
        print(task)

        data = { 
            "subject": "My subject",
            "description": {
                "format": "textile",
                "raw": "teste",
                "html": "teste"
            },
            "_links": {
                "type": {"href": "/api/v3/types/1"},
                "status": {"href": "/api/v3/statuses/1"},
                "priority": {"href": "/api/v3/priorities/8"},
                "assignee": {"href": "/api/v3/users/4"}
            },
            "customField1" : "5750d112-2954-4d0f-a9b9-f6428c467d44"
        } 
            # ,
            # "customField1": "f70011dc-5bc5-4c75-9a09-052179fbfd1c"

        URI = "/api/v3/projects/{0}/work_packages/".format(
            "outros-projetos")
#        URI = "/api/v3//work_packages/form"
        print(URI)
        # print(json.dumps(CONTENT))
        # result = self._callCurl('POST', URI, str(json.dumps(CONTENT)))
        result = self._callCurl('POST', URI, data)
        self._ppjson(result)
        # “Content-Type: application/json”

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
