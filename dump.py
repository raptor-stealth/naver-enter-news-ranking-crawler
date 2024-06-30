import os
from datetime import datetime
import json
from openai import OpenAI
from typing import List, Dict

import bs4
from bs4 import BeautifulSoup as bs
import selenium
from selenium.webdriver.common.by import By
from tqdm import tqdm

from selenium_utils import (
    load_chrome_driver,
)


def parse_article(
    article: bs4.element.Tag,
) -> Dict[str, str]:
    rank = article.select("div > span > em")[0].text.strip()
    thumbnail = article.select("a > img")[0].get("src").strip()
    title = article.select("div > a")[0].text.strip()
    snippet = article.select("div > p")[0].text.strip()
    return {
        "rank": rank,
        "thumbnail": thumbnail,
        "title": title,
        "snippet": snippet,
    }


def generate_query_with_openai(
    articles: List[Dict[str, str]],
    model_name: str = "gpt-3.5-turbo",
) -> List[Dict[str, str]]:
    def build_prompt(article):
        prompt = ""
        prompt += "다음 제목과 내용을 보고 검색에 적절한 대표적인 검색어로 하나만 추천해줘.\n\n"
        zeroshot = {
            "title": "12세 삼둥이, 185㎝ 父 송일국 따라잡겠네‥아가에서 장정된 폭풍 성장(유퀴즈)",
            "snippet": " 배우 송일국이 삼둥이(대한, 민국, 만세) 아들의 폭풍 성장 근황을 공개했다. 6월 29일 tvN ‘유 퀴즈 온 더 블럭’ 채널에는 “삼둥이 아…",
            "query": "송일국 삼둥이 근황",
        }
        prompt += "제목: {}\n문서: {}\n검색어: {}\n".format(zeroshot['title'], zeroshot['snippet'], zeroshot['query'])
        prompt += "제목: {}\n문서: {}\n검색어: ".format(article['title'], article['snippet'])
        return prompt

    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    api_responses = [
        client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": build_prompt(article)}],
        ) for article in tqdm(articles)]
    queries = [response.choices[0].message.content for response in api_responses]
    for article, query in zip(articles, queries):
        article['query'] = query

    return articles


def parse_html(
    driver: selenium.webdriver.chrome.webdriver.WebDriver,
    url: str,
):
    now = datetime.now().strftime("%y%m%d-%H%M%S")

    driver.get(url)
    left_cont = driver.find_element(By.CLASS_NAME, "left_cont")
    html = left_cont.get_attribute('outerHTML')
    soup = bs(html, "html.parser")
    articles = soup.select("ul > li")
    articles = [parse_article(article) for article in articles]
    articles = generate_query_with_openai(articles)
    json.dump(articles, open(now+".json", "w"), ensure_ascii=False, indent=4)


if __name__ == "__main__":
    URL = "https://entertain.naver.com/ranking"
    # URL = "https://entertain.naver.com/ranking/five"

    driver = load_chrome_driver(headless=False)
    parse_html(driver, URL)
