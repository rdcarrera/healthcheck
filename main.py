#!/usr/bin/env python
import sys 
import yaml 
import importlib
import getopt
import datetime
import threading
import os
from time import sleep
from dateutil import parser 

class StepData (object):
    def run(self):
        config_file = default_config_folder+self.config_name+".yml"
        if os.path.isfile(config_file) is False:
            return("[CRITICAL] - The config file doesn't exist, please check "+config_file,2)
        if os.path.isfile("./modules/"+self.module_name+".py") is False:
            return("[CRITICAL] - The module file doesn't exist, please check ./modules/"+self.module_name+".py",2)
        module = importlib.import_module('modules.'+self.module_name)
        open(self.lockfile, 'a').close()
        for i in range(0,default_retry_on_faults):
            _module_info = module.main(config_file)
            if _module_info[1] is 0:
                break
            sleep(3)
        if os.path.isfile(self.lockfile):
            os.remove(self.lockfile)
        return _module_info
    def returninfo(self):
        return { 
            'config_name': self.config_name, 
            'module_name': self.module_name, 
            'execution_time': self.execution_time, 
            'result_info': 
            [ 
                self.result_info[0],
                self.result_info[1] 
            ],
            'history_changed_status': self.history_changed_status
            }
    def calculate_history_data(self):
        if os.path.isfile(self.result_file):
            _result_file_load = open(self.result_file,'r')
            _result_file_data = yaml.safe_load(_result_file_load)
            _history_changed_status = _result_file_data["history_changed_status"] 
            if int(_history_changed_status[0].strip().split()[0]) is not self.result_info[1]:
                _state_changed_data = str(self.result_info[1]) + " ||| " + str(self.execution_time) + " ||| " + self.result_info[0] 
                _history_changed_status.insert(0,_state_changed_data)
        else:
            _history_changed_status  = [ str(self.result_info[1]) + " ||| " + str(self.execution_time) + " ||| " + self.result_info[0] ]
        if len(_history_changed_status) > default_max_history_data:
            del _history_changed_status[-1]
        return _history_changed_status

    def __init__(self,module_name, config_name, result_file,lockfile):
        print("[ " + str(datetime.datetime.now()) + " ] - [START] - [ " + str(threading.current_thread().name) + " ] - Executing test " + config_name + " in background...")
        self.module_name = module_name
        self.config_name = config_name
        self.result_file = result_file
        self.lockfile = lockfile
        self.result_info = self.run()
        self.execution_time = datetime.datetime.now()
        self.history_changed_status = self.calculate_history_data()
        with open(result_file, 'w') as _outfile:
            yaml.dump(self.returninfo(), _outfile, default_flow_style=False)
        print("[ " + str(datetime.datetime.now()) + " ] -  [END]  - [ "+str(threading.current_thread().name)+" ] - Executing test " + config_name + " in background...")
        return None
        
def time_comparation(result_file,external_config):
    if os.path.isfile(result_file):
        if "seconds_interval" not in external_config:
            seconds_interval = default_seconds_interval
        else:
            seconds_interval = external_config["seconds_interval"]
        result_file_load = open(result_file,'r')
        result_file_data = yaml.safe_load(result_file_load)
        next_execution_time = result_file_data["execution_time"]+datetime.timedelta(seconds=seconds_interval)
        if datetime.datetime.now() < next_execution_time:
            return False
    return True

 
def main(argv):
    health_check_config = ''
    try:
        opts, _args = getopt.getopt(argv,"c:",["config="])
    except getopt.GetoptError:
        print("main.py -c <config>")
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-c", "--config"):
            health_check_config = arg
    if health_check_config == "":
        health_check_config = "./templates/Healthcheck.yml"
    if os.path.isfile(health_check_config) is False:
        print("[ " + str(datetime.datetime.now()) + " ] -[CRITICAL] - The config of the health check proccess doesn't exist, please check "+health_check_config)
        sys.exit(2)

    config_process_load = open(health_check_config,'r')
    config_process = yaml.safe_load(config_process_load)

    try:
        global default_seconds_interval
        if "default_seconds_interval" not in config_process["config"]:
            default_seconds_interval = 60
        else:
            default_seconds_interval = config_process["config"]["default_seconds_interval"]

        if "default_proccess_wait_time" not in config_process["config"]:
            default_proccess_wait_time = 5
        else:
            default_proccess_wait_time = config_process["config"]["default_proccess_wait_time"]

        if "default_history_folder" not in config_process["config"]:
            default_history_folder = "./history/"
        else:
            default_history_folder = config_process["config"]["default_history_folder"]
        
        if not os.path.exists(default_history_folder):
            os.makedirs(default_history_folder)

        global default_config_folder
        if "default_config_folder" not in config_process["config"]:
            default_config_folder = "./templates/"
        else:
            default_config_folder = config_process["config"]["default_config_folder"]

        global default_retry_on_faults
        if "default_retry_on_faults" not in config_process["config"]:
            default_retry_on_faults = 3
        else:
            default_retry_on_faults = config_process["config"]["default_retry_on_faults"]

        global default_lock_folder
        if "default_lock_folder" not in config_process["config"]:
            default_lock_folder = "./lock/"
        else:
            default_lock_folder = config_process["config"]["default_lock_folder"]
        if not os.path.exists(default_lock_folder):
            os.makedirs(default_lock_folder)

        global default_max_history_data
        if "default_max_history_data" not in config_process["config"]:
            default_max_history_data = 2048
        else:
            default_max_history_data = config_process["config"]["default_max_history_data"]

        print("[ " + str(datetime.datetime.now()) + " ] - Loaded config file " + health_check_config + " the process is going to start...")

        try: 
            while True:
                for _iterator in range(len(config_process["tasks"])):

                    for _iterator2 in range(len(config_process["tasks"][_iterator]["steps"])):
                
                        result_file = default_history_folder+config_process["tasks"][_iterator]["steps"][_iterator2]["name"]+".yml"
                        if time_comparation(result_file,config_process["tasks"][_iterator]["steps"][_iterator2]) is False:
                            continue
                        lockfile = default_lock_folder+config_process["tasks"][_iterator]["steps"][_iterator2]["name"]+".lck"
                        if os.path.isfile(lockfile) is False:
                            threading.Thread(target=StepData, args=(config_process["tasks"][_iterator]["steps"][_iterator2]["module"],config_process["tasks"][_iterator]["steps"][_iterator2]["name"],result_file,lockfile)).start()
                
                sleep(default_proccess_wait_time)
        except KeyboardInterrupt:
            print("[ " + str(datetime.datetime.now()) + " ] - [ STOPPING ] - The user stopped the proccess")
            sys.exit(0)
        except:
            print("[ " + str(datetime.datetime.now()) + " ] - Undefined error.")
            sys.exit(0)

    except (KeyError,TypeError) as _error:
        print("[ " + str(datetime.datetime.now()) + " ] - [CRITICAL] - The config file "+health_check_config+" is invalid")
        sys.exit(2)


if __name__ == "__main__":
    print("[ " + str(datetime.datetime.now()) + " ] - [STARTING] - The process is starting")
    main(sys.argv[1:])
            
