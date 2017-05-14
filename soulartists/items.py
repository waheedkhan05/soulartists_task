# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BookingDetailItem(scrapy.Item):
    hotel_name = scrapy.Field()
    hotel_address = scrapy.Field()
    hotel_desc_title = scrapy.Field()
    hotel_desc_detail = scrapy.Field()
    hotel_desc_summary = scrapy.Field()
    facilities = scrapy.Field()
    landmarks_nearby = scrapy.Field()
    hotel_most_popular_facilities = scrapy.Field()
    restaurants_and_markets = scrapy.Field()
    natural_beauties = scrapy.Field()
    airports_nearby = scrapy.Field()