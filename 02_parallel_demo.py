import asyncio
from crawl4ai import *
from typing import List

async def main():
    urls= [
        "https://news.ycombinator.com",
        "https://example.com",
        "https://httpbin.org/html"
    ]
    
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun_many(
            urls=urls,
        )
        print(f"cwaled {len(results)} URLs in parallel:")
        
        for i, result in enumerate(results):
            print(
                f"{i+1} - {result.url} - {'Success' if result.success else 'Failed'}"
            )


if __name__ == "__main__":
    asyncio.run(main())