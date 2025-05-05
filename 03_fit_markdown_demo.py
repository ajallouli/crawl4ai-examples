import asyncio
from crawl4ai import *
from typing import List

async def main():
    
    async with AsyncWebCrawler() as crawler:
        result: List[CrawlResult] = await crawler.arun(
            url="https://en.wikipedia.org/wiki/Python_(programming_language)",
            config=CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                )
            )
        )
        print(f"RAW: {len(result.markdown.raw_markdown)} chars")
        print(f"RAW: {len(result.markdown.fit_markdown)} chars")

if __name__ == "__main__":
    asyncio.run(main())