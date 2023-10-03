import httpx
import asyncio
from parsel import Selector


class AsyncScraper:
    TARGET_URL = "https://kloop.kg/"
    LINK_XPATH = '//div[@class="elementor-widget-container"]/a/@href'
    HEADERS = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Referer': 'https://www.google.com/',
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'cross-site'
}

    async def parse_date(self):
        async with httpx.AsyncClient(headers=self.HEADERS) as client:
            await self.get_url(client, url=self.TARGET_URL)

    async def get_url(self, client, url):
        response = await client.get(url)
        # print(response.text)
        await self.scrap_links(content=response.text, client=client)

    async def scrap_links(self, content, client):
        tree = Selector(text=content)
        links = tree.xpath(self.LINK_XPATH).extract()[:5]
        for link in links:
            print(link)


if __name__ == "__main__":
    scraper = AsyncScraper()
    asyncio.run(scraper.parse_date())