from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

def Create_Service(service_account_info, api_name, api_version, *scopes):
    print(api_name, api_version, scopes, sep='-')
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    credentials = service_account.Credentials.from_service_account_info(
        service_account_info, scopes=SCOPES)

    service = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)
    print(API_SERVICE_NAME, 'service created successfully')
    return service

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
