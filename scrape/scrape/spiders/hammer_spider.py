from itertools import combinations
import re

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from scrape.items import VoteItem

def parse_votes(res):
    m = re.match("\s*(\d+)\s+out\s+of\s+(\d+)", res)
    if not m:
        raise Exception("Could not parse " + res + "as score")
    left_votes, total_votes = m.groups()
    left_votes  = int(left_votes)
    total_votes = int(total_votes)
    right_votes = total_votes - left_votes
    return (left_votes, right_votes)

def parse_langs(res):
    m = re.match("\s*(.*)\s+(?:and|over)\s+(.*)", res)
    if not m:
        raise Exception("Could not parse " + res + "as language pair")
    return m.groups()

class HammerSpider(Spider):
    def create_vote_item(self, slug, votes, langs):
        item = VoteItem()
        item["slug"]  = slug 
        item["votes"] = parse_votes(votes)
        item["langs"] = parse_langs(langs)
        return item

    def parse_faceoff(self, response):
        sel = Selector(response)

        assertions = sel.xpath('//li[@class="assertion"]')

        slug_list  = assertions.xpath('h3/a/@data-slug').extract()
        votes_list = assertions.xpath('div/span[@class="votes"]/text()').extract()
        votes_list = filter(lambda t: re.search("picked|each", t), votes_list)
        langs_list = assertions.xpath('div/span[@class="votes"]/a/text()').extract()
        
        if len(slug_list) != len(votes_list) or len(slug_list) != len(langs_list):
            raise Exception("Mismatched lengths %d,%d,%d" 
                            % len(slug_list), len(votes_list), len(langs_list))
        
        items =  [ self.create_vote_item(*el) for el in zip (slug_list, votes_list, langs_list) ] 
        
        return items

    def request_from_pair(self, code1, code2):
        url_base = "http://hammerprinciple.com/therighttool/items"
        url = "%s/%s/%s" % (url_base, code1, code2)
        return Request(url, self.parse_faceoff)
        
    def requests_from_codes(self, codes):
        return (self.request_from_pair(*pair) for pair in combinations(codes, 2))

    def parse(self, response):
        
        sel = Selector(response)

        language_hrefs = sel.xpath('//div[@class="chart items"]//a/@href').extract()
        language_codes = [ (href.split("/"))[-1] for href in language_hrefs]

        language_codes.remove("actionscript")
        
        return self.requests_from_codes(language_codes)

    name = "hammer"
    allowed_domains = ["hammerprinciple.com"]
    start_urls = [
        "http://hammerprinciple.com/therighttool/"
    ]

