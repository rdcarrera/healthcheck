import six
def main (_config_template,_config_module,config_path):
    for key_name in _config_template.keys():
        if key_name not in _config_module:
            return("[CRITICAL] - The key name %s doesn't exist in the config file %s" %(key_name,config_path),2)
        if isinstance(_config_template[key_name], dict) == False:
            if isinstance(_config_module[key_name], type(_config_template[key_name])) is False:
                return("[CRITICAL] - The type object of %s must be %s" %(key_name,type(_config_template[key_name])),2)
        else:
            __config_template=_config_template[key_name]
            __config_module=_config_module[key_name]
            return_msg=main(__config_template,__config_module,config_path)
            if return_msg is not None:
                return return_msg