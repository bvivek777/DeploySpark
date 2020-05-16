from fabric import Connection;
import json;

class Connection_Manager :

    def __init__(self):
        with open('../config.json') as deployment_config :
            self.__config = json.load(deployment_config);
        
        super().__init__()