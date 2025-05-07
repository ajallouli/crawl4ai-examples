import asyncio
import json
from crawl4ai import JsonCssExtractionStrategy, LLMConfig

async def generate_hackernews_schema():
    # Sample HTML from The Hacker News article
    sample_html = """
        <div class="body-post clear">
        <a class="story-link" href="https://thehackernews.com/2025/05/hackers-exploit-samsung-magicinfo.html">
        <div class="clear home-post-box cf">
        <div class="home-img clear">
        <div class="img-ratio"><img alt="Hackers Exploit " class="home-img-src lazyload loaded" decoding="async" height="380" src="https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgcntDUofgjvW98jqFEedPc494A_7Raxqkae3EP06JGxrfmeEwW64e1nM6LyaK7TK3E4r9Z0EbR88ugllsPUwn8Ils9gzi-kcpBd_iZd1ulRfU-YJGDHLyO7XKu6SFsV749RalqWLswDpt3idxsup4vSuip5OT6aenoOqE4JnqFo7nqaUMfuMrTIjPkOG0D/w500/botnet.jpg" width="728"></div>
        <noscript><img alt=' Mirai Botnet' decoding='async' loading='lazy' src='https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEgcntDUofgjvW98jqFEedPc494A_7Raxqkae3EP06JGxrfmeEwW64e1nM6LyaK7TK3E4r9Z0EbR88ugllsPUwn8Ils9gzi-kcpBd_iZd1ulRfU-YJGDHLyO7XKu6SFsV749RalqWLswDpt3idxsup4vSuip5OT6aenoOqE4JnqFo7nqaUMfuMrTIjPkOG0D/s728-rw-e365/botnet.jpg'/></noscript>
        </div>
        <div class="clear home-right">
        <h2 class="home-title">Hackers Botnet</h2>
        <div class="item-label">
        <span class="h-datetime"><i class="icon-font icon-calendar"></i>May 06, 2025</span>
        <span class="h-tags">Internet of Thing / Vulnerability</span>
        </div>
        <div class="home-desc"> Threat actors Akamai researcher Kyle Lefton said  in a report shared with The Hacker News.   In the attacks detected by the web </div>
        </div>
        </div>
        </a>
        </div>
    """

    try:
        # Try to generate schema using JsonCssExtractionStrategy
        print("Attempting to generate schema using LLM...")
        schema = JsonCssExtractionStrategy.generate_schema(
            html=sample_html,
            llm_config=LLMConfig(
                provider='anthropic/claude-3-7-sonnet-20250219',
                api_token='env:ANTHROPIC_API_KEY',
            ),
            query="I have shared a sample of one news div with a title, date, and description. Please generate a schema for this news div.",
        )
        
        if not schema:
            raise Exception("Empty schema returned")
        else:
            print(f"**** Generated schema: {json.dumps(schema, indent=2)}")
            
    except Exception as e:
        print(f"Error generating schema with LLM: {e}")
        print("Using pre-defined schema based on HTML structure...")
        
        # Create a hardcoded schema based on the HTML structure
        schema = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the news article",
                    "cssSelector": ".home-title"
                },
                "date": {
                    "type": "string",
                    "description": "The publication date of the article",
                    "cssSelector": ".h-datetime"
                },
                "tags": {
                    "type": "string",
                    "description": "The category or tags of the article",
                    "cssSelector": ".h-tags"
                },
                "description": {
                    "type": "string",
                    "description": "The summary or description of the article",
                    "cssSelector": ".home-desc"
                },
                "image_url": {
                    "type": "string",
                    "description": "The URL of the article's main image",
                    "cssSelector": ".home-img-src",
                    "attribute": "src"
                },
                "article_url": {
                    "type": "string",
                    "description": "The URL of the full article",
                    "cssSelector": ".story-link",
                    "attribute": "href"
                }
            },
            "required": ["title", "date", "description", "article_url"]
        }
    
    # Print the generated schema
    print("\nGenerated schema for The Hacker News:")
    print(json.dumps(schema, indent=2))
    
    # Save the schema to a file for future use
    with open('hackernews_schema.json', 'w') as f:
        json.dump(schema, f, indent=2)
    print("\nSchema saved to 'hackernews_schema.json'")
    
    return schema

async def main():
    # Generate the schema
    schema = await generate_hackernews_schema()
    
    print("\nThis schema can be used for scraping The Hacker News website (https://thehackernews.com/)")
    print("Example usage:")
    print("""
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
    from crawl4ai import JsonCssExtractionStrategy
    import json
    import asyncio
    
    async def scrape_hackernews():
        # Load the schema
        with open('hackernews_schema.json', 'r') as f:
            schema = json.load(f)
        
        # Create extraction strategy with the schema
        extraction_strategy = JsonCssExtractionStrategy(schema=schema)
        
        # Create and run the crawler
        crawler = AsyncWebCrawler(
            config=CrawlerRunConfig(
                start_urls=["https://thehackernews.com/"],
                extraction_strategy=extraction_strategy,
            )
        )
        results = await crawler.run()
        
        # Print the extracted data
        for result in results:
            print(json.dumps(result.data, indent=2))
    
    if __name__ == "__main__":
        asyncio.run(scrape_hackernews())
    """)

if __name__ == "__main__":
    asyncio.run(main())