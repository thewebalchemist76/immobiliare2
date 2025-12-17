FROM apify/actor-python:3.11

# Copia requirements
COPY requirements.txt ./

# Installa dipendenze Python
RUN pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright
RUN python -m playwright install chromium

# Installa dipendenze di sistema per Playwright
RUN python -m playwright install-deps chromium

# Copia codice sorgente
COPY src ./src

# Avvio actor
CMD ["python", "-m", "src.main"]
