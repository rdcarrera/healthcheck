# Module: MysqlSelect
# Author: rdcarrera
# Version: 0.1
# Require:
#       Extras - PortOpen, CheckConfig
#       Config - template MysqlSelect
# Check petition to a http server and validate a string

# Import of the requirenments
import yaml
import os.path
import modules.HealthCheck.PortOpen as PortOpen
import modules.HealthCheck.CheckConfig as CheckConfig
import modules.HealthCheck.ResolvName as ResolvName
import platform
import mysql.connector
from mysql.connector import Error
# Import the config model from the template
from modules.MysqlSelect.MysqlSelectTemplate import config_template_require


def main ( config_path = "examples/checks/LocalMysql.yml" ):
    # Import of the configuration files
    if os.path.isfile(config_path) is False:
        return("[CRITICAL] - The config file doesn't exist, please check "+config_path,2)

    with open(config_path, 'r') as yaml_stream:
        try:
            mysqlSelect = yaml.safe_load(yaml_stream)
        except yaml.YAMLError as exc:
            print(exc)

    #Verifiy the configuration
    return_check_config = CheckConfig.main(config_template_require,mysqlSelect,config_path)
    if return_check_config is not None:
      return return_check_config


    #Confirm the module name
    if mysqlSelect["module"] != "MysqlSelect":
        return("[CRITICAL] - The config file doesn't correspont with the module, please check "+config_path,2)

    #Set the exit values
    if isinstance(mysqlSelect["conf"]["anomaly_exit"], int) is False:
        exit_code = 1
        exit_value="WARNING"
    else:
        exit_code = mysqlSelect["conf"]["anomaly_exit"]
        if exit_code == 0:
            exit_value="OK"
        elif exit_code == 1:
            exit_value="WARNING"
        elif exit_code == 2:
            exit_value="CRITICAL"
        else:
            exit_value="UNKNOWN"

    #Check comunication with the services
    if ResolvName.main(mysqlSelect["mysql_conf"]["host"]) == False:
        return("["+exit_value+"] - Can't resolve dns %s" % (mysqlSelect["mysql_conf"]["host"]),exit_code)
    if PortOpen.main(mysqlSelect["mysql_conf"]["host"],mysqlSelect["mysql_conf"]["port"]) != 0:
        return("["+exit_value+"] - Database unreachable %s:%s" % (mysqlSelect["mysql_conf"]["host"],mysqlSelect["mysql_conf"]["port"]),exit_code)

    # connect to the mysql
    try:
        mysql_connection = mysql.connector.connect(**mysqlSelect["mysql_conf"])
        if mysql_connection.is_connected():
            if "mysql_table" in mysqlSelect:
                if "table" not in mysqlSelect["mysql_table"] or "conditional" not in mysqlSelect["mysql_table"]:
                    return("["+exit_value+"] - You doesn't have defined the table or conditional on mysql_table",exit_code)
                if isinstance(mysqlSelect["mysql_table"]["table"], str) is False:
                    return("["+exit_value+"] - The table definition isn't valid: %s",mysqlSelect["mysql_table"]["table"],exit_code)
                if isinstance(mysqlSelect["mysql_table"]["conditional"], str) is False:
                    return("["+exit_value+"] - The conditional definition isn't valid: %s",mysqlSelect["mysql_table"]["conditional"],exit_code)
                mysql_query = ("SELECT * FROM "+mysqlSelect["mysql_table"]["table"]+" "+mysqlSelect["mysql_table"]["conditional"]+";" )
            else:
                mysql_query = ("SELECT 1 + 1 FROM DUAL;")
            try:
                mysql_connection_cursor = mysql_connection.cursor()
                mysql_connection_cursor.execute(mysql_query)
            except:
                return("["+exit_value+"] - The proccess can't execute the query %s" % (mysql_query),exit_code)
            finally:
                if mysql_connection.is_connected():
                    mysql_connection_cursor.close()
                    mysql_connection.close()

    except Error as e:
        return("["+exit_value+"] - The proccess can't connect to %s port %s database %s" % (mysqlSelect["mysql_conf"]["host"],mysqlSelect["mysql_conf"]["port"],mysqlSelect["mysql_conf"]["database"]),exit_code)

    #The correct exit
    return("[OK] - The database: %s was verified" % (mysqlSelect["mysql_conf"]["database"]),0)
