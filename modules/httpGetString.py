# Module: httpGetString
# Author: rdcarrera
# Version: 0.1
# Require:
#       Module - portOpen
#       Config - template httpGetString
# Check petition to a http server and validate a string

#def httpGetString()

# Import of the requirenments
import sys
import yaml
import urllib
from portOpen import PortOpen

def ReturnValue(msg, result = "OK" ):
    print ("%s - %s" % (result,msg))
    sys.exit(2)

# Import of the configuration files
config_path = "../templates/httpGetString.yml"
with open(config_path, 'r') as yaml_stream:
    try:
        httpgetstring = yaml.load(yaml_stream)
    except yaml.YAMLError as exc:
        print(exc)


# Verification of the parameters
if isinstance(httpgetstring["module"], str) is False or  \
   httpgetstring["module"] != "httpGetString":
       ReturnValue("El fichero de configuracio no corresponde con el template")

if isinstance(httpgetstring["conf"]["host"], str) is False:
    ReturnValue("No esta correctamente definido la variable host","critical")

if isinstance(httpgetstring["conf"]["port"], int) is False:
    ReturnValue("No esta correctamente definido el puerto","critical")

if len(httpgetstring["conf"]["string"]) is 0:
    ReturnValue("No se ha definido ningun string de chequeo","critical")

if isinstance(httpgetstring["conf"]["code"], int) is False:
    ReturnValue("No esta correctamente definido el codigo de respuesta","critical")

for _iterator in range(len(httpgetstring["conf"]["string"])):
    if isinstance(httpgetstring["conf"]["string"][_iterator], str) is False:
            ReturnValue("El string definido no es correcto","critical")


#Check comunication with the services
if PortOpen(httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]) != 0:
    ReturnValue("Imposible comunicar con %s:%s" % (httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]),"critical")

# Capturar la web
urlParse = ("%s://%s:%i%s" % (httpgetstring["conf"]["protocol"],httpgetstring["conf"]["host"],httpgetstring["conf"]["port"],httpgetstring["conf"]["context"]))
_dataresponse = urllib.urlopen(urlParse, data=None)
if _dataresponse.getcode() is not httpgetstring["conf"]["code"]:
    ReturnValue("El codigo de respuesta es invalido %i" % (_dataresponse.getcode()),"critical")
vardata = _dataresponse.read()
for _iterator2 in range(len(httpgetstring["conf"]["string"])):
    if httpgetstring["conf"]["string"][_iterator2] not in vardata:
        ReturnValue("No se ha encontrado el string %s en la web solicitada" % (httpgetstring["conf"]["string"][_iterator2]),"critical")
