# persistence.py

import configparser
import os

from dhuolib.utils.utils import decode, encode


LOCAL_DHUO_CONFIG = ".dhuo"


class Persistence():
    
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.username = None
        self.password = None
        self.workspace = None
        self.project = None
        self.workspace_id = None
        self.experiment_id = None
        
        if not os.path.isfile(LOCAL_DHUO_CONFIG):
            self.init()


    def init(self ):
        data = {"default": 
                    {"username": "",
                     "password": "",
                     "project": "",
                     "workspace": "",
                     "workspace_id": "",
                     "experiment_id": "",
                     }
        }

        self.save(data)


    def save(self, data):
        self.config.read_dict(data)
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)


    def save_username(self, username):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["username"] = username
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)  


    def save_password(self, password):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["password"] = encode(password)
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)              


    def save_project(self, project):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["project"] = project
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)  


    def save_workspace(self, workspace):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["workspace"] = workspace
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)  


    def save_workspace_id(self, workspace_id):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["workspace_id"] = workspace_id
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)              


    def save_experiment_id(self, experiment_id):
        self.config.read(LOCAL_DHUO_CONFIG)
        self.config["default"]["experiment_id"] = experiment_id
        with open(LOCAL_DHUO_CONFIG, 'w') as configfile:
            self.config.write(configfile)  


    def get_username(self):
        dict = self.to_dict()
        return dict["default"]["username"]
    

    def get_password(self):
        dict = self.to_dict()
        return dict["default"]["password"]
    

    def get_workspace(self):
        dict = self.to_dict()
        return dict["default"]["workspace"]
    
    
    def get_workspace_id(self):
        dict = self.to_dict()
        return dict["default"]["workspace_id"]


    def get_project(self):
        dict = self.to_dict()
        return dict["default"]["project"]
    

    def get_experiment_id(self):
        dict = self.to_dict()
        return dict["default"]["experiment_id"]    
    

    def to_dict(self):
        self.config.read(LOCAL_DHUO_CONFIG)
        return  {
            "default": {
                "username": self.config["default"]["username"],
                "password": decode(self.config["default"]["password"]),
                "project": self.config["default"]["project"],
                "workspace": self.config["default"]["workspace"],
                "workspace_id": self.config["default"]["workspace_id"],
                "experiment_id": self.config["default"]["experiment_id"]
            }
        }
    
    
    def reset_and_get_credentials(self):
        self.save_experiment_id("")
        self.save_project("")
        self.save_workspace("")
        self.save_workspace_id("")

        return self.get_username(), self.get_password()


persistence = Persistence()


if __name__ == "__main__":
    
    persistence.save_username("antonioclj.ac@gmail.com")
    persistence.save_password("Pwd@9051")
    persistence.save_project("projeto-123")
    persistence.save_workspace("wks-abc")
    persistence.save_workspace_id("wks-123")
    persistence.save_experiment_id("exp-123")

    print(persistence.to_dict())
    print(persistence.get_username())
    print(persistence.get_password())
    print(persistence.get_project())
    print(persistence.get_workspace())
    print(persistence.get_workspace_id())
    print(persistence.get_experiment_id())
    
    print(persistence.reset_and_get_credentials())
