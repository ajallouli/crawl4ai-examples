import asyncio
from crawl4ai import *
from typing import List
import json

async def main():
    print("Extract media and links from a pag: ")
    async with AsyncWebCrawler() as crawler:
        result: List[CrawlResult] = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Main_Page"
        )

        for i, result in enumerate(result):
            images = result.media.get("images",[])
            print(f'Found {len(images)} images!')

            internal_links = result.media.get("internal",[])
            print(f'Found {len(internal_links)} internal_links!')

            external_links = result.media.get("external",[])
            print(f'Found {len(external_links)} external_links!')

            #save 
            with open("images.json", 'w') as f:
                json.dump(images, f, indent=2)

            #save 
            with open("links.json", 'w') as f:
                json.dump(
                    {
                    "internal":internal_links,
                    "external":external_links}
                    , f, indent=2)


        print(f"RAW: {len(result.markdown.raw_markdown)} chars")
        print(f"RAW: {len(result.markdown.fit_markdown)} chars")

if __name__ == "__main__":
    asyncio.run(main())