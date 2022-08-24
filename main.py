import requests
import bs4
import fake_headers
from datetime import datetime


def get_full_text_habr_article(url):
    headers = fake_headers.Headers(
        # generate any browser & os headeers
        headers=False  # don`t generate misc headers
    )

    response = requests.get(url=url, headers=headers.generate())
    response.raise_for_status()
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")

    article = soup.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-2")
    if article is None:
        article = soup.find(class_="article-formatted-body article-formatted-body article-formatted-body_version-1")

    res = ""

    article_headers = article.find_all("h2")

    article_headers = " ".join(article_header.text for article_header in article_headers)

    res += article_headers

    article_paragraphs = article.find_all("p")
    article_paragraphs = " ".join(article_paragraph.text for article_paragraph in article_paragraphs)

    res += article_paragraphs

    return res


if __name__ == '__main__':

    # определяем список ключевых слов
    KEYWORDS = ['дизайн', 'фото', 'web', 'python', 'RamDisk']

    url = "https://habr.com/ru/all/"

    headers = fake_headers.Headers(
        # generate any browser & os headeers
        headers=False  # don`t generate misc headers
    )

    response = requests.get(url=url, headers=headers.generate())
    response.raise_for_status()
    text = response.text

    soup = bs4.BeautifulSoup(text, features="html.parser")

    articles = soup.find_all("article")

    res = []
    for article in articles:


        title = article.find(class_="tm-article-snippet__title tm-article-snippet__title_h2").find("span").text


        href = article.find(class_="tm-article-snippet__readmore").attrs["href"]
        url_article = "https://habr.com" + href

        #print(title)
        try: #встречаются статьи с алтернативной версткой. в них текст превью не в <p>, а в <br>. В названии класса другая версия
            paragraphs = article.find(
                class_="article-formatted-body article-formatted-body article-formatted-body_version-2").find_all("p")
        except AttributeError:
            paragraphs = article.find(
                class_="article-formatted-body article-formatted-body article-formatted-body_version-1").find_all("br")

        #print(paragraphs)

        text_preview = " ".join(paragraph.text for paragraph in paragraphs)

        keyword_founded = False
        for keyword in KEYWORDS:
            if keyword in text_preview or keyword in title:
                keyword_founded = True
                break
        else:  # если в превью и названии ключевых слов не обнаружено, то открываем и проводим поиск по всей статье
            text_full = get_full_text_habr_article(url_article)
            for keyword in KEYWORDS:
                if keyword in text_full:
                    keyword_founded = True
                    break


        if keyword_founded:
            date = article.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"].split(
                ",")
            date = date[0]
            # date = datetime.strptime(date[0], '%Y-%m-%d')
            # title = "2022-08-24, 20:46" > сегодня
            print ( f"<{date}> - <{title}> - <{url_article}>")
