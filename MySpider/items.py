# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class GewaraFilm(scrapy.Item):
    name = scrapy.Field()
    cinema = scrapy.Field()
    date = scrapy.Field()
    screenings = scrapy.Field()

class GewaraFilmScreenings(scrapy.Item):
    auditorium = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    language = scrapy.Field()

class NuomiFilm(scrapy.Item):
    name = scrapy.Field()
    cinema = scrapy.Field()
    date = scrapy.Field()
    screenings = scrapy.Field()

class NuomiFilmScreenings(scrapy.Item):
    auditorium = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    remain = scrapy.Field()

class MeituanFilm(scrapy.Item):
    name = scrapy.Field()
    cinema = scrapy.Field()
    date = scrapy.Field()
    screenings = scrapy.Field()

class MeituanFilmScreenings(scrapy.Item):
    auditorium = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()

