import requests
from bs4 import BeautifulSoup
import os

def crawl_novelpia(novel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(novel_url, headers=headers)
    if response.status_code != 200:
        raise Exception("노벨피아 페이지에 접근할 수 없습니다.")
    
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("h1").get_text(strip=True)  # 제목을 가져옵니다.
    chapters = soup.find_all("a", class_="chapter-link")  # 각 장 링크 찾기
    
    novel_text = ""
    for chapter in chapters:
        chapter_url = chapter["href"]
        chapter_response = requests.get(chapter_url, headers=headers)
        chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
        content = chapter_soup.find("div", class_="content").get_text("\n", strip=True)
        novel_text += f"{content}\n\n"
    
    file_path = f"{title}.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(novel_text)
    
    return file_path