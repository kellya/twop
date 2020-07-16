import requests as request
import json
import sys

# https://docs.openproject.org/api/filters/



class openproject:

    def __init__(self, baseUrl, apiKey, debug=False):
        self.baseUrl = baseUrl
        self.apiKey = apiKey
        self.debug = debug

    def _ppjson(self, json_object):

        json_formatted_str = json.dumps(json_object, indent=2)

        print(json_formatted_str)

    def _callCurl(self, method, path, data={}):
        auth = ('apikey', self.apiKey)

        resp = ''

        if method == 'GET':
            resp = request.get(self.baseUrl + path, auth=auth)
        elif method == 'PUT':
            resp = request.put(self.baseUrl + path, data)
        elif method == 'POST':
            resp = request.post(self.baseUrl + path, data)
        elif method == 'DELETE':
            resp = request.delete(self.baseUrl + path)
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

    def whoami(self):
        URI = '/api/v3/users/me'
        me = self._callCurl('GET', URI)
        return me

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

    def getWorkPackage(self, id):
        URI = '/api/v3/work_packages/'+str(id)
        wp = self._callCurl('GET', URI)
        print(wp)

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

    def listAvailableProjects(self):
        URI = '/api/v3/queries/available_projects'
        projects = self._callCurl('GET', URI)
        for project in projects:
            print("{0:3d} {1:20s} {2:s} ".format(
                project['id'], project['identifier'], project['name']))

