# Immobiliare.it Scraper

Scraper completo per Immobiliare.it con supporto per tutti i filtri disponibili sul sito.

## Features

✅ Tutti i filtri di ricerca (prezzo, dimensione, locali, bagni, etc.)
✅ Filtri avanzati (terrazzo, balcone, ascensore, arredato, cantina, piscina)
✅ Paginazione automatica
✅ Export dati strutturati
✅ Deploy su Apify

## Filtri disponibili

- Città/Comune
- Vendita/Affitto
- Prezzo min/max
- Superficie min/max (m²)
- Locali min/max
- Bagni
- Stato immobile
- Piano
- Garage/Posto auto
- Riscaldamento
- Giardino
- Terrazzo (sì/no)
- Balcone (sì/no)
- Ascensore (sì/no)
- Arredato (sì/no)
- Cantina (sì/no)
- Piscina (sì/no)
- Escludi aste
- Virtual tour
- Parole chiave

## Setup locale
```bash
# Clone repository
git clone <your-repo-url>
cd immobiliare-scraper

# Install dependencies
pip install -r requirements.txt

# Install Playwright
playwright install chromium

# Run scraper
python -m src.main
```

## Deploy su Apify

1. Crea un nuovo Actor su Apify
2. Collega questo repository GitHub
3. Apify farà auto-deploy ad ogni push

## Output

I dati vengono salvati con questa struttura:
```json
{
  "title": "Appartamento in Via Roma",
  "price": "€ 250.000",
  "location": "Roma, Centro",
  "rooms": 3,
  "bathrooms": 2,
  "surface_sqm": 85,
  "features": "3 locali, 2 bagni, 85 m²",
  "url": "https://www.immobiliare.it/...",
  "image_url": "https://...",
  "listing_id": "123456",
  "scraped_at": "2025-12-16T15:00:00Z"
}
```

## Note legali

⚠️ Questo scraper è per scopi educativi. Lo scraping di Immobiliare.it potrebbe violare i loro Terms of Service. Usa a tuo rischio.
```

---

## Struttura finale:
```
immobiliare-scraper/
├── src/
│   ├── __init__.py          ✅
│   ├── main.py              ✅
│   ├── scraper.py           ✅
│   └── config.py            ✅
├── .actor/
│   ├── actor.json           ✅
│   └── input_schema.json    ✅
├── Dockerfile               ✅
├── requirements.txt         ✅
├── .gitignore               ✅
└── README.md                ✅# immobiliare2
