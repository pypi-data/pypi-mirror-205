# encoding: utf-8
# @time :  2023-04-29 17:00:00
# @file : openapi.py
# @author : Ading
# Official Account: AdingBLOG
import requests


class Video:
    def __init__(self, video_id, title, desc, create_time, cover):
        self.video_id = video_id
        self.title = title
        self.desc = desc
        self.create_time = create_time
        self.cover = cover


class Comment:
    def __init__(self, comment_id, aweme_id, create_time, text):
        self.comment_id = comment_id
        self.aweme_id = aweme_id
        self.create_time = create_time
        self.text = text


class DouyinOpenAPI:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_video_list(self, count=10, cursor=0):
        video_list_url = "https://open.douyin.com/video/list/"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "count": count,
            "cursor": cursor
        }

        response = requests.post(video_list_url, headers=headers, json=payload)

        if response.status_code == 200:
            video_list = []
            for video in response.json()["data"]:
                video_list.append(Video(
                    video_id=video["aweme_id"],
                    title=video["desc"],
                    desc=video["desc"],
                    create_time=video["create_time"],
                    cover=video["cover"]["url_list"][0]
                ))
            return video_list
        else:
            raise Exception("Failed to get video list.")

    def get_video_comment_list(self, video_id, count=10, cursor=0):
        video_comment_list_url = "https://open.douyin.com/video/comment/list/"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "aweme_id": video_id,
            "count": count,
            "cursor": cursor
        }

        response = requests.post(video_comment_list_url, headers=headers, json=payload)

        if response.status_code == 200:
            comment_list = []
            for comment in response.json()["data"]:
                comment_list.append(Comment(
                    comment_id=comment["cid"],
                    aweme_id=comment["aweme_id"],
                    create_time=comment["create_time"],
                    text=comment["text"]
                ))
            return comment_list
        else:
            raise Exception("Failed to get video comment list.")

    def post_video_comment_reply(self, video_id, comment_id, content):
        comment_reply_url = "https://open.douyin.com/video/comment/reply/"
        headers = {
            "Authorization": "Bearer " + self.access_token,
            "Content-Type": "application/json"
        }
        payload = {
            "aweme_id": video_id,
            "cid": comment_id,
            "content": content
        }

        response = requests.post(comment_reply_url, headers=headers, json=payload)

        if response.status_code == 200:
            return True
        else:
            return False
