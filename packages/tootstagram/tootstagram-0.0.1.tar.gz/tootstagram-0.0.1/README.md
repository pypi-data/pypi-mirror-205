# Tootstagram

https://cvs.sonologic.net/gmc/tootstagram

## Installation

```
pip install tootstagram
```

## Usage

Create a configuration file name `tootstragram.toml` based on the
example `tootstragram.toml.example` and place it in any of these
locations:

* In your home or user directory
* In a subdirectory `.tootstagram` under your home or user directory
* In the current working directory

The tool will search each of these locations in that order.

Then simply invoke the tool with:

```
tootstagram
```

This will fetch the feed from the Mastodon account and post any
images that were not already posted to the Instagram account.

## Limitations

* Only posts toots with images, not videos (I don't do videos myself)
* Any html tags in the toot are crudely removed by a simple regexp
* If a toot has multiple images, but not all have alt text, none of the
  instagram posts will have alt text (because it is impossible to derive
  from the feed which alt text belongs to which image)
* Editing a toot will not alter on or repost to instagram
* Only posts listed toots, as those are the only ones available from the
  feed
