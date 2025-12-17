import asyncio


links = await page.evaluate("""
() => Array.from(
document.querySelectorAll('a[href*="/annunci/"]')
).map(a => a.href)
""")


links = list(set(links))
Actor.log.info(f"🔗 Annunci trovati: {len(links)}")


for url in links:
await self.scrape_listing(context, url)


next_btn = await page.query_selector('a.pagination__next:not(.disabled)')
if not next_btn:
break


await next_btn.click()
await self.human_pause(4, 6)
page_num += 1


await browser.close()


async def scrape_listing(self, context, url: str):
page = await context.new_page()


try:
await page.goto(url, wait_until="networkidle")
await self.human_pause(3, 5)


html = await page.content()
soup = BeautifulSoup(html, "html.parser")


data = {
"url": url,
"title": soup.select_one("h1") and soup.select_one("h1").get_text(strip=True),
"price": soup.select_one("li.in-detail__mainFeaturesPrice")
and soup.select_one("li.in-detail__mainFeaturesPrice").get_text(strip=True),
}


await Actor.push_data(data)
Actor.log.info(f"✅ Scraped: {data.get('title')}")


except Exception as e:
Actor.log.warning(f"⚠️ Errore su annuncio: {e}")


finally:
await page.close()