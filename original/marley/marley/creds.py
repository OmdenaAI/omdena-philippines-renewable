from pydrive.auth import GoogleAuth
import logging
import json
from configparser import ConfigParser
from os.path import expanduser
HOME = expanduser("~")

logging.getLogger("googleapiclient").setLevel(logging.ERROR)
logging.getLogger("oauth2client").setLevel(logging.ERROR)
logging.getLogger("google_auth_httplib2").setLevel(logging.ERROR)


def gdrive(force=False, credsfile=f"{HOME}/.gdrive.json"):
    """ return credentials for google drive

    onetime setup::
        pip install fs.googledrivefs
        enable google drive api
        create creds
            credentials/create oauth clientid
            select web application
            authorised javascript origins http://localhost:8080
            authorised redirect urls http://localhost:8080/ [NOTE THE / on the end]
            download client_secrets.json and move to ~/.gdrive.json

    Usage to open google drive using pyfilesystem::
        fs1 = fs.open_fs(f"googledrive://{gdrive()}")

    :param force: force reauthentication. needed if token expired or cancelled.
    :param credsfile: location of client_secrets.json downloaded from google
    :return: authorisation string for google drive
    """
    # get creds that are needed to obtain tokens
    creds = json.load(open(credsfile))
    web = creds["web"]
    client_id = web["client_id"]
    client_secret = web["client_secret"]

    # get tokens once per device and save in credsfile
    if force or "refresh_token" not in web:
        gauth = GoogleAuth()
        gauth.settings["client_config_file"] = credsfile
        gauth.settings["get_refresh_token"] = True
        gauth.LocalWebserverAuth()
        web["access_token"] = gauth.credentials.access_token
        web["refresh_token"] = gauth.credentials.refresh_token
        json.dump(creds, open(credsfile, "w"))
    access_token = web["access_token"]
    refresh_token = web["refresh_token"]

    return f"?client_id={client_id}&client_secret={client_secret}&" \
           f"access_token={access_token}&refresh_token={refresh_token}"

def aws(profile="default", credsfile=f"{HOME}/.aws/credentials"):
    """ return credentials for s3. this is not needed for the default profile.
    :param profile: section in .aws/credentials file
    :return: authorisation string for aws
    """
    cfg = ConfigParser()
    cfg.read(credsfile)
    try:
        key  = cfg.get(profile, "aws_access_key_id")
        secret = cfg.get(profile, "aws_secret_access_key")
    except:
        key = cfg.get("default", "aws_access_key_id")
        secret = cfg.get("default", "aws_secret_access_key")
    return f"{key}:{secret}"