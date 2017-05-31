import scrapy
from MySpider.items import GewaraFilmScreenings
from MySpider.items import GewaraFilm

class NuomiSpider(scrapy.Spider):
    name = 'nuomi'
    start_urls = []

