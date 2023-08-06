# openid.py


import requests
import os

class OpenId():
    def __init__(self, username, password) -> None:
        self.host = os.getenv("IAM_URI")
        self.username = username
        self.password = password
        self.access_token = None
        self.member_of = None
        self.workspace = None
        self.workspace_id = None
                
        self.refresh_user_info()


    def is_authenticated(self):
        return self.access_token != None


    def get_url(self, endpoint) -> str:
        return self.host + endpoint
    

    def build_header(self, headers):
        headers["Authorization"] = f"Bearer {self.access_token}"
        return headers
    

    def get_workspace(self):
        return self.workspace


    def get_token(self) -> None:
        endpoint = "/realms/dhuodata/protocol/openid-connect/token"
    
        headers = {}        
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        
        payload = {}
        payload["client_id"] = "admin-cli"
        payload["grant_type"] = "password"
        payload["username"] = self.username
        payload["password"] = self.password
        payload["scope"] = "openid"
                
        response = requests.request("POST", self.get_url(endpoint), headers=headers, data=payload)

        data = response.json()

        if "access_token" in data:
           self.access_token = data["access_token"]


    def refresh_user_info(self):
        """refresh_user_info"""
        
        self.get_token()
        if not self.is_authenticated():
            return

        endpoint = "/realms/dhuodata/protocol/openid-connect/userinfo"

        headers = {}        
        headers = self.build_header(headers)

        response = requests.get(self.get_url(endpoint), headers=headers)
        data = response.json()

        self.member_of = data["memberOf"]

        SEP = "/wks_"

        print("****** tirar o 9 *****")
        self.workspace = list((word for word in self.member_of if SEP+"9" in word))
        
        if self.workspace:
            self.workspace = self.workspace[0].split(SEP)[1]


if __name__ == "__main__":

    username = "antonioclj.ac@gmail.com"
    password = "Pwd@9051"
       
    openid = OpenId(username, password)
    if openid.is_authenticated():
        print("workspace -> " + openid.workspace)
        print("access token -> " + openid.access_token)
    else:
        print("Não autenticado")

