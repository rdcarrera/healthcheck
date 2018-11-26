# Module: HttpGetString
# Author: rdcarrera
# Version: 0.2
# Require:
#       Extras - PortOpen, CheckConfig
#       Config - template HttpGetString
# Check petition to a http server and validate a string

# Import of the requirenments
import yaml
import os.path
import modules.extras.PortOpen as PortOpen
import modules.extras.CheckConfig as CheckConfig
import platform
if int(platform.python_version_tuple()[0]) < 3:
    import urllib
else: 
    import urllib.request as urllib

def main ( config_path = "templates/HttpGetString.yml" ):
    #default config template
    config_template = {
        "module": "str",
        "conf": {
            "anomaly_exit": 0
        },
        "http_conf": {
            "protocol": "str",
            "port": 0,
            "host": "str",
            "context": "str",
            "code": 0
        }
    }

    # Import of the configuration files
    if os.path.isfile(config_path) is False:
        return("[CRITICAL] - The config file doesn't exist, please check "+config_path,2)

    with open(config_path, 'r') as yaml_stream:
        try:
            httpgetstring = yaml.load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)
    
    #Verifiy the configuration
    return_check_config = CheckConfig.main(config_template,httpgetstring,config_path)
    if return_check_config is not None:
      return return_check_config


    #Confirm the module name
    if httpgetstring["module"] != "HttpGetString":
           return("[CRITICAL] - The config file doesn't correspont with the module, please check "+config_path,2)

    #Set the exit values
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
    if PortOpen.main(httpgetstring["http_conf"]["host"],httpgetstring["http_conf"]["port"]) != 0:
        return("["+exit_value+"] - Host unreachable %s:%s" % (httpgetstring["http_conf"]["host"],httpgetstring["http_conf"]["port"]),exit_code)

    #Get the website
    urlParse = ("%s://%s:%i%s" % (httpgetstring["http_conf"]["protocol"],httpgetstring["http_conf"]["host"],httpgetstring["http_conf"]["port"],httpgetstring["http_conf"]["context"]))
    _dataresponse = urllib.urlopen(urlParse, data=None)
    if _dataresponse.getcode() is not httpgetstring["http_conf"]["code"]:
        return("["+exit_value+"] - The response code isn't valid: %i" % (_dataresponse.getcode()),exit_code)
    
    #Verify the strings
    if "http_string" in httpgetstring:
        for _iterator in range(len(httpgetstring["http_string"])):
            if isinstance(httpgetstring["http_string"][_iterator], str) is False:
                return("[CRITICAL] - The defined strings aren't correct, please check "+config_path,2)

        vardata = _dataresponse.read()
        for _iterator2 in range(len(httpgetstring["http_string"])):
            if httpgetstring["http_string"][_iterator2].encode() not in vardata:
                return("["+exit_value+"] - The defined string %s wasn't found in the website %s" % (httpgetstring["http_string"][_iterator2],urlParse),exit_code)

    #The correct exit
    return("[OK] - The website: %s was verified" % (urlParse),0)