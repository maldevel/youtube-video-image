#!/usr/bin/python
# encoding: UTF-8

import os
import urllib
import urllib2
from bs4 import BeautifulSoup
import argparse
from argparse import RawTextHelpFormatter
import sys

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Download youtube video cover image.",                                 
                                     formatter_class=RawTextHelpFormatter)
    
    parser.add_argument("-u", '--url', action="store", metavar='URL', dest='url', 
                        default=None, help="Youtube URL")
    
    args = parser.parse_args()
    
    if len(sys.argv) is 1:
        parser.print_help()
        sys.exit()

    if not args.url:
        print(red("[-] Please specify a youtube url."))
        sys.exit(2)
    
    html = urllib2.urlopen(args.url)
    soup = BeautifulSoup(html, "lxml")

    imgs = soup.findAll("meta", {"property":"og:image"})
    
    for img in imgs:
        filename = img['content'].replace(":", "").replace("/", "_")
        urllib.urlretrieve(img['content'], filename)
        print 'Image for video {} downloaded.\n'.format(img['content'])
        
        
