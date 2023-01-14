import requests
import json
import random
import uuid
import os
from PIL import Image

from django.conf import settings
class Pexel:
    def __init__(self, query) -> None:
        self.url : str = "https://api.pexels.com/v1/search"
        self.headers : dict = {
            "Authorization" : os.getenv("pexel_api")
        }
        self.params : dict = {
            "query" : query,
            "orientation" : "portrait",
            # "size" : ,
            # "page" : ,
            # "per_page" : ,
        }
    
    def fetch_img(self, img_quality="large") -> bytes:
        """
        img_quality = ["tiny", "large", "medium", "small", "portrait", "landscape", "original"]
        """
        r = requests.get(url=self.url, headers=self.headers, params=self.params)
        parsed = json.loads(r.text)
        # print(json.dumps(parsed, indent = 4, sort_keys = True))

        img_list = parsed["photos"]
        img_data = requests.get(img_list[random.randint(0, len(img_list) - 1)]["src"][img_quality])
        
        return img_data.content


class Photo:
    def __init__(self, type, query) -> None:
        self.img : bytes = None
        self.img_name : str = str(uuid.uuid4()) + ".jpg"
        self.type : str = type
        self.query : str = query
        if type == "Profile":
            self.path : str = os.path.join(settings.MEDIA_ROOT, "profile_pics", self.img_name)
        elif type == "Article":
            self.path : str = os.path.join(settings.MEDIA_ROOT, "article_img", self.img_name)

    def create_photo(self) -> str:
        img = Pexel(self.query)
        if self.type == "Profile":
            self.img = img.fetch_img("medium")
        elif self.type == "Article":
            self.img = img.fetch_img("large")

        with open(self.path, "wb") as f:
            f.write(self.img)
        
        return self.path

