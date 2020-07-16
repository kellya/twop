import json
import os
import openproject
import taskwarrior

# import argparse
# import logging

# logger = logging.getLogger(__name__)
configfile_name = "twop.json"

def _init_config():
    # Create the configuration file as it doesn't exist yet
    config = {'key1': 'value1', 'key2': 'value2'}

    config['op']={}
    config['op']['baseUrl'] = input("OpenProject Site: ")
    config['op']['apiKey'] = input("Your API key: ")
    
    op = openproject.openproject(config['op']['baseUrl'],config['op']['apiKey'])
    me = op.whoami()
    print (me)
    
    config['op']['userId'] = me
    
    with open(configfile_name, 'w') as f:
        json.dump(config, f)

def _read_config():

    with open(configfile_name, 'r') as f:
        config = json.load(f)
        return config

    raise Exception('Problem reading config file')

def pull():
    pass

def push():
    pass

def main():

    x=taskwarrior.taskwarrior()
    x.hello()

    #check if there is a config file
    if not os.path.isfile(configfile_name):
        _init_config()

    # read configuration
    config = _read_config()

    print(config)

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
