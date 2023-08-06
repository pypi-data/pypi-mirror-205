"""
Copyright (c) 2023, Koen Martens <kmartens@sonologic.se>

Licensed under a hippocratic license. License terms can be found in
LICENSE.md or online:

https://firstdonoharm.dev/version/3/0/bds-cl-eco-extr-ffd-media-my-soc-sv-tal-xuar.md

"""
import os
from tempfile import TemporaryDirectory

import instagrapi

from tootstagram.utils import download_file


class InstagramClient:
    def __init__(self, username: str, password: str) -> None:
        self._client = instagrapi.Client()
        self._client.login(username, password)

    def post_image(self, image_url: str, description: str, alt_text: str) -> None:
        extra_data = {}
        if alt_text:
            extra_data['custom_accessibility_caption'] = alt_text

        extension = os.path.splitext(os.path.basename(image_url))[1][1:]
        with TemporaryDirectory() as temp_dir:
            image_path = os.path.join(temp_dir, f'image.{extension}')
            download_file(image_url, image_path)
            self._client.photo_upload(
                image_path,
                description,
                extra_data=extra_data
            )

