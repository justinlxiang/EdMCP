import os
from edapi import EdAPI

class EdClient:
    def __init__(self):
        self.api = EdAPI()
        # Try to load token from file
        try:
            with open(".env", "r") as f:
                self.api.api_token = f.read().strip()
        except FileNotFoundError:
            self.api.api_token = None

    def get_threads(self, course_id, limit=20):
        return self.api.list_threads(course_id, limit=limit)

    def get_thread(self, thread_id):
        return self.api.get_thread(thread_id)

    def post_thread(self, course_id, title, content, category):
        params = {
            "type": "post",
            "title": title,
            "category": category,
            "subcategory": "",
            "subsubcategory": "",
            "content": content,
            "is_pinned": False,
            "is_private": False,
            "is_anonymous": False,
            "is_megathread": False,
            "anonymous_comments": False
        }
        return self.api.post_thread(course_id, params)

    def get_user_info(self):
        return self.api.get_user_info()

    def list_user_activity(self, user_id, course_id, limit=10, filter="all"):
        return self.api.list_user_activity(user_id, course_id, limit=limit, filter=filter)

    def upload_file(self, filename, content_type):
        with open(filename, "rb") as f:
            file_bytes = f.read()
        return self.api.upload_file(filename, file_bytes, content_type)

    def set_api_token(self, token):
        self.api.api_token = token
        with open(".env", "w") as f:
            f.write(f"ED_API_TOKEN={token}")
