import streamlit as st
import requests
from bs4 import BeautifulSoup
import os

st.title("소설 크롤러 및 TXT 변환기")

# 크롤링 함수들
def crawl_moonpia(novel_url):
    """문피아 크롤러"""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(novel_url, headers=headers)
    if response.status_code != 200:
        raise Exception("문피아 페이지에 접근할 수 없습니다.")
    
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="chapter-link")
    
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

def crawl_naver_series(novel_url):
    """네이버 시리즈 크롤러"""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(novel_url, headers=headers)
    if response.status_code != 200:
        raise Exception("네이버 시리즈 페이지에 접근할 수 없습니다.")
    
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="episode-link")
    
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

def crawl_novelpia(novel_url):
    """노벨피아 크롤러"""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(novel_url, headers=headers)
    if response.status_code != 200:
        raise Exception("노벨피아 페이지에 접근할 수 없습니다.")
    
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="chapter-link")
    
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

# Streamlit 인터페이스
option = st.selectbox(
    "크롤링할 사이트를 선택하세요:",
    ["문피아", "네이버 시리즈", "노벨피아"]
)

novel_url = st.text_input("소설 페이지 링크를 입력하세요:")

if st.button("크롤링 시작"):
    if not novel_url:
        st.error("소설 링크를 입력하세요.")
    else:
        try:
            if option == "문피아":
                file_path = crawl_moonpia(novel_url)
            elif option == "네이버 시리즈":
                file_path = crawl_naver_series(novel_url)
            elif option == "노벨피아":
                file_path = crawl_novelpia(novel_url)
            else:
                st.error("유효하지 않은 옵션입니다.")
                file_path = None
            
            if file_path:
                st.success(f"크롤링이 완료되었습니다: {file_path}")
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="다운로드",
                        data=file,
                        file_name=os.path.basename(file_path),
                        mime="text/plain"
                    )
        except Exception as e:
            st.error(f"오류 발생: {e}")

st.info("크롤링한 파일은 앱 종료 시 삭제될 수 있습니다. 저장을 원하시면 다운로드 버튼을 사용하세요.")