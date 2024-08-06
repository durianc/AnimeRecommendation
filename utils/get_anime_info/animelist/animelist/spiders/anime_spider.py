import csv
import scrapy

BASE_URL = 'https://myanimelist.net/anime'

class AnimeSpider(scrapy.Spider):
    name = "anime"

    def start_requests(self):
        with open('G:\\AnimeRecommendation\\data\\anime.csv', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            anime_ids = [row["anime_id"] for row in reader]

        with open('output.csv', encoding='utf-8') as output_file:
            output_reader = csv.DictReader(output_file)
            existing_anime_ids = [row['anime_id'] for row in output_reader]

        anime_ids = [id for id in anime_ids if id not in existing_anime_ids]

        for id in anime_ids:
            yield scrapy.Request(url=f'{BASE_URL}/{id}', callback=self.parse, meta={'anime_id': id})

    def parse(self, response):
        anime_id = response.meta.get("anime_id")

        # 使用XPath提取日本标题，并去除空格
        japanese_titles = response.xpath("//span[contains(text(), 'Japanese')]/following-sibling::text()").getall()
        japanese_titles = [text.strip() for text in japanese_titles if len(text) > 0]

        # 使用XPath提取播放时间，并去除空格
        aired = response.xpath("//span[contains(text(), 'Aired')]/following-sibling::text()").getall()
        aired = [text.strip() for text in aired if len(text) > 0]

        # 使用XPath提取图片URL
        image_url = response.xpath("//a[contains(@href, 'pics')]/img/@data-src").getall()
        if image_url:
            image_url = image_url[0]  # 获取列表中的第一个元素
        else:
            image_url = ""

        # 打印提取的数据
        print(f"{anime_id}: {japanese_titles}\n[{aired}]")

        # 生成字典并使用yield返回
        yield {
            'anime_id': anime_id,
            'japanese_title': japanese_titles,
            'aired': aired,
            'image_url': image_url
        }