"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

import datetime
import requests
import urllib


class VkError(Exception):
    pass


class Vk:

    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://api.vk.com/method/"

    def __str__(self):
        return "Vk v 0.1"

    def _call_method(self, method, **params):
        api_url = self.api_url + method + "?"
        access_token = {
            "access_token": self.access_token,
            "v": 5.62}
        params.update(access_token)

        r = requests.get(api_url, params=params)

        return self._json(r)

    def _json(self, r):
        r.raise_for_status()

        res = r.json()
        if "error" in res and "error_msg" in res["error"]:
            raise VkError("Ошибка выполнения запроса:\n\n"
                          "1. url: {}\n\n2. Ошибка: {}".
                          format(urllib.parse.unquote(r.url),
                                 res["error"]["error_msg"]))

        return res

    def _upload_image(self, owner_id, image_filename):
        params = dict()
        params['user_id'] = owner_id
        res = self._call_method("photos.getWallUploadServer", **params)

        files = {"photo": open(image_filename, "rb")}
        upload_url = res["response"]["upload_url"]
        r = requests.post(upload_url, files=files)
        res = self._json(r)

        res = self._call_method("photos.saveWallPhoto", **res)
        image_id = res["response"][0]["id"]

        return image_id

    def wall_post(self, owner_id, message,
                  location=None, image_filename=None, link=None):
        params = dict(owner_id=owner_id, message=message, attachments="")

        params["publish_date"] = \
            int((datetime.datetime.now() +
                datetime.timedelta(days=1)).timestamp())

        attachments = []
        if image_filename:
            line_image = "photo{owner_id}_{image_id}".format(
                owner_id=owner_id,
                image_id=self._upload_image(owner_id, image_filename))
            attachments.append(line_image)
        if link:
            attachments.append(link)

        params["attachments"] = ",".join(attachments)

        if location:
            params.update(location)

        post_id = self._call_method("wall.post", **params)

        return post_id["response"]['post_id']
