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
from portOpen import PortOpen

def HttpGetString( config_path = "templates/httpGetString.yml" ):
    # Import of the configuration files
    with open(config_path, 'r') as yaml_stream:
        try:
            httpgetstring = yaml.load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)


    # Verification of the parameters
    if isinstance(httpgetstring["module"], str) is False or  \
       httpgetstring["module"] != "httpGetString":
           return("[CRITICAL] - El fichero de configuracio no corresponde con el template",2)

    if isinstance(httpgetstring["conf"]["host"], str) is False:
        return("[CRITICAL] - No esta correctamente definido la variable host",2)

    if isinstance(httpgetstring["conf"]["port"], int) is False:
        return("[CRITICAL] - No esta correctamente definido el puerto",2)

    if len(httpgetstring["conf"]["string"]) is 0:
        return("[CRITICAL] - No se ha definido ningun string de chequeo",2)

    if isinstance(httpgetstring["conf"]["code"], int) is False:
        return("[CRITICAL] - No esta correctamente definido el codigo de respuesta",2)

    for _iterator in range(len(httpgetstring["conf"]["string"])):
        if isinstance(httpgetstring["conf"]["string"][_iterator], str) is False:
                return("[CRITICAL] - El string definido no es correcto",2)


    #Check comunication with the services
    if PortOpen(httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]) != 0:
        return("[CRITICAL] - Imposible comunicar con %s:%s" % (httpgetstring["conf"]["host"],httpgetstring["conf"]["port"]),2)

    # Capturar la web
    urlParse = ("%s://%s:%i%s" % (httpgetstring["conf"]["protocol"],httpgetstring["conf"]["host"],httpgetstring["conf"]["port"],httpgetstring["conf"]["context"]))
    _dataresponse = urllib.urlopen(urlParse, data=None)
    if _dataresponse.getcode() is not httpgetstring["conf"]["code"]:
        return("[CRITICAL] - El codigo de respuesta es invalido %i" % (_dataresponse.getcode()),2)
    vardata = _dataresponse.read()
    for _iterator2 in range(len(httpgetstring["conf"]["string"])):
        if httpgetstring["conf"]["string"][_iterator2] not in vardata:
            return("[CRITICAL] - No se ha encontrado el string %s en la web solicitada" % (httpgetstring["conf"]["string"][_iterator2]),2)

    return("[OK] - Se ha verificado la direccion: %s" % (urlParse),0)
