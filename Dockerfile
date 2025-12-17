FROM apify/actor-python:3.11


# Install Playwright dependencies
RUN playwright install chromium


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY src ./src


CMD ["python", "-m", "src.main"]