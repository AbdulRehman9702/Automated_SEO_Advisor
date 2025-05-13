import scrapy
from scrapy.http import HtmlResponse


class MetaSpider(scrapy.Spider):
    name = "meta_spider"
    start_urls = [
        'https://books.toscrape.com/',  # Add more URLs as needed
    ]

    def parse(self, response: HtmlResponse):
        """
        Parse the response from the given URL and extract metadata.
        """
        # Extract meta data
        title = response.xpath('//title/text()').get() or ''
        meta_description = response.xpath('//meta[@name="description"]/@content').get() or ''
        h1 = response.xpath('//h1/text()').get() or ''
        word_count = len(response.xpath('//body//text()').getall())
        links = response.xpath('//a/@href').getall()

        # Prepare the data dictionary
        data = {
            'Address': response.url,
            'Content Type': response.headers.get('Content-Type', b'').decode('utf-8'),
            'Status Code': response.status,
            'Indexability': 'index' if 'noindex' not in response.text else 'noindex',
            'Title 1': title,
            'Title 1 Length': len(title),
            'Meta Description 1': meta_description,
            'Meta Description 1 Length': len(meta_description),
            'H1-1': h1.strip(),
            'H1-1 Length': len(h1.strip()),
            'Word Count': word_count,
            'Sentence Count': response.text.count('.'),
            'Size (bytes)': len(response.body),
            'Transferred (bytes)': len(response.body),
            'Average Words Per Sentence': word_count / max(response.text.count('.'), 1),
            'Outlinks': len(links),
            'Unique Outlinks': len(set(links)),
            'External Outlinks': len([link for link in links if link.startswith('http')]),
            'Unique External Outlinks': len(set(link for link in links if link.startswith('http'))),
        }

        # Output the data
        yield data
