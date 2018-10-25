#!/usr/bin/env python
import sys
from modules.httpGetString import HttpGetString
httpGetStringResult = HttpGetString()
print httpGetStringResult[0]
sys.exit(httpGetStringResult[1])


    StepData.module_name=config["tasks"][_iterator]["steps"][_iterator2]["module"]
    StepData.config_name=config["tasks"][_iterator]["steps"][_iterator2]["name"]

    StepData.config_file=CONFIG_DIRECTORY+config["tasks"][_iterator]["steps"][_iterator2]["name"]+".yml"

    StepData.module = importlib.import_module('modules.'+StepData.module_name)
    StepData.result = StepData.module.main( StepData.config_file )


StepData(config["tasks"][_iterator]["steps"][_iterator2]["module"],config["tasks"][_iterator]["steps"][_iterator2]["name"],CONFIG_DIRECTORY+ResultMatrix[_iterator][_iterator2].config_name+".yml",importlib.import_module('modules.'+ResultMatrix[_iterator][_iterator2].module_name),ResultMatrix[_iterator][_iterator2].module.main( ResultMatrix[_iterator][_iterator2].config_file ))
