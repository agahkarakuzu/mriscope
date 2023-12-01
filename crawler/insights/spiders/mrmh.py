import scrapy
from scrapy.item import Item, Field
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from bs4 import BeautifulSoup
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re                      
import os 
   
class MrmhItem(Item):
    result = Field()
    
class MrmhSpider(CrawlSpider):
    name = 'mrmh'
    allowed_domains = ['blog.ismrm.org']
    # Generate start_urls for a range of years, months, and dates
    start_urls = ["https://blog.ismrm.org/{}/reproducible-research-insights".format(f'202{year:01d}/{month:02d}/{day:02d}') 
                  for year in range(0, 4)  # assuming 2023
                  for month in range(1, 13)
                  for day in range(1, 32)]
    rules = (Rule(LinkExtractor(allow=(r'/\d{4}/\d{2}/\d{2}/reproducible-research-insights.*',"parse",)), callback='parse'),)
    
    def parse(self, response):
        cwd = os.getcwd()
        crawler_output_path = os.path.join(cwd,"crawler_output")
        if not os.path.exists(crawler_output_path):
            os.mkdir(crawler_output_path)
        soup = BeautifulSoup(response.text, 'html.parser')
        td_post_content = soup.find('div', class_='td-post-content')
        if td_post_content:
            headers = [header.get_text(strip=True) for header in td_post_content.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])]
            paragraphs = [p.get_text(strip=True) for p in td_post_content.find_all('p')]
            content = "\n".join(headers + paragraphs)

        filename = f"{response.url.replace('/', '_').lstrip('_')}"
        filename = f"{filename.split('_')[-2]}.txt"

        self.log(f"{filename}")
        save_file = os.path.join(crawler_output_path,filename)
        # Save content to a text file
        with open(save_file, 'w', encoding='utf-8') as file:
            file.write(content)