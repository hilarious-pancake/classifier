#!/usr/bin/env python

import flickrapi, nltk, re, urllib2, os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

api_key = u'bd357bbf22b783cd194d9585e495e0a4'
api_secret = u'8be92d6e6304428a'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

# open_file('recycle.txt')

def open_file(filename):
  # read file line by line into a list
  with open(filename) as f:
    items = f.readlines()

  # remove newline characters from list items
  items = [x.strip('\n') for x in items]

  for item in items:
    # search for query
    search_flickr(item)

def search_flickr(query):
  # grab photo urls from flickr
  photos = flickr.photos.search(text=query, sort='relevance')

  photo_urls = []

  # parse photo data
  for i in range(0, 10):
    attributes = photos[0][i].attrib
    photo_urls.append('https://farm' + attributes['farm'] +
      '.staticflickr.com/' + attributes['server'] + '/' +
      attributes['id'] + '_' + attributes['secret'] + '_m.jpg')

  return photo_urls

  # input urls into cloudsight api

  # wait

  # copy resulting description into links