import asyncio
from crawl4ai import *
from typing import List
# import os
# import base64
import json

async def main():
    print("Structred extraction with LLM: ")
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider='anthropic/claude-3-7-sonnet-20250219',
            api_token='env:ANTHROPIC_API_KEY'
        ),
        instruction='This is news.ycombinator.com, extract all the news and for each I want: title, source url, number of comments.',
        extraction_type='schema',
        schema='{title: str, url: str, comment:int}',
        extra_args={
            "temperature":0.0
        },
        verbose=True
    )
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            url="https://news.ycombinator.com/",
            config=config
        )

        for result in results:
            print(f'URL = {result.url}')
            print(f'success = {result.success}')
            if result.success:
                data=json.loads(result.extracted_content)
                print(json.dumps(data,indent=2))
            else:
                print('failed to extract structed data')



if __name__ == "__main__":
    asyncio.run(main())