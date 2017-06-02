import scrapy

class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    start_urls = []

    def start_requests(self):
        request_url = 'http://nj.meituan.com/dianying/'
        return [scrapy.FormRequest(request_url, callback=self.parse_movie)]

    def parse_movie(self, response):
        movie_list = response.xpath('//div[@class="reco-movieinfo"] | //div[@class="reco-movieinfo reco-movieinfo--last"]')
        for index, div in enumerate(movie_list):
            movie_name = div.xpath('.//h3/text()').extract_first()
            movie_url = div.xpath('./a/@href').extract_first()
            next_request = movie_url + '?mtt=1.movie%2Fmoviedeal'
            yield scrapy.Request(next_request, callback=self.parse_date_and_cinema,
                                 meta={'name': movie_name})

    def parse_date_and_cinema(self, response):
        textarea = response.xpath('.//div[@data-component="cinema-list"]//textarea//h4').extract_first()
        print(textarea)
        # date_list = response.xpath('//div[@class="filter-label-list filter-section date-filter-wrapper first-filter"]//a')
        # cinema_list = response.xpath('//div[@class="filter-label-list filter-section brand-filter-wrapper"]//a')
        # for indexd, ad in enumerate(date_list):
        #     date_url = ad.xpath('./@href').extract_first()
        #     for indexc, ac in enumerate(cinema_list):
        #         cinema_url = ac.xpath('./@href').extract_first()
        #         print(date_url+' '+cinema_url)