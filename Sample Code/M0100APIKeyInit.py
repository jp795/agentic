import os
import sys
import configparser

class APIKeyInitializer:
    """
    A Open AI key initializer for handling API key operations.
    This class stores the API key in the OS environment variable.
    """

    def __init__(self, api_key=" ", default_section='DEFAULT', config_file_name='pyvenv.cfg', config_key_name='OPENAI_API_KEY', os_var_name='OPENAI_API_KEY'):
        
        # cfg_path = os.path.join(os.getcwd(), config_file_name) 
        cfg_path = os.path.join(sys.prefix, config_file_name)
        print(f"Reading configuration from: {cfg_path}")
        config = configparser.ConfigParser()
        with open(cfg_path, 'r') as cfg_file:
            configContent = '[DEFAULT]\n' + cfg_file.read()
        config.read_string(configContent)
        openai_api_key = config.get('DEFAULT', 'OPENAI_API_KEY')
        print(f"OPENAI_API_KEY: {openai_api_key}")
        os.environ['OPENAI_API_KEY'] = openai_api_key
        print(f"API key has been set in the environment variable: {os_var_name}")

