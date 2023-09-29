from parsel import Selector
import requests


class NewsScraper:
    PLUS_URL = "https://24.kg/"
    URL = "https://24.kg/"
    LINK_XPATH = '//div[@class="title"]/a/@href'
    TITLE_XPATH = '//div[@class="title"]/a/strong'


    def parse_data(self):
        html = requests.get(url=self.URL).text
        tree = Selector(text=html)
        links = tree.xpath(self.LINK_XPATH).extract()
        titles = tree.xpath(self.TITLE_XPATH).extract()
        # for link in links:
        #     print(self.PLUS_URL + link)
        #     print()
        #     for title in titles:
        #         print(title)
        return links[:5]

if __name__ == "__main__":
    scraper = NewsScraper()
    scraper.parse_data()