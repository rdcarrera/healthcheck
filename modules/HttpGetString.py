# Module: httpGetString
# Author: rdcarrera
# Version: 0.1
# Require:
#       Module - portOpen
#       Config - template httpGetString
# Check petition to a http server and validate a string

#def httpGetString()

# Import of the requirenments
import yaml
import urllib
import os.path
from extras.PortOpen import PortOpen


def main ( config_path = "templates/HttpGetString.yml" ):
    # Import of the configuration files
    if os.path.isfile(config_path) is False:
	return("[CRITICAL] - The config file doesn't exist, please check "+config_path,2)

    with open(config_path, 'r') as yaml_stream:
        try:
            httpgetstring = yaml.load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)


    # Verification of the parameters
    if isinstance(httpgetstring["module"], str) is False or  \
       httpgetstring["module"] != "HttpGetString":
           return("[CRITICAL] - The config file doesn't correspont with the module, please check "+config_path,2)

    if isinstance(httpgetstring["conf"]["host"], str) is False:
        return("[CRITICAL] - The defined host value isn't valid, please check "+config_path,2)

    if isinstance(httpgetstring["conf"]["port"], int) is False:
        return("[CRITICAL] - The defined port value isn't valid, please check "+config_path,2)

    if len(httpgetstring["conf"]["string"]) is 0:
        return("[CRITICAL] - You doesn't define any string in the config, please check "+config_path,2)

    if isinstance(httpgetstring["conf"]["code"], int) is False:
        return("[CRITICAL] - The defined response code is incorrect, please check "+config_path,2)

    for _iterator in range(len(httpgetstring["conf"]["string"])):
        if isinstance(httpgetstring["conf"]["string"][_iterator], str) is False:
                return("[CRITICAL] - The defined strings aren't correct, please check "+config_path,2)

    if isinstance(httpgetstring["conf"]["anomaly_exit"], int) is False:
        exit_code = 1
        exit_value="WARNING"
    else:
        exit_code = httpgetstring["conf"]["anomaly_exit"]
        if exit_code == 0:
            exit_value="OK"
        elif exit_code == 1:
            exit_value="WARNING"
        elif exit_code == 2:
            exit_value="CRITICAL"
        else:
            exit_value="UNKNOWN"


    #Check comunication with the services
    if PortOpen(httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]) != 0:
        return("["+exit_value+"] - Host unreachable %s:%s" % (httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]),exit_code)

    # Capturar la web
    urlParse = ("%s://%s:%i%s" % (httpgetstring["conf"]["protocol"],httpgetstring["conf"]["host"],httpgetstring["conf"]["port"],httpgetstring["conf"]["context"]))
    _dataresponse = urllib.urlopen(urlParse, data=None)
    if _dataresponse.getcode() is not httpgetstring["conf"]["code"]:
        return("["+exit_value+"] - The response code isn't valid: %i" % (_dataresponse.getcode()),exit_code)
    vardata = _dataresponse.read()
    for _iterator2 in range(len(httpgetstring["conf"]["string"])):
        if httpgetstring["conf"]["string"][_iterator2] not in vardata:
            return("["+exit_value+"] - The defined string %s wasn't found in the website %s" % (httpgetstring["conf"]["string"][_iterator2],urlParse),exit_code)

    return("[OK] - The website: %s was verified" % (urlParse),0)
