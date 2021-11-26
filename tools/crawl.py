import os
import time

import requests
import bs4
from .tor import new_session, renew_connection
from .log_to_db import write
import json


def get_urls(data):
    urls = []
    for url in data.decode().split("<a href=\"http"):
        url = "http" + url.split("\"")[0]
        if "onion" not in url:
            continue
        else:
            urls.append(url)
    return urls


def index_words(data: bytes, urls):
    site = str(data).strip("b'").strip("'")
    soup = bs4.BeautifulSoup(site, features="html.parser")
    text = soup.text
    text = text.replace("\\r", "\n")
    text = str(text).split()
    for url in urls:
        try:
            text.remove(url)
        except ValueError:
            pass
        try:
            text.remove(url.replace("http:", ""))
        except ValueError:
            pass
        try:
            text.remove(url.replace("https:", ""))
            text.remove(url.replace(".onion", ""))
        except ValueError:
            pass

    index = []
    for i in text:
        word, count = i, text.count(i)
        try:
            text.remove(i)
        except ValueError:
            pass

        index.append({"word": word, "count": count})

    return index


def crawl_site(session: requests.Session, url: str) -> dict:
    site = session.get(url)
    data = site.content
    urls = get_urls(data)
    words = index_words(data, urls)
    write = {
        url: {
            "words": words,
            "urls": urls
        }
    }
    return write


def recursive_crawl(pickup=False):
    if not pickup:
        try:
            print("Attempting seed. ->", end="")
            seed = "http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion"

            session = new_session()

            seed_data = crawl_site(session, seed)

            urls = seed_data[seed]['urls']
            print(200)
        except requests.exceptions.ConnectionError:
            print("Seed request went wrong.")
            return
    else:
        session = new_session()
        print("Picking up based off of urls.txt thus no seeding required.")
        with open('urls.txt', 'r') as f:
            urls = json.loads(f.read())
    i = 0

    while bool(urls):
        url = urls.pop(0)
        try:
            i += 1
            if i == 10:
                previous_ip = session.get("https://httpbin.org/ip").json()['origin']
                print("Requesting new IP Address, Current IP: " + previous_ip)
                renew_connection()
                session = new_session()
                new_ip = session.get("https://httpbin.org/ip").json()['origin']
                print("Request completed, new IP Address: " + new_ip)

                i = 0
            print("Crawling site: " + url + " -> ", end="")
            site_data = crawl_site(session, url)
            urls += site_data[url]['urls']
            with open("urls.txt", 'w') as f:
                f.write(json.dumps(urls))
            write(url, site_data)
            print(200, end="")
            print(f", {len(urls)} urls remaining.")
        except requests.exceptions.ConnectionError:
            print(500)
            urls.append(url)
            time.sleep(2)
        except UnicodeDecodeError:
            print(501)
            with open('failed.txt', 'a') as f:
                f.write("\n" + url)
