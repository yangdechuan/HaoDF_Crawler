# -*- coding: utf-8 -*-
import scrapy

import requests
from lxml.html import etree

from HaoDF_Crawler.items import HaodfCrawlerItem

class HaodfSpiderSpider(scrapy.Spider):
    name = 'haodf_spider'
    allowed_domains = ['zixun.haodf.com']
    start_urls = ['http://zixun.haodf.com/']

    def start_requests(self):
        header_data = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Host": "zixun.haodf.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
        }
        base_url = "https://zixun.haodf.com/dispatched/37.htm?p={}"
        for i in range(1, 35):
            cur_url = base_url.format(i)
            res = requests.get(cur_url, headers=header_data)
            html_con = etree.HTML(res.content)

            # targets = html_con.xpath("//li[@class='clearfix']/span[@class='fl']/a[1]/text()")
            # titles = html_con.xpath("//li[@class='clearfix']/span[@class='fl']/a[2]/text()")
            # titles = [title.strip() for title in titles]  # delete space in the title
            urls = html_con.xpath("//li[@class='clearfix']/span[@class='fl']/a[2]/@href")
            for url in urls:
                yield scrapy.Request("https:" + url, callback=self.parse)


    def parse(self, response):
        title = response.xpath("//div[@class='h_s_info_cons']/h3[@class='h_s_cons_info_title']/text()").extract_first()
        disease = response.xpath("//div[@class='h_s_info_cons']/h2[1]/a/text()").extract_first()

        des = response.xpath("//div[@class='h_s_info_cons']/div[1]/strong[1]/text()").extract_first()
        if "病情描述" in des:
            descriptions = response.xpath("//div[@class='h_s_info_cons']/div[1]/text()").extract()
            description = " ".join([x.strip() for x in descriptions if x])

        item = HaodfCrawlerItem()
        item["title"] = title
        item["disease"] = disease
        item["description"] = description
        item["url"] = response.url

        yield item

