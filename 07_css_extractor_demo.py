

import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai import RoundRobinProxyStrategy
from crawl4ai import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai import LLMConfig
from crawl4ai import PruningContentFilter, BM25ContentFilter
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai import BFSDeepCrawlStrategy, DomainFilter, FilterChain
from crawl4ai import BrowserConfig
from typing import List
import os
import json

async def main():

    """Extract structured data using CSS selectors"""
    print("\n=== 5. CSS-Based Structured Extraction ===")
    # Sample HTML for schema generation (one-time cost)
    sample_html = """
    <div class="body-post clear">
    <a class="story-link" href="https://thehackernews.com/2025/04/malicious-python-packages-on-pypi.html">
        <div class="clear home-post-box cf">
            <div class="home-img clear">
                <div class="img-ratio">
                    <img alt="..." src="...">
                </div>
            </div>
            <div class="clear home-right">
                <h2 class="home-title">Malicious Python Packages on PyPI Downloaded 39,000+ Times, Steal Sensitive Data</h2>
                <div class="item-label">
                    <span class="h-datetime"><i class="icon-font icon-calendar"></i>Apr 05, 2025</span>
                    <span class="h-tags">Malware / Supply Chain Attack</span>
                </div>
                <div class="home-desc"> Cybersecurity researchers have...</div>
            </div>
        </div>
    </a>
    </div>
    """

    # Check if schema file exists
    schema_file_path = f"{os.getcwd()}/schema.json"
    if os.path.exists(schema_file_path):
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
    else:
        # Generate schema using LLM (one-time setup)
        schema = JsonCssExtractionStrategy.generate_schema(
            html=sample_html,
            llm_config=LLMConfig(
                provider='anthropic/claude-3-7-sonnet-20250219',
                api_token='env:ANTHROPIC_API_KEY',
            ),
            query="From https://thehackernews.com/, I have shared a sample of one news div with a title, date, and description. Please generate a schema for this news div.",
        )

        print(f"Generated schema: {json.dumps(schema, indent=2)}")
        # Save the schema to a file , and use it for future extractions, in result for such extraction you will call LLM once
        with open(f"{os.getcwd()}/schema.json", "w") as f:
            json.dump(schema, f, indent=2)

    # Create no-LLM extraction strategy with the generated schema
    extraction_strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    # Use the fast CSS extraction (no LLM calls during extraction)
    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            "https://thehackernews.com", config=config
        )

        # Create an array to store all extracted dictionaries
        all_extracted_data = []
        
        for result in results:
            print(f"URL: {result.url}")
            print(f"Success: {result.success}")
            if result.success:
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2))
                # Add the extracted data to our array
                all_extracted_data.append(data)
            else:
                print("Failed to extract structured data")
        
        # Write all collected dictionaries to a file
        output_file_path = f"{os.getcwd()}/all_extracted_data.json"
        with open(output_file_path, "w") as f:
            json.dump(all_extracted_data, f, indent=2)
        
        print(f"\nAll extracted data has been saved to: {output_file_path}")


if __name__ == "__main__":
    asyncio.run(main())