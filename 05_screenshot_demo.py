import asyncio
from crawl4ai import *
from typing import List
import os
import base64

async def main():
    print("Creating Screenshot: ")
    async with AsyncWebCrawler() as crawler:
        result: List[CrawlResult] = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Main_Page",
            config=CrawlerRunConfig(screenshot=True, pdf=True)
        )

        destination_path = os.getcwd()

        for i, result in enumerate(result):
            if result.screenshot:
                screenshot_path = f'{destination_path}/example_screenshot.png'
                with open(screenshot_path, "wb") as f:
                    f.write(base64.b64decode(result.screenshot))
            
                print(f'Screenshot saved to {screenshot_path}')

            if result.pdf:
                screenshot_path = f'{destination_path}/example_screenshot.pdf'
                with open(screenshot_path, "wb") as f:
                    f.write(result.pdf)            
                print(f'PDF saved to {screenshot_path}')


if __name__ == "__main__":
    asyncio.run(main())