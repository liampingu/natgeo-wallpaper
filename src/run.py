#!/usr/bin/python3


import requests, pickle

import comun
from ngdownloader import md5, download, set_background


# defines a place that photos and their metadata can be retreived
# has no indication of where and how they are retreived
class Source(object):
  def __init__(self, name, database):
    self.name = name
    self.database = database

  def index_all_pics(self):
    pass

# National Geographic Photo of the Day
# it has a json REST API
class NatGeo(Source):
  def __init__(self, database):
    Source.__init__(self, 'NatGeo', database)
    self.url = 'http://www.nationalgeographic.com/photography/photo-of-the-day/_jcr_content/.gallery.{year}-{month:02}.json'

  def index_all_pics(self):
    for year in range(2009, 2019):
      for month in range(1, 13):
        print('year={} month={}'.format(year, month))
        url = self.url.format(year=year, month=month)
        r = requests.get(url)
        if r.status_code == 200:
          data = r.json()
          if 'items' in data:
            for metadata in data['items']:
              url = metadata['url']
              if 'sizes' in metadata:
                url += metadata['sizes']['1600']
              self.database.append(Picture(
                metadata['title'],
                metadata['caption'],
                url,
                self,
                metadata['publishDate'],
              ))



class Picture(object):
  def __init__(self, name, description, url, source, date):
    self.name = name # string
    self.description = description # string
    self.url = url # string
    self.source = source # Source object
    self.date = date # string

  def to_str(self):
    return 'Picture({:15} - {:80})'.format(self.name[:15], self.description[:80])


def use_picture(pic):
  if download(pic.url) is True:
      set_background(comun.POTD)



if __name__ == '__main__':
  pic_list = []
  natgeo_source = NatGeo(pic_list)
  natgeo_source.index_all_pics()
  print('\n'.join(x.to_str() for x in pic_list))

  pickle.dump(pic_list, open('natgeo_pic_list', 'wb'))