FROM apify/actor-python:3.11

# Copia requirements
COPY requirements.txt ./

# Installa dipendenze Python (QUI arriva playwright)
RUN pip install --no-cache-dir -r requirements.txt

# Installa browser Playwright
RUN python -m playwright install chromium

# Copia codice
COPY src ./src

# Avvio actor
CMD ["python", "-m", "src.main"]
