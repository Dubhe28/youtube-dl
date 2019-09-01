import json
from urllib.parse import urlparse, urlencode, parse_qs
from urllib.request import urlopen

import pandas as pd
import argparse
import os


class YoutubeCommentsDL:
    _YOUTUBE_COMMENT_URL = 'https://www.googleapis.com/youtube/v3/commentThreads'

    def __init__(self, api_key):
        self.api_key = api_key

    @staticmethod
    def _open_url(url, params):
        f = urlopen(url + '?' + urlencode(params))
        data = f.read()
        matches = data.decode("utf-8")
        f.close()
        return matches

    @staticmethod
    def _load_comment_info(comment):
        comment_snippet = comment["snippet"]
        comment_id = comment["id"]
        published_time = comment_snippet["publishedAt"]
        author = comment_snippet["authorDisplayName"]
        text = comment_snippet["textDisplay"]
        like_count = comment_snippet["likeCount"]
        return [comment_id, published_time, author, text, like_count]

    def _load_comments(self, mat, comments):
        for item in mat["items"]:
            comment = item["snippet"]["topLevelComment"]
            comments.append(self._load_comment_info(comment))
            if 'replies' in item.keys():
                for reply in item['replies']['comments']:
                    comments.append(self._load_comment_info(reply))

    def get_video_comment(self, video_id, max_page=True):
        max_res = 100
        params = {
            'part': 'snippet,replies',
            'maxResults': max_res,
            'videoId': video_id,
            'textFormat': 'plainText',
            'key': self.api_key
        }

        comments = []

        try:
            matches = self._open_url(self._YOUTUBE_COMMENT_URL, params)
            mat = json.loads(matches)
            i = 1
            self._load_comments(mat, comments)
            next_page_token = mat.get("nextPageToken")

            while next_page_token and max_page:
                params.update({'pageToken': next_page_token})
                matches = self._open_url(self._YOUTUBE_COMMENT_URL, params)
                mat = json.loads(matches)
                i += 1
                self._load_comments(mat, comments)
                next_page_token = mat.get("nextPageToken")
                if max_page is not True:
                    max_page -= 1

        except KeyboardInterrupt:
            print("User Aborted the Operation")

        except:
            print("Cannot Open URL or Fetch comments at a moment")

        cols = ['comment_id', 'published_time', 'author', 'text', 'like_count']
        df = pd.DataFrame(comments, columns=cols)
        return df


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--video_url', required=True)
    parser.add_argument('-k', '--youtube_api_key', required=False)
    parser.add_argument('-m', '--max_page', default="50")
    args = parser.parse_args()

    if len(args.video_url) == 11:  # if the argument input was video_id
        vid = args.video_url
    else:
        vid = get_video_id(dequote(args.video_url))

    if args.youtube_api_key:
        api_key = dequote(args.youtube_api_key)
    else:
        try:
            with open('youtube_api_key.txt', 'r') as f:
                api_key = f.read()
            if "[YOUR_API_KEY]" in api_key:
                raise ValueError
        except:
            print("ERROR: Please give a Youtube API key in a text file ('youtube_api_key.txt') or as an argument [-k]")
            exit()

    max_page = int(dequote(args.max_page))

    if not os.path.exists("../video_comments"):
        os.makedirs("../video_comments")
        print("Created a directory named 'video_comments' in the parent folder.")

    df = YoutubeCommentsDL(api_key).get_video_comment(vid, max_page)

    comments_filename = '../video_comments/' + vid + '.csv'
    df.to_csv(comments_filename, mode="w", index=False, encoding="utf-8-sig")


def dequote(s):
    # If a string has single or double quotes around it, remove them.
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s


def get_video_id(url_string):
    parts = urlparse(url_string)
    query = parse_qs(parts.query)
    return query["v"][0]


if __name__ == "__main__":
    main()
