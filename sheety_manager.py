"""The Google sheet database has one sheet named <passwords> and as column headers
<website>, <username>, <password> and <updated>"""

import os
import requests
from dotenv import load_dotenv
import datetime as dt

load_dotenv()

# Go to sheety.co to create a project, link your Google sheet and get an ENDPOINT and a TOKEN or an AUTHORIZATION
SHEETY_ENDPOINT = os.getenv("SHEETY_ENDPOINT")  # ENDPOINT from sheety.co
SHEETY_AUTHORIZATION = os.getenv("SHEETY_AUTHORIZATION")  # AUTHORIZATION from sheety.co


class Sheety:  # This class object is responsible for communicating with the Google sheet using sheety API

    def __init__(self):  # initiate a sheety object
        self.endpoint = SHEETY_ENDPOINT
        self.authorization = SHEETY_AUTHORIZATION
        self.headers = {"Authorization": self.authorization}

    def new_post(self, website, username, password):
        """take new data and insert them on a new line on the Google sheet project and return a
        status_code"""

        # set sheety parameters for the new post
        now = dt.datetime.now()
        sheety_params = {
            "password": {
                "website": website.lower(),
                "username": username,
                "password": password,
                "updated": now.strftime("%x") + " " + now.strftime("%X")
            }
        }

        # send the new post
        new_post = requests.post(url=self.endpoint, json=sheety_params, headers=self.headers)
        return new_post.status_code  # return a status code (200 if success)

    def get_data(self, website):
        """take a website and fetch it from the sheet and return a json data"""

        get_endpoint = f"{self.endpoint}?filter[website]={website.lower()}"

        # send a get request
        new_get = requests.get(url=get_endpoint, headers=self.headers)
        return new_get.json()['passwords']  # return a json data

    def put_data(self, website, username, password, data_id):
        """take a website id and modify the correspondant line on the sheet"""

        put_endpoint = f"{self.endpoint}/{data_id}"

        # set sheety parameters for the new post
        now = dt.datetime.now()
        sheety_params = {
            "password": {
                "website": website.lower(),
                "username": username,
                "password": password,
                "updated": now.strftime("%x") + " " + now.strftime("%X")
            }
        }

        # send a put request
        new_put = requests.put(url=put_endpoint, json=sheety_params, headers=self.headers)
        return new_put.status_code  # return a status code (200 if successful)

