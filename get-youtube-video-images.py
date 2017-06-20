#!/usr/bin/env python
# -*- coding: utf-8 -*-

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import sys
import hashlib
import argparse
import requests
from bs4 import BeautifulSoup
from argparse import RawTextHelpFormatter


video_url = 'https://www.youtube.com/watch?v={}'
thumbnail_url = 'https://i.ytimg.com/vi/{}/maxresdefault.jpg'
empty_thumbnail_md5digest = 'e2ddfee11ae7edcae257da47f3a78a70'


def parse_args():
    parser = argparse.ArgumentParser(description="Download YouTube video cover image.",
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument("-i", '--id', action="store", metavar='YouTubeID', dest='ytid',
                        default=None, help="YouTube Video ID")
    parser.add_argument("-r", '--related', action="store_true", dest='related',
                        default=False, help="Download thumbnails from related videos as well")
    #parser.add_argument("-d", '--depth', action="store", metavar='Depth', dest='depth',
    #                    default=None, help="Crawl Depth")

    args = parser.parse_args()

    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    #if not args.ytid:
    #    print(red('[-] Please specify a YouTube URL'))
    #    sys.exit(2)

    return args


def download_thumbnail(ytid):
    resp = requests.get(thumbnail_url.format(ytid), stream=True)
    raw_resp = resp.raw.read()
    md5digest = hashlib.md5(raw_resp).hexdigest()

    if md5digest == empty_thumbnail_md5digest:
        print '[*] Empty thumbnail ({})'.format(ytid)
        return

    if md5digest in downloaded_thumbs:
        print '[*] Thumbnail already downloaded ({})'.format(ytid)
        return

    downloaded_thumbs.append(md5digest)
    print '[*] Downloading {}...'.format(ytid)
    with open('{}.png'.format(ytid), 'wb') as thumbnail:
        thumbnail.write(raw_resp)


def find_related(ytid):
    html = requests.get(video_url.format(ytid)).content
    soup = BeautifulSoup(html, 'lxml')
    related = list(set(re.findall('data\-thumb="https://i\.ytimg\.com/vi/([a-zA-Z0-9\-_]{5,20})/hqdefault\.jpg', html)))
    return related


def main():
    args = parse_args()
    global downloaded_thumbs
    downloaded_thumbs = []
    download_thumbnail(args.ytid)
    if args.related:
        related = find_related(args.ytid)
        for r in related:
            download_thumbnail(r)


if __name__ == '__main__':
    main()

