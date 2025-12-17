import asyncio
from apify import Actor

from src.scraper import ImmobiliareScraper


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}

        max_pages = actor_input.get("max_items") or 1

        filters = {
            "municipality": actor_input.get("municipality"),
            "operation": actor_input.get("operation"),
            "min_price": actor_input.get("min_price"),
            "max_price": actor_input.get("max_price"),
            "min_size": actor_input.get("min_size"),
            "max_size": actor_input.get("max_size"),
            "min_rooms": actor_input.get("min_rooms"),
            "max_rooms": actor_input.get("max_rooms"),
            "bathrooms": actor_input.get("bathrooms"),
            "property_condition": actor_input.get("property_condition"),
            "floor": actor_input.get("floor"),
            "garage": actor_input.get("garage"),
            "heating": actor_input.get("heating"),
            "garden": actor_input.get("garden"),
            "terrace": actor_input.get("terrace"),
            "balcony": actor_input.get("balcony"),
            "lift": actor_input.get("lift"),
            "furnished": actor_input.get("furnished"),
            "cellar": actor_input.get("cellar"),
            "pool": actor_input.get("pool"),
            "exclude_auctions": actor_input.get("exclude_auctions"),
            "virtual_tour": actor_input.get("virtual_tour"),
            "keywords": actor_input.get("keywords"),
        }

        scraper = ImmobiliareScraper(filters=filters)
        await scraper.run(max_pages=max_pages)


if __name__ == "__main__":
    asyncio.run(main())
