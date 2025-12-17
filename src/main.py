import asyncio
from apify import Actor
from src.scraper import ImmobiliareScraper




async def main():
async with Actor:
actor_input = await Actor.get_input() or {}


filters = {
"municipality": actor_input.get("municipality", "roma"),
"operation": actor_input.get("operation", "vendita"),
}


max_pages = actor_input.get("max_pages", 3)


scraper = ImmobiliareScraper(filters)
await scraper.run(max_pages=max_pages)




if __name__ == "__main__":
asyncio.run(main())