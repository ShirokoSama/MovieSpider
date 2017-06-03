import scrapy
from MySpider.items import MeituanFilmScore

class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    start_urls = []
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'

    def start_requests(self):
        request_url = 'http://nj.meituan.com/dianying/'
        return [scrapy.FormRequest(request_url, callback=self.parse_movie)]

    def parse_movie(self, response):
        movie_list = response.xpath('//div[@class="reco-movieinfo"] | //div[@class="reco-movieinfo reco-movieinfo--last"]')
        for index, div in enumerate(movie_list):
            movie_name = div.xpath('.//h3/text()').extract_first()
            before = div.xpath('.//strong[@class="rates"]/text()').extract_first()
            after = div.xpath('.//strong[@class="rates-point"]/text()').extract_first()
            score = MeituanFilmScore(name=movie_name, score=before+after)
            yield score
