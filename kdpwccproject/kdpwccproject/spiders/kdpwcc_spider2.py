import scrapy
import os
from kdpwccproject.items import KdpwccprojectItem

class KdpwccSpider(scrapy.Spider):
    name = "kdpwcc_spider2"
    allowed_domains = ["kdpwccp.pl"]
    start_urls = ["https://www.kdpwccp.pl/en/resolutions.html?category=2"]

    download_dir = r'D:\PDF\'OTC'

    def parse(self, response):
        for resolution in response.css('.box-11'):
            resolution_number = resolution.css('.txt-1::text').get()
            resolution_detail = resolution.css('.txt-2::text').get()
            pdf_link = resolution.css('a[href$=".pdf"]::attr(href)').get()


            
            item = KdpwccprojectItem(
                resolution_number=resolution_number,
                resolution_detail=resolution_detail,
                pdf_link=response.urljoin(pdf_link) if pdf_link else None
            )
            
            if pdf_link:
                pdf_url = response.urljoin(pdf_link)
                request = scrapy.Request(url=pdf_url, callback=self.save_pdf)
                request.meta['item'] = item
                yield request
            else:
                yield item

        # pagination
        page_urls = response.css('.chosen-select option::attr(value)').getall()
        for page_url in page_urls:
            if page_url.startswith("https://"):
                yield scrapy.Request(page_url, callback=self.parse)

    def save_pdf(self, response):
        pdf_name = response.url.split('/')[-1]
        if not os.path.exists(self.download_dir):
            os.makedirs(self.download_dir)
        file_path = os.path.join(self.download_dir, pdf_name)
        with open(file_path, 'wb') as f:
            f.write(response.body)
        
        self.log(f"Downloaded PDF: {file_path}")
        
       
        item = response.meta['item']
        yield item

