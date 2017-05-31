import scrapy
from MySpider.items import GewaraFilmScreenings
from MySpider.items import GewaraFilm

class GewaraSpider(scrapy.Spider):
    name = 'gewara'
    start_urls = ['http://www.gewara.com/cinema/searchOpi.xhtml']

    def start_requests(self):
        return [scrapy.FormRequest("http://www.gewara.com/cinema/searchOpi.xhtml",
                                   cookies={'citycode': '320100'},
                                   callback=self.parse_city)]

    def parse_city(self, response):
        prefix = 'http://www.gewara.com/movie/ajax/getOpiItemNew.xhtml'
        movie_id_list = response.xpath('//div[@id="movieSiteHeight"]/a/@id').extract()
        movie_name_list = response.xpath('//div[@id="movieSiteHeight"]/a/text()').extract()
        cinema_id_list = response.xpath('//div[@id="cinemaPanel"]/a/@id').extract()
        cinema_name_list = response.xpath('//div[@id="cinemaPanel"]/a/text()').extract()
        date_list = response.xpath('//a[@rel="fyrq"]/@id').extract()
        for fyrq in date_list:
            for cid, cinema_name in zip(cinema_id_list, cinema_name_list):
                for movieid, movie_name in zip(movie_id_list, movie_name_list):
                    ajax_url = prefix + '?cid=' + cid + '&movieid=' + movieid + '&fyrq=' + fyrq
#                    yield scrapy.Request(ajax_url, callback=lambda response, date=date, name=name, cinema=cinema: self.parse_ajax)
                    yield scrapy.Request(ajax_url, callback=self.parse_ajax,
                                         meta={'date': fyrq, 'name': movie_name.strip(), 'cinema': cinema_name.strip()})

    def parse_ajax(self, response):
        screenings = []
        chooseOpi_body = response.xpath('//div[@class="chooseOpi_body "]//li')
        for index, li in enumerate(chooseOpi_body):
            auditorium = li.xpath('.//span[@class="opiRoom ui_roomType"]/label/text()').extract_first()
            time = li.xpath('.//span[@class="opitime"]/b/text()').extract_first()
            price = li.xpath('.//span[@class="opiPrice"]/b/text()').extract_first()
            language = li.xpath('.//span[@class="opiEdition"]/em/text()').extract_first()
            screening = GewaraFilmScreenings(auditorium=auditorium, time=time, price=price, language=language)
            screenings.append(screening)
        film = GewaraFilm(name=response.meta['name'], cinema=response.meta['cinema'], date=response.meta['date'], screenings=screenings)
        return film









