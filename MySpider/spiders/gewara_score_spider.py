import scrapy
from MySpider.items import GewaraFilmScore

class GewaraScoreSpider(scrapy.Spider):
    name = 'gewara_score'
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
            yield scrapy.Request(next_request, callback=self.parse_score,
                                 meta={'name': movie_name.strip()})

    def parse_score(self, response):
        before = response.xpath('//div[@class="mt20"]/span/sub/text()').extract_first()
        after = response.xpath('//div[@class="mt20"]/span/sup/text()').extract_first()
        score = GewaraFilmScore(name=response.meta['name'], score=before+after)
        return score