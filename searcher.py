#!/usr/bin/env python

import flickrapi, unirest, time, os

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

  for url in photo_urls:
    read_image(url)

def read_image(photo_url):
  post_res = unirest.post("https://camfind.p.mashape.com/image_requests",
    headers = {
      "X-Mashape-Key": "6qRcLmRhtpmshHUnKZhr35Tkpf4Ep18I4HbjsndLZjL7cUMrwt",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    params = {
      "focus[x]": "480",
      "focus[y]": "640",
      "image_request[altitude]": "27.912109375",
      "image_request[language]": "en",
      "image_request[latitude]": "35.8714220766008",
      "image_request[locale]": "en_US",
      "image_request[longitude]": "14.3583203002251",
      "image_request[remote_image_url]": photo_url
    }
  )
  
  return get_description(post_res.body['token'])

def check_res(token):
  time.sleep(20)
  
  response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
    headers = {
      "X-Mashape-Key": "6qRcLmRhtpmshHUnKZhr35Tkpf4Ep18I4HbjsndLZjL7cUMrwt",
      "Accept": "application/json"
    }
  )
 
  return response

def get_description(token):
  description = check_res(token)

  if description.body.has_key('name') == False:
    description = check_res(token)

  return description.body['name']