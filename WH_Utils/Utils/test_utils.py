import os
from dotenv import load_dotenv
import requests

load_dotenv()

#setting up authentication for testing

WH_API_KEY = ''

WH_auth_dict = {
    "accept": "application/json",
    "Authorization": WH_API_KEY
}

login_header = {"accept":"application/json",
                "Content-Type":"application/x-www-form-urlencoded"}

login_data = {"username":"mcclain.thiel@berkeley.edu",
              "password":os.getenv("WH_ACCOUNT_PASSWORD")}

response = requests.post("https://db.wealthawk.com/login", headers = login_header, data = login_data)

key = response.json()['access_token']
access_token_string = "Bearer {}".format(key)

WH_auth_dict["Authorization"] = access_token_string

CS_API_KEY = 'Bearer ' + os.getenv("CORESIGNAL_API_KEY")
CS_auth_dict = {
    "accept": "application/json",
    "Authorization": CS_API_KEY
}

BASE_URL = "https://db.wealthawk.com"