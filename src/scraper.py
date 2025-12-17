import asyncio
import random
from urllib.parse import urlencode, urlparse

from apify import Actor
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, Page
from typing import Dict, List

from src.config import REAL_USER_AGENT, VIEWPORT


class ImmobiliareScraper:
    BASE_URL = "https://www.immobiliare.it"

    def __init__(self, filters: Dict) -> None:
        self.filters = filters

    def build_url(self) -> str:
        municipality = (self.filters.get("municipality") or "Chieti").lower()
        operation = (self.filters.get("operation") or "vendita").lower()

        if operation == "buy":
            operation = "vendita"
        elif operation == "rent":
            operation = "affitto"

        base_path = f"/{operation}-case/{municipality}/"
        params: Dict[str, str | int] = {}

        if self.filters.get("min_price"):
            params["prezzoMinimo"] = self.filters["min_price"]
        if self.filters.get("max_price"):
            params["prezzoMassimo"] = self.filters["max_price"]
        if self.filters.get("min_size"):
            params["superficieMinima"] = self.filters["min_size"]
        if self.filters.get("max_size"):
            params["superficieMassima"] = self.filters["max_size"]
        if self.filters.get("min_rooms"):
            params["localiMinimo"] = self.filters["min_rooms"]
        if self.filters.get("max_rooms"):
            params["localiMassimo"] = self.filters["max_rooms"]
        if self.filters.get("bathrooms"):
            params["bagni"] = self.filters["bathrooms"]
        if self.filters.get("property_condition"):
            params["stato"] = self.filters["property_condition"]
        if self.filters.get("floor"):
            params["piano"] = self.filters["floor"]
        if self.filters.get("garage"):
            params["garage"] = self.filters["garage"]
        if self.filters.get("heating"):
            params["riscaldamento"] = self.filters["heating"]
        if self.filters.get("garden"):
            params["giardino"] = self.filters["garden"]
        if self.filters.get("terrace"):
            params["terrazzo"] = "terrazzo"
        if self.filters.get("balcony"):
            params["balcone"] = "balcone"
        if self.filters.get("lift"):
            params["ascensore"] = "1"
        if self.filters.get("furnished"):
            params["arredato"] = "on"
        if self.filters.get("cellar"):
            params["cantina"] = "1"
        if self.filters.get("pool"):
            params["piscina"] = "1"
        if self.filters.get("exclude_auctions"):
            params["noAste"] = "on"
        if self.filters.get("virtual_tour"):
            params["virtualTour"] = "1"
        if self.filters.get("keywords"):
            params["q"] = self.filters["keywords"]

        url = f"{self.BASE_URL}{base_path}"
        if params:
            url += f"?{urlencode(params)}"
        return url

    async def human_pause(self, min_sec: int = 2, max_sec: int = 4) -> None:
        await asyncio.sleep(random.uniform(min_sec, max_sec))

    async def extract_listing_links(self, page: Page) -> List[str]:
        selectors = [
            ".in-card",
            ".nd-list__item.in-realEstateResults__item",
            "article[class*='card']",
        ]

        working_selector = None
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, timeout=3000)
                working_selector = selector
                Actor.log.info(f"Using selector: {selector}")
                break
            except Exception:
                continue

        if not working_selector:
            return []

        links = await page.evaluate(
            f"""
        () => Array.from(
            document.querySelectorAll('{working_selector} a[href*="/annunci/"]')
        ).map(a => a.href)
        """
        )

        links = list(set(links))
        Actor.log.info(f"🔗 Annunci trovati: {len(links)}")
        return links

    async def scrape_listing(self, context, url: str) -> None:
        page = await context.new_page()
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await self.human_pause(3, 5)

            html = await page.content()
            soup = BeautifulSoup(html, "html.parser")

            title_el = soup.select_one("h1")
            price_el = soup.select_one("li.in-detail__mainFeaturesPrice")

            data = {
                "url": url,
                "title": title_el.get_text(strip=True) if title_el else "",
                "price": price_el.get_text(strip=True) if price_el else "",
            }

            await Actor.push_data(data)
            Actor.log.info(f"✅ Scraped: {data.get('title')}")
        except Exception as e:
            Actor.log.warning(f"⚠️ Errore su annuncio {url}: {e}")
        finally:
            await page.close()

    async def run(self, max_pages: int = 1) -> None:
        start_url = self.build_url()
        Actor.log.info(f"🏁 URL iniziale: {start_url}")

        async with async_playwright() as p:
            proxy_config = await Actor.create_proxy_configuration(groups=["RESIDENTIAL"])
            proxy_url = await proxy_config.new_url()
            parsed = urlparse(proxy_url)

            browser = await p.chromium.launch(
                headless=True,
                proxy={
                    "server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}",
                    "username": parsed.username,
                    "password": parsed.password,
                },
                args=["--disable-blink-features=AutomationControlled"],
            )

            context = await browser.new_context(
                viewport=VIEWPORT,
                user_agent=REAL_USER_AGENT,
                locale="it-IT",
            )

            page = await context.new_page()
            try:
                await page.goto(start_url, wait_until="networkidle", timeout=30000)
                await self.human_pause(3, 5)

                page_num = 1
                while page_num <= max_pages:
                    html = await page.content()
                    if "captcha" in html.lower():
                        Actor.log.error("❌ CAPTCHA rilevato sulla pagina lista, stop.")
                        break

                    links = await self.extract_listing_links(page)
                    if not links:
                        Actor.log.warning(f"Nessun annuncio trovato a pagina {page_num}")
                        break

                    for url in links:
                        await self.scrape_listing(context, url)
                        await self.human_pause(2, 4)

                    next_btn = await page.query_selector(
                        "a.pagination__next:not(.disabled)"
                    )
                    if not next_btn:
                        break

                    await next_btn.click()
                    await self.human_pause(4, 6)
                    page_num += 1

            finally:
                await browser.close()
