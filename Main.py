from tools.crawl import recursive_crawl
from tools.db import main


if __name__ == "__main__":
    if input("crawl/search ->") == "crawl":
        recursive_crawl(False)
    else:
        main()
