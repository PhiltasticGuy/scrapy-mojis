# ML - Scrapy-mojis

The first run will take a few minutes as the HTTP requests are cached by `scrapy`.

The custom code is all contained in a single `spider` under `/ml_scrapy_mojis/spiders/unicode.py`.

You need to install the `scrapy` package before running it. You can use the following commands:

```bash
# Install scrapy.
pip install scrapy

# Run the spider.
scrapy crawl unicode
```
