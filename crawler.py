import os.path

import html2text
import scrapy
from slugify import slugify


def clean_text(text: str):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    return h.handle(text)


class TiSpider(scrapy.Spider):
    name = "ticino"
    allowed_domains = ["ti.ch"]
    start_urls = ["https://www4.ti.ch/tich/tematiche"]
    max_depth = 3

    custom_settings = {"COOKIES_ENABLED": False, "javascript": None}

    def parse(self, response, **kwargs):
        depth = response.meta.get("depth", 1)
        content = response.xpath('//div[@id="contenitore"]').get()

        if not content:
            return

        window_title = response.xpath("//title/text()").get()
        title = slugify(window_title)
        path = os.path.join("documents", f"{title}.md")
        with open(path, "w") as f:
            f.writelines(clean_text(content))

        # Follow and scrape links on the page
        links = response.css("a::attr(href)").getall()
        if depth < self.max_depth:
            for link in links:
                yield response.follow(
                    link, callback=self.parse, meta={"depth": depth + 1}
                )
