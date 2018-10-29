#!/usr/bin/env python
import sys, yaml, importlib, getopt, time, threading
import os.path
import random

CONFIG_DIRECTORY = "./config/"
HISTORY_DIRECOTRY = "./history/"

class StepData (object):
    def run(self):
        config_file = CONFIG_DIRECTORY+self.config_name+".yml"
    	if os.path.isfile(config_file) is False:
    		return("[CRITICAL] - The config file doesn't exist, please check "+config_file,2)
        if os.path.isfile("./modules/"+self.module_name+".py") is False:
            return("[CRITICAL] - The module file doesn't exist, please check ./modules/"+self.module_name+".py",2)
        module = importlib.import_module('modules.'+self.module_name)
        return module.main(config_file)
    def __init__(self,module_name, config_name):
        self.module_name = module_name
        self.config_name = config_name
        self.result_info = self.run()
        self.execution_time = time.time()
        result_file = HISTORY_DIRECOTRY+config_name+".yml"
        with open(result_file, 'w') as _outfile:
            yaml.dump(self, _outfile, default_flow_style=False)
        print self.result_info[0]

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
    config_file_load = open(health_check_config,'r')
    config = yaml.safe_load(config_file_load)

    try:
        for _iterator in range(len(config["tasks"])):
            for _iterator2 in range(len(config["tasks"][_iterator]["steps"])):
                threading.Thread(target=StepData, args=(config["tasks"][_iterator]["steps"][_iterator2]["module"],config["tasks"][_iterator]["steps"][_iterator2]["name"])).start()
    except (KeyError,TypeError) as _error:
        print "[CRITICAL] - The config file "+health_check_config+" is invalid"
        sys.exit(2)


if __name__ == "__main__":
    main(sys.argv[1:])
