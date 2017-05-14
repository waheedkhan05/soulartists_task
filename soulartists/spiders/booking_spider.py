import scrapy
from scrapy.loader import ItemLoader
from soulartists.items import BookingDetailItem

class BookingSpider(scrapy.Spider):
    name = "booking"
    destination_id = '38833'
    start_urls = [
        # Adding the start url for Marakesh from booking.com
	"https://www.booking.com/searchresults.html?label=gen173nr-1DCAooggJCAlhYSDNiBW5vcmVmaAKIAQGYATHCAQN4MTHIAQzYAQPoAQH4AQKSAgF5qAID;sid=4c399253f9275f4758931bfd757c0c76;checkin=2017-05-15;checkout=2017-05-16;city=-38833"
    ]

    pageNumber = 1

    #for each hotel from list of hotels in Marakesh, pick the url and pass to parse_hotel_public_data
    def parse(self, response):
        for hotelurl in response.xpath('//a[@class="hotel_name_link url"]/@href'):
            url = response.urljoin(hotelurl.extract())
            yield scrapy.Request(url, callback=self.parse_hotel_public_data)

        next_page = response.xpath('//a[starts-with(@class,"paging-next")]/@href')
        if next_page:
            url = response.urljoin(next_page[0].extract())
            yield scrapy.Request(url, self.parse)

    def parse_hotel_public_data(self,response):
        hotel_name = response.xpath('//h2[@id="hp_hotel_name"]/text()').extract()
        hotel_address = response.xpath('//p[@class="address address_clean"]/span/text()').extract()
        hotel_desc_title = response.xpath("//div[@id='summary']/h3[@class='b_geo_hp_city_centre_description_heading']/text()").extract()
        hotel_desc_summary = response.xpath('//div[@id="summary"]//p/text()').extract()
        hotel_desc_detail = response.xpath('//div[@class="hp_hotel_description_hightlights_wrapper   "]//p/text()').extract()
        hotel_most_popular_facilities = response.xpath('//div[@class="hp_hotel_description_hightlights_wrapper   "]//div[@class="important_facility hp-desc-facility "]/text()').extract()
        facilities_xpath = response.xpath('//div[@id="hp_facilities_box"]/div[@class="facilitiesChecklist"]/div')
        landmarks = response.xpath('//div[@class="hp-poi-content-container clearfix hp-poi-content-container--column"]//div[@class="hp-poi-content-section popular-landmarks"]/ul/li/span[@class="poi-list-item__title"]/text()').extract()
        restaurants_and_markets = response.xpath('//div[@class="hp-poi-content-container clearfix hp-poi-content-container--column"]//div[@class="hp-poi-content-section hp-surroundings-category hp-surroundings-category_num-1"]/ul/li/span/span[@class="poi-list-item__name"]/text()').extract()
        natural_beauties = response.xpath('//div[@class="hp-poi-content-container clearfix hp-poi-content-container--column"]//div[@class="hp-poi-content-section hp-surroundings-category hp-surroundings-category_num-2"]/ul/li/span/span[@class="poi-list-item__name"]/text()').extract()
        airports = response.xpath('//div[@class="hp-poi-content-container clearfix hp-poi-content-container--column"]//div[@class="hp-poi-content-section hp-surroundings-category hp-surroundings-category_num-3"]//ul/li/span[@class="poi-list-item__title"]/text()').extract()
        scoreword = response.xpath('//div[@id="photo_wrapper"]//a[@class="big_review_score_detailed js-big_review_score_detailed ind_rev_total hp_review_score js-hotel-review-score"]/span/text()').extract()
        score = response.xpath('//div[@id="photo_wrapper"]//a[@class="big_review_score_detailed js-big_review_score_detailed ind_rev_total hp_review_score js-hotel-review-score"]/span/span[@class="average js--hp-scorecard-scoreval"]/text()').extract()
        score_out_of = response.xpath('//div[@id="photo_wrapper"]//a[@class="big_review_score_detailed js-big_review_score_detailed ind_rev_total hp_review_score js-hotel-review-score"]/span/span[@class="out_of"]/span/text()').extract()
        
        item = BookingDetailItem()
        # store facilities as dictionary, as facilities_dict['Facility Title'] = ['','']
        facilities_dict = {}
        facilities_xpath = response.xpath('//div[@id="hp_facilities_box"]/div[@class="facilitiesChecklist"]/div')
        for facility in facilities_xpath:
            titles = [tit.replace('\n','') for tit in facility.xpath('h5/text()').extract() if len(tit)>1]
            facs = [f.replace('\n','') for f in facility.xpath('ul/li/span/text()').extract() if len(f)>1]
            facilities_dict["".join(titles)] = facs
        if score:
            item['score'] = "".join([tit.replace('\n','') for tit in score])
        if scoreword:
            item['score_word'] = "".join([tit.replace('\n','') for tit in scoreword])
        if facilities_dict:
            item['facilities'] = unicode(facilities_dict)
        if hotel_name:
            item['hotel_name'] = ''.join(e.replace('\n','') for e in hotel_name) 
        if hotel_address:
            item['hotel_address'] = ''.join(e.replace('\n','') for e in hotel_address) 
            import re
            zipcode = re.match('^.*(?P<zipcode>\d{5}).*$', item['hotel_address']).groupdict()['zipcode']
            if zipcode:
                item['zipcode'] = zipcode
        item['destination_id'] = '38833'
        if hotel_desc_title:
            item['hotel_desc_title'] = ''.join(e.replace('\n','') for e in hotel_desc_title)
        if hotel_desc_detail:
            item['hotel_desc_detail'] = '\n'.join(e.replace('\n','') for e in hotel_desc_detail)
        if landmarks:
            item['landmarks_nearby'] = ','.join(e.replace('\n','') for e in landmarks)
        if hotel_most_popular_facilities:
            item['hotel_most_popular_facilities'] = ','.join(e.replace('\n','') for e in hotel_most_popular_facilities)
        if restaurants_and_markets:
            item['restaurants_and_markets'] = ','.join(e.replace('\n','') for e in restaurants_and_markets)
        if hotel_desc_summary:
            item['hotel_desc_summary'] = '\n'.join(e for e in hotel_desc_summary)
        if natural_beauties:
            item['natural_beauties'] = ','.join(e for e in natural_beauties)
        if airports:
            item['airports_nearby'] = ','.join(e for e in airports)
        yield item