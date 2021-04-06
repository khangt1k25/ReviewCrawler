FROM python:3

WORKDIR usr/scr/app

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["scrapy", "crawl", "review", "-o", "result.json"]
