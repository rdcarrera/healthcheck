#!/usr/bin/env python
import sys, yaml, importlib, getopt, datetime, threading, os
from dateutil import parser 

CONFIG_DIRECTORY = "./config/"
HISTORY_DIRECTORY = "./history/"
SECONDS_INTERVAL = 300

class StepData (object):
    def run(self):
        config_file = CONFIG_DIRECTORY+self.config_name+".yml"
    	if os.path.isfile(config_file) is False:
    		return("[CRITICAL] - The config file doesn't exist, please check "+config_file,2)
        if os.path.isfile("./modules/"+self.module_name+".py") is False:
            return("[CRITICAL] - The module file doesn't exist, please check ./modules/"+self.module_name+".py",2)
        module = importlib.import_module('modules.'+self.module_name)
        return module.main(config_file)
    def returninfo(self):
        return { 
            'config_name': self.config_name, 
            'module_name': self.module_name, 
            'execution_time': self.execution_time, 
            'result_info': 
            [ 
                self.result_info[0],
                self.result_info[1] 
            ] 
            }
    def __init__(self,module_name, config_name, result_file):
        self.module_name = module_name
        self.config_name = config_name
        self.result_info = self.run()
        self.execution_time = datetime.datetime.now()
        with open(result_file, 'w') as _outfile:
            yaml.dump(self.returninfo(), _outfile, default_flow_style=False)
        
def time_comparation(result_file,external_config):
    if os.path.isfile(result_file):
        if "seconds_interval" not in external_config:
            seconds_interval = SECONDS_INTERVAL
        else:
            seconds_interval = external_config["seconds_interval"]
    result_file_load = open(result_file,'r')
    result_file_data = yaml.safe_load(result_file_load)
    yaml.load_all
    next_execution_time = result_file_data["execution_time"]+datetime.timedelta(seconds=seconds_interval)
    if datetime.datetime.now() < next_execution_time:
        return False
    return True


def main(argv):
    health_check_config = ''
    try:
        opts, _args = getopt.getopt(argv,"c:",["config="])
    except getopt.GetoptError:
        print 'main.py -c <config>'
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--config"):
            health_check_config = arg
    if health_check_config == "":
        health_check_config = CONFIG_DIRECTORY+"Healthcheck.yml"
    if os.path.isfile(health_check_config) is False:
        print "[CRITICAL] - The config of the health check proccess doesn't exist, please check "+health_check_config
        sys.exit(2)
    if not os.path.exists(HISTORY_DIRECTORY):
        os.makedirs(HISTORY_DIRECTORY)

    config_file_load = open(health_check_config,'r')
    config = yaml.safe_load(config_file_load)

    try:
        for _iterator in range(len(config["tasks"])):
            for _iterator2 in range(len(config["tasks"][_iterator]["steps"])):
                result_file = HISTORY_DIRECTORY+config["tasks"][_iterator]["steps"][_iterator2]["name"]+".yml"
                if time_comparation(result_file,config["tasks"][_iterator]["steps"][_iterator2]) is False:
                    continue

                threading.Thread(target=StepData, args=(config["tasks"][_iterator]["steps"][_iterator2]["module"],config["tasks"][_iterator]["steps"][_iterator2]["name"],result_file)).start()

    except (KeyError,TypeError) as _error:
        print "[CRITICAL] - The config file "+health_check_config+" is invalid"
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
