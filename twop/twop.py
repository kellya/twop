import os
import sys
import json
import openproject
import taskwarrior

# import argparse
# import logging

# logger = logging.getLogger(__name__)
configfile_name = "twop.json"


def _init_config():
    """
    Create a new configuration from nothing
    """
    config = {'lessThanDaysAgo': '30', }

    config['op'] = {}

    # get basic information to contact OpenProject
    config['op']['baseUrl'] = input("OpenProject Site: ")
    config['op']['apiKey'] = input("Your API key: ")

    op = openproject.openproject(
        config['op']['baseUrl'], config['op']['apiKey'])

    # get information abou who am i
    me = op.whoami()
    config['op']['userId'] = me['id']

    # get all projects to choose from which is the
    # principal, later, will collect information about sub projects
    projects = op.listAvailableProjects()
    dirtyProjectDB = {}
    for project in projects:
        print("{0:3d} {1:40s} {2:s} ".format(
            project['id'], project['identifier'], project['name']))
        dirtyProjectDB[str(project['id'])] = project['identifier']

    config['op']['projectID'] = input("What is ID of your project: ")

    # collect information about subprojects, to create maps between openProject projects and taskwarrir projects
    config['maps'] = {dirtyProjectDB[config['op']['projectID']]: ''}

    childProjects = op.searchChildProjects(config['op']['projectID'])
    for childProject in childProjects:
        config['maps'].update({childProject['identifier']: ''})

    tw = taskwarrior.taskwarrior()
    twProjects = tw.listProjects()

    print("\nInformation about your taskwarrior projects\n")
    print("{0:12s} {1:5s}".format('Project', 'Tasks'))
    print("{0:12s} {1:5s}".format('------------', '-----'))
    for name, items in twProjects.items():
        print("{0:12s} {1:5s}".format(name, items))

    with open(configfile_name, 'w') as f:
        json.dump(config, f, indent=2)

    print()
    sys.exit(
        'Add information about TaskWarrior projects in your twop.json configuration file')


def _read_config():

    with open(configfile_name, 'r') as f:
        config = json.load(f)
        return config

    raise Exception('Problem reading config file')


def main():

    # check if there is a config file
    if not os.path.isfile(configfile_name):
        _init_config()

    # read configuration
    config = _read_config()

    op = openproject.openproject(
        config['op']['baseUrl'], config['op']['apiKey'])
    opWPs = op.searchWorkPackage(
        config['op']['userId'], config['lessThanDaysAgo'], config['op']['projectID'])

    tw = taskwarrior.taskwarrior(config['maps'])

    # get all recent work packages changed in last days
    for workPackage in opWPs:
        wp = openproject.wp(op.directCall(
            workPackage['_links']['self']['href']))

        # for debuging
        exclusions = ('0')
        if wp.id in exclusions:
            continue

        # match with a existing task
        if wp.uuid is not None:
            pass
        else:
            # create a new task in taskwarrior
            uuid = tw.new(wp)
            wp.updateUuid(uuid)

        sys.exit()
        # openproject.openproject._ppjson(json.loads(task))

    # parser = argparse.ArgumentParser('tasksync', parents=[oauth2client.tools.argparser])
    # parser.add_argument('--debug', action='store_true', default=False, help='Enable debugging.')
    # args = parser.parse_args()

    # logging.basicConfig(level=logging.INFO)
    # if args.debug:
    #     logging.basicConfig(level=logging.DEBUG)
    #     httplib2.debuglevel=4

    # runbook = executions(args)
    # for p in runbook:
    #     logger.info("Running - %s.", p)
    #     sync_all(runbook[p])


if __name__ == "__main__":
    main()
