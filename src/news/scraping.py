from bs4 import BeautifulSoup
import requests

def scrape():
    session = requests.Session()
    session.headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    url = 'https://www.birgun.net/guncel'
    main_url = 'https://www.birgun.net'
    content = session.get(url, verify=False).content

    for i in range(1,10):
        url_list = 'https://www.birgun.net/guncel?p={}'.format(i)
        soup = BeautifulSoup(content, "html.parser")
        first_news = soup.findAll("div", {"class": "aciklamali-haber haber"})
        total_text = ''

        print(url_list)
scrape()