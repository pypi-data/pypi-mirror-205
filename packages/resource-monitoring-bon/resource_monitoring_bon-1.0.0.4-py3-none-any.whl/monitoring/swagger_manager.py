import jwt
from pydantic import BaseModel
from keycloak import KeycloakOpenID
import requests
import os

import json
from typing import Optional
import winreg

class Study(BaseModel):
    id: str
    status: Optional[str]
    isSupported: bool
    isAnon: bool
    patientId: str
    patientName: str
    patientSex: str
    patientAge: str
    birthDate: str
    studyDate: str
    studyDescription: str
    accessionNumber: str
    modality: str
    bodyPart: str
    requestedProcedureDescription: str
    deviceNames: list
    numberOfSeries: int
    numberOfInstances: int
    createdAt: str

class Token(BaseModel):
    licenseId: str
    realm: str
    hospitalName: str
    paconSecret: str
    isDemo:str
    isResearch:str
    deployType: str
    region: str
    country: str
    reconUrl: str
    authUrl: str
    collectorUrl: str
    collectorSecret: str
    alertChannelUrl: str
    connectorServer: str
    connectorPort: str
    activated: str
    deactivationPeriod: str
    deactivatedAt: Optional[str]
    exp: str
    iat: str

def get_license_token() -> Token:
    try:
        # set the registry key path and value name
        key_path = r'SOFTWARE\SwiftMR Pacon Launcher'
        value_name = 'LicenseAccessToken'

        # open the registry key for reading
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, key_path)

        # get the value of the registry key
        token = winreg.QueryValueEx(key, value_name)[0]

        decoded_token = jwt.decode(token, options={"verify_signature": False})

        # close the registry key
        winreg.CloseKey(key)
    except:
        token = os.getenv('LICENSE_ACCESS_TOKEN')

        decoded_token = jwt.decode(token, options={"verify_signature": False})
    
    return decoded_token


class UserKeyCloak:
    keycloak_openid: any
    token: str
    access_token: str

    def __init__(self, license_token: Token):
        try:
            self.keycloak_openid = KeycloakOpenID(server_url=license_token.authUrl + "/auth/",
                                client_id="swiftmr-client",
                                realm_name=license_token.realm)
            self.token = self.keycloak_openid.token("pq", "Code123$")
            self.access_token = self.token['access_token']
        except Exception as e:
            print("Check User Config")
            print(e)
            exit(0)

    def logout(self):
        self.keycloak_openid.logout(self.token['refresh_token'])

def _get(url: str, access_token):
    return requests.get(url,
                        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(access_token)})

def _post(url: str, data, access_token: str):
    return requests.post(url,
                        data=json.dumps(data),
                        headers={'Content-Type': 'application/json', 'Authorization': 'Bearer {}'.format(access_token)})

def get_device_list(licenseToken: Token, access_token: str):
    url = 'http://localhost:5000/pacon/{}/api/v2/settings/devices'.format(licenseToken.realm)
    return _get(url, access_token)

def swagger_get_study(licenseToken: Token, access_token: str):
    url = "http://localhost:5000/pacon/{}/api/v2/studies?limit=500".format(licenseToken.realm)

    study_res = _get(url, access_token)
    
    study_info = []
    
    for num_study in range(len(study_res.json())):
        study = Study(**study_res.json()[num_study])

        if study.status == 'InProgress' or study.status == None:
            study_info.append(study)
    
    return sorted(study_info, key=lambda x: x.createdAt, reverse=False)

def get_study_info():
    license_token = Token(**get_license_token())
    
    user_keycloak = UserKeyCloak(license_token)

    study_info = swagger_get_study(license_token, user_keycloak.access_token)
    
    user_keycloak.logout()
    
    return study_info

def post_select_device():
    license_token = Token(**get_license_token())
    
    user_keycloak = UserKeyCloak(license_token)

    url = 'http://localhost:5000/pacon/{}/api/v2/settings/devices:select'.format(license_token.realm)
    
    device_list = []

    # get device id list
    for device in get_device_list(license_token, user_keycloak.access_token).json():
        device_list.append(device['id'])
    
    device_dict = {"deviceIds": device_list}

    select_res = _post(url, device_dict, user_keycloak.access_token)    

    user_keycloak.logout()

if __name__ == "__main__":
    get_study_info()