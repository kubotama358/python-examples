import requests
from pyquery import PyQuery as pq
import bs4
from urllib.request import urlopen
from lxml.html import fromstring

def main():
    search_word = "au"
    url = f"http://find.5ch.net/search?q={search_word}"
    res = requests.get(url)

    query = pq(res.text, parser='html')

    # soup = bs4.BeautifulSoup(res.text, "html.parser")
    # print(soup.title)
    list_obj = query(".list_line")
    for a in list_obj:
        pq_obj = pq(a)
        print(pq_obj(".list_line_link").attr('href'))

if __name__ == '__main__':
    main()