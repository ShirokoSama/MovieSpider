import scrapy
import time
from datetime import date
from MySpider.items import NuomiFilm
from MySpider.items import NuomiFilmScreenings

class NuomiSpider(scrapy.Spider):
    name = 'nuomi'
    start_urls = []
    cityId = '315'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def start_requests(self):
        prefix = 'https://dianying.nuomi.com/index'
        next_request = prefix + '?cityId=' + self.cityId
        return [scrapy.FormRequest(next_request, headers={'User-Agent': self.user_agent},
                                   callback=self.parse_movie)]

    def parse_movie(self, response):
        prefix = response.url
        flexslider = response.xpath('//div[@class="flexslider movielist"]//li')
        for index, li in enumerate(flexslider):
            movie_name = li.xpath('.//p[@class="text font14"]/text()').extract_first()
            movie_id_map = li.xpath('.//a[@class="detail"]//@data-data | .//a[@class="buy"]//@data-data').extract_first()
            movie_id = movie_id_map.split(':')[-1][0:-1]
            next_request = prefix.replace('index','movie/cinema') + '&movieId=' + movie_id + '&pagelets[]=pageletCinema'
            yield scrapy.Request(next_request, callback=self.parse_date,
                                 meta={'name': movie_name})

    def parse_date(self, response):
        prefix = response.url
        date_list = response.xpath('//ul[@id=\'\\"dateList\\"\']//li')
        for index, li in enumerate(date_list):
            date_ticks = li.xpath('.//@data-id').extract_first()
            date_ticks = date_ticks.replace('\\"','')
            date_str = li.xpath('.//span/text()').extract_first()
            date_str = self.date_format(date_str)
            time_ticks = str(int(time.time()*1000))
            next_request = prefix + '&date=' + date_ticks + '&t=' + time_ticks
            yield scrapy.Request(next_request, callback=self.parse_cinema
                                 ,meta={'name': response.meta['name'], 'date': date_str, 'date_ticks': date_ticks})

    def parse_cinema(self, response):
        prefix = response.url
        cinema_list = response.xpath('//li[@class=\'\\"clearfix\\"\']')
        for index, li in enumerate(cinema_list):
            cinema_id = li.xpath('.//p[@class=\'\\"title\\"\']/@data-data').extract_first()
            cinema_id = cinema_id[cinema_id.find(':')+1:cinema_id.find('}')]
            cinema_name = li.xpath('.//p[@class=\'\\"title\\"\']/span/text()').extract_first()
            next_request = prefix.replace('movie/cinema', 'cinema/cinemadetail')
            next_request = next_request.replace('pageletCinema', 'pageletCinemadetail')
            next_request = next_request + '&cinemaId=' + cinema_id
            it = scrapy.Request(next_request, callback=self.parse_bigpipe,
                                 meta={'name': response.meta['name'], 'date': response.meta['date'], 'date_ticks': response.meta['date_ticks'], 'cinema': cinema_name})
            if it!=None:
                yield it

    def parse_bigpipe(self, response):
        date_ticks = response.meta['date_ticks']
        screening_list =response.xpath('//div[@data-id=\'\\"'+date_ticks+'\\"\']//li')
        screenings = []
        for index, s in enumerate(screening_list):
            auditorium = s.xpath('.//div[@class=\'\\"hall\']/text()').extract_first()
            start = s.xpath('.//p[@class=\'\\"start\\"\']/text()').extract_first()
            price = s.xpath('.//span[@class=\'\\"num\']/text()').extract_first()
            remain = s.xpath('.//div[@class=\'\\"seat\']/text()').extract_first()
            remain = remain[remain.find('位')+1:remain.find('%')+1]
            screening = NuomiFilmScreenings(auditorium=auditorium.strip(), time=start.strip(), price=price.strip(), remain=remain)
            screenings.append(screening)
        if len(screenings)==0:
            return None
        film = NuomiFilm(name=response.meta['name'], cinema=response.meta['cinema'], date=response.meta['date'], screenings=screenings)
        return film

    def date_format(self, date_str):
        year = date.today().year
        month_pos = date_str.find('月')
        month = date_str[2:month_pos]
        day = date_str[month_pos+1:-2]
        s = str(year) + '-' + month + '-' + day
        return s







