from fabric import Connection, Config
import json
from prereq.Prereq import Prereq;

class Connection_Manager :

    def __init__(self, profile="dev"):        
        super().__init__()
        # Load the configuration information
        with open('./config.json') as deployment_config :
            config = json.load(deployment_config)
        self.slave_connections = []
        # create all the slave connections
        for s in config[profile]["slaves"] :
            self.slave_connections.append(
                Connection(
                    host = s["host"], # for test replace with the docker port using ifconfig
                    user = s["user"],
                    port = s["port"],
                    connect_kwargs = {
                        "password": s["sudo_pass"],
                        #TODO "pkey" : s["public_key"]
                    },
                    config = Config(
                        overrides={'sudo': {'password': s["sudo_pass"] }}
                    )
                )
            )
        
        # Create the master connection
        self.master_connection = Connection(
            host = config[profile]["master"]["host"], # for test replace with the docker port using ifconfig
            user = config[profile]["master"]["user"],
            port = config[profile]["master"]["port"],
            connect_kwargs = {
                "password": config[profile]["master"]["sudo_pass"],
                #TODO "pkey" : s["public_key"]
            },
            config = Config(
                overrides={'sudo': {'password': config[profile]["master"]["sudo_pass"] }}
            )
        )

    def start_deployment(self) :
        # install all the pre-requisites
        prereq = Prereq()
        prereq.install_prereqs(connection=self.master_connection)
        # for s in self.slave_connections :
        #     prereq.install_prereqs(s)
        