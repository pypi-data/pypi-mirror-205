"""
Copyright (c) 2023, Koen Martens <kmartens@sonologic.se>

Licensed under a hippocratic license. License terms can be found in
LICENSE.md or online:

https://firstdonoharm.dev/version/3/0/bds-cl-eco-extr-ffd-media-my-soc-sv-tal-xuar.md

"""
import os
from pathlib import Path

import toml

from tootstagram.database import Database
from tootstagram.instagram import InstagramClient
from tootstagram.mastodon import MastodonClient

CONFIG_FILENAME = 'tootstagram.toml'


def config_finder() -> str:
    user_dir = Path.home()
    if os.path.isfile(os.path.join(user_dir, CONFIG_FILENAME)):
        return os.path.join(user_dir, CONFIG_FILENAME)
    if os.path.isfile(os.path.join(user_dir, '.tootstagram', CONFIG_FILENAME)):
        return os.path.join(user_dir, '.tootstagram', CONFIG_FILENAME)
    if os.path.isfile(os.path.join(os.getcwd(), CONFIG_FILENAME)):
        return os.path.join(os.getcwd(), CONFIG_FILENAME)


def main() -> None:
    config = toml.load(config_finder())
    database = Database()
    mastodon_client = MastodonClient(config['mastodon']['account'], database)
    instagram_client = InstagramClient(config['instagram']['username'], config['instagram']['password'])
    to_post = mastodon_client.get_images()
    for toot in to_post:
        for media in toot.media:
            instagram_client.post_image(media.url, toot.description, media.alt_text)
            database.add_processed(toot.id, media.url)
