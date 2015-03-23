#!/usr/bin/env python

import flickrapi, unirest, time

# connect to flickr api
api_key = u'key'
api_secret = u'secret'

flickr = flickrapi.FlickrAPI(api_key, api_secret)

def open_file(filename):
  # read file line by line into a list
  with open(filename) as f:
    items = f.readlines()

  # remove newline characters from list items
  items = [x.strip('\n') for x in items]

  for item in items:
    print item
    # search for query
    search_flickr(item)

def search_flickr(query):
  # grab photo urls from flickr
  photos = flickr.photos.search(text=query, sort='relevance')

  # initialize empty array to hold photo urls
  photo_urls = []

  # add first four photo urls to array
  for i in range(0, 5):
    attributes = photos[0][i].attrib
    photo_urls.append('https://farm' + attributes['farm'] +
      '.staticflickr.com/' + attributes['server'] + '/' +
      attributes['id'] + '_' + attributes['secret'] + '_m.jpg')

  # read each image in array
  for url in photo_urls:
    read_image(url)

def read_image(photo_url):
  # post photo url to camfind api
  post_res = unirest.post("https://camfind.p.mashape.com/image_requests",
    headers = {
      "X-Mashape-Key": "key",
      "Content-Type": "application/x-www-form-urlencoded",
      "Accept": "application/json"
    },
    params = {
      "image_request[locale]": "en_US",
      "image_request[remote_image_url]": photo_url
    }
  )
  
  # retrieve description for url
  return get_description(post_res.body['token'])

def check_res(token):
  time.sleep(20)
  
  response = unirest.get("https://camfind.p.mashape.com/image_responses/" + token,
    headers = {
      "X-Mashape-Key": "key",
      "Accept": "application/json"
    }
  )
 
  return response

def get_description(token):
  # it takes camfind up to 20s to return a result, so delay retrieval by 20s
  time.sleep(20)
  
  # retrieve description
  description = check_res(token)

  # if description is unfinished, check the result again
  if not description.body.has_key('name'):
    description = check_res(token)

  print description.body

  # if description was skipped, return 'skipped'
  if description.body.has_key('reason'):
    return 'skipped'
  # else save the description 
  else:
    return save_description(description.body['name'])

def save_description(desc):
  # write descriptions to a specified file
  with open('compost-desc.txt', 'a') as f:
    f.write(desc + '\n')