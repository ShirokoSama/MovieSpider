import scrapy
from MySpider.items import GewaraFilmScreenings
from MySpider.items import GewaraFilm

class GewaraSpider(scrapy.Spider):
    name = 'gewara'
    start_urls = []

    def start_requests(self):
        return [scrapy.FormRequest("http://www.gewara.com/cinema/searchOpi.xhtml",
                                   cookies={'citycode': '320100'},
                                   callback=self.parse_movie)]

    def parse_movie(self, response):
        prefix = response.url
        movie_id_list = response.xpath('//div[@id="movieSiteHeight"]/a/@id').extract()
        movie_name_list = response.xpath('//div[@id="movieSiteHeight"]/a/text()').extract()
        for movieid, movie_name in zip(movie_id_list, movie_name_list):
            next_request = prefix + '?movieid=' + movieid
            yield scrapy.Request(next_request, callback=self.parse_date,
                                 meta={'name': movie_name.strip()})

    def parse_date(self, response):
        prefix = response.url
        date_list = response.xpath('//a[@rel="fyrq"]/@id').extract()
        for fyrq in date_list:
            next_request = prefix + '&fyrq=' + fyrq
            yield scrapy.Request(next_request, callback=self.parse_cinema,
                                 meta={'name': response.meta['name'], 'date': fyrq.strip()})

    def parse_cinema(self, response):
        prefix = response.url
        cinema_id_list = response.xpath('//div[@id="cinemaPanel"]/a/@id').extract()
        cinema_name_list = response.xpath('//div[@id="cinemaPanel"]/a/text()').extract()
        for cid, cinema_name in zip(cinema_id_list, cinema_name_list):
            ajax_url = prefix.replace('cinema/searchOpi','movie/ajax/getOpiItemNew') + '&cid=' + cid
            it =  scrapy.Request(ajax_url, callback=self.parse_ajax,
                                 meta={'name': response.meta['name'], 'date': response.meta['date'], 'cinema': cinema_name.strip()})
            if it!=None:
                yield it

#     def parse_city(self, response):
#         prefix = 'http://www.gewara.com/movie/ajax/getOpiItemNew.xhtml'
#         movie_id_list = response.xpath('//div[@id="movieSiteHeight"]/a/@id').extract()
#         movie_name_list = response.xpath('//div[@id="movieSiteHeight"]/a/text()').extract()
#         cinema_id_list = response.xpath('//div[@id="cinemaPanel"]/a/@id').extract()
#         cinema_name_list = response.xpath('//div[@id="cinemaPanel"]/a/text()').extract()
#         date_list = response.xpath('//a[@rel="fyrq"]/@id[position()<3]').extract()
#         for fyrq in date_list:
#             for cid, cinema_name in zip(cinema_id_list, cinema_name_list):
#                 for movieid, movie_name in zip(movie_id_list, movie_name_list):
#                     ajax_url = prefix + '?cid=' + cid + '&movieid=' + movieid + '&fyrq=' + fyrq
# #                    yield scrapy.Request(ajax_url, callback=lambda response, date=date, name=name, cinema=cinema: self.parse_ajax)
#                     it = scrapy.Request(ajax_url, callback=self.parse_ajax,
#                                          meta={'date': fyrq, 'name': movie_name.strip(), 'cinema': cinema_name.strip()})
#                     if it!=None:
#                         yield it

    def parse_ajax(self, response):
        screenings = []
        chooseOpi_body = response.xpath('//div[@class="chooseOpi_body "]//li')
        for index, li in enumerate(chooseOpi_body):
            auditorium = li.xpath('.//span[@class="opiRoom ui_roomType"]/label/text()').extract_first()
            time = li.xpath('.//span[@class="opitime"]/b/text()').extract_first()
            price = li.xpath('.//span[@class="opiPrice"]/b/text()').extract_first()
            language = li.xpath('.//span[@class="opiEdition"]/em/text()').extract_first()
            screening = GewaraFilmScreenings(auditorium=auditorium.strip(), time=time.strip(), price=price.strip(), language=language.strip())
            screenings.append(screening)
        if len(screenings)==0:
            return None
        film = GewaraFilm(name=response.meta['name'], cinema=response.meta['cinema'], date=response.meta['date'], screenings=screenings)
        return film









