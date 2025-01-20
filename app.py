import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import random
import os

# 요청 함수: 재시도 및 딜레이 포함
def request_with_retry(session, url, headers, retries=3, delay=2):
    for attempt in range(retries):
        try:
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response
            else:
                time.sleep(delay + random.uniform(0, 1))  # 랜덤 딜레이
        except Exception as e:
            time.sleep(delay)
    raise Exception(f"요청 실패: {url}")

# 문피아 크롤러
def crawl_moonpia(novel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://novelpia.com",
        "Accept-Language": "ko-KR,ko;q=0.9",
    }
    session = requests.Session()
    response = request_with_retry(session, novel_url, headers)

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="chapter-link")

    novel_text = ""
    for chapter in chapters:
        chapter_url = chapter["href"]
        chapter_response = request_with_retry(session, chapter_url, headers)
        chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
        content = chapter_soup.find("div", class_="content").get_text("\n", strip=True)
        novel_text += f"{content}\n\n"
        time.sleep(random.uniform(1, 3))  # 요청 간 무작위 대기

    file_path = f"{title}_moonpia.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(novel_text)
    return file_path

# 네이버 시리즈 크롤러
def crawl_naver_series(novel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    }
    session = requests.Session()
    response = request_with_retry(session, novel_url, headers)

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="episode-link")

    novel_text = ""
    for chapter in chapters:
        chapter_url = chapter["href"]
        chapter_response = request_with_retry(session, chapter_url, headers)
        chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
        content = chapter_soup.find("div", class_="content").get_text("\n", strip=True)
        novel_text += f"{content}\n\n"
        time.sleep(random.uniform(1, 3))  # 요청 간 무작위 대기

    file_path = f"{title}_naver.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(novel_text)
    return file_path

# 노벨피아 크롤러
def crawl_novelpia(novel_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://novelpia.com",
    }
    session = requests.Session()
    response = request_with_retry(session, novel_url, headers)

    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.find("meta", property="og:title")["content"]
    chapters = soup.find_all("a", class_="chapter-link")

    novel_text = ""
    for chapter in chapters:
        chapter_url = chapter["href"]
        chapter_response = request_with_retry(session, chapter_url, headers)
        chapter_soup = BeautifulSoup(chapter_response.content, "html.parser")
        content = chapter_soup.find("div", class_="content").get_text("\n", strip=True)
        novel_text += f"{content}\n\n"
        time.sleep(random.uniform(1, 3))  # 요청 간 무작위 대기

    file_path = f"{title}_novelpia.txt"
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(novel_text)
    return file_path

# Streamlit 앱
st.title("소설 크롤러 및 TXT 변환기")
st.markdown("크롤링할 소설 사이트를 선택하고 링크를 입력하세요.")

# UI 구성
option = st.selectbox("크롤링할 사이트를 선택하세요:", ["문피아", "네이버 시리즈", "노벨피아"])
novel_url = st.text_input("소설 페이지 링크를 입력하세요:")

# 버튼 클릭 시 크롤링 시작
if st.button("크롤링 시작"):
    if not novel_url:
        st.error("소설 링크를 입력하세요.")
    else:
        try:
            # 크롤링 실행
            if option == "문피아":
                file_path = crawl_moonpia(novel_url)
            elif option == "네이버 시리즈":
                file_path = crawl_naver_series(novel_url)
            elif option == "노벨피아":
                file_path = crawl_novelpia(novel_url)
            else:
                st.error("유효하지 않은 옵션입니다.")
                file_path = None

            # 성공 시 다운로드 버튼 생성
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