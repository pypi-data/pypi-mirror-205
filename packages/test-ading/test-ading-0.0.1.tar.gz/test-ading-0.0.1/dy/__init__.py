# encoding: utf-8
# @time :  2023-04-29 16:58:00
# @file : __init__.py.py
# @author : Ading
# Official Account: AdingBLOG
import requests


class DouyinAPI:
    def __init__(self, client_key, client_secret, redirect_uri):
        self.client_key = client_key
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    def get_authorize_url(self, state):
        authorize_url = "https://open.douyin.com/platform/oauth/connect/?client_key={client_key}&response_type=code&scope={scope}&redirect_uri={redirect_uri}&state={state}".format(
            client_key=self.client_key,
            scope="aweme.post,aweme.comment",
            redirect_uri=self.redirect_uri,
            state=state
        )

        return authorize_url

    def get_access_token(self, code):
        access_token_url = "https://open.douyin.com/oauth/access_token/"

        payload = {
            "client_key": self.client_key,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": self.redirect_uri
        }

        response = requests.post(access_token_url, data=payload)

        if response.status_code == 200:
            return response.json()["access_token"]
        else:
            raise Exception("Failed to get access token.")
