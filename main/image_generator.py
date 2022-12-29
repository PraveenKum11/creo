import requests
import json
import cred
import random
import uuid
from PIL import Image


class Pexel:
    def __init__(self) -> None:
        self.url : str = "https://api.pexels.com/v1/search"
        self.headers : dict = {
            "Authorization" : cred.pexel_api
        }
        self.params : dict = {
            "query" : "nature",
            # "orientation" : ,
            # "size" : ,
            # "page" : ,
            # "per_page" : ,
        }
    
    def fetch_img(self) -> bytes:
        r = requests.get(url=self.url, headers=self.headers, params=self.params)
        parsed = json.loads(r.text)
        # print(json.dumps(parsed, indent = 4, sort_keys = True))

        img_quality = ["tiny", "large", "medium", "small", "portrait", "landscape", "original"]
        img_list = parsed["photos"]
        img_data = requests.get(img_list[random.randint(0, len(img_list) - 1)]["src"][img_quality[2]])
        
        return img_data.content


class Photo:
    def __init__(self) -> None:
        self.img : bytes = None
        self.img_name : str = str(uuid.uuid4()) + ".jpg"
        # self.path : str = f"../media/profile_pics/{self.img_name}"
        self.path : str = f"C:\\Users\\pkkp0\\Documents\\pydev\\web_dev\\blog_web\\media\\profile_pics\\{self.img_name}"

    def create_photo(self) -> str:
        img = Pexel()
        self.img = img.fetch_img()

        with open(self.path, "wb") as f:
            f.write(self.img)
        
        return self.path

