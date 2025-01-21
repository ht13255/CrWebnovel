# streamlit_novelpia_crawler_to_txt.py

import os
import time
import random
import requests
from bs4 import BeautifulSoup
import streamlit as st

# Streamlit 설정
st.title("노벨피아 소설 크롤러")
st.write("소설 내용을 크롤링하고 텍스트 파일로 저장합니다.")

# 사용자 입력
url = st.text_input("소설 페이지 URL을 입력하세요:", "https://novelpia.com/novel/222765")
output_dir = st.text_input("저장할 디렉토리:", "./novel_contents")

if st.button("크롤링 시작"):
    if "novelpia.com" not in url:
        st.error("올바른 노벨피아 URL을 입력하세요.")
    else:
        try:
            # 세션 초기화 및 헤더 설정 (우회)
            session = requests.Session()
            headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
                )
            }

            # 메인 페이지 요청
            response = session.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            # 소설 기본 정보
            title = soup.find("title").get_text(strip=True)
            st.write(f"**소설 제목**: {title}")

            # 저장 디렉토리 확인 및 생성
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 화별 정보 추출
            episodes = []
            for episode in soup.select(".episode-item"):
                episode_title = episode.select_one(".title").get_text(strip=True)
                episode_link = "https://novelpia.com" + episode.select_one("a")["href"]
                episodes.append({"title": episode_title, "link": episode_link})

            # 각 화 크롤링 및 저장
            for idx, ep in enumerate(episodes, start=1):
                st.write(f"크롤링 중: {ep['title']} ({idx}/{len(episodes)})")
                ep_response = session.get(ep["link"], headers=headers)
                ep_response.raise_for_status()
                ep_soup = BeautifulSoup(ep_response.text, "html.parser")

                # 화 내용 추출
                content = ep_soup.select_one(".novel-content").get_text(strip=True)

                # 파일로 저장
                file_path = os.path.join(output_dir, f"{idx:03d}_{ep['title']}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.write(f"{ep['title']} 저장 완료: {file_path}")

                # 딜레이 추가 (크롤링 방지 우회)
                time.sleep(random.uniform(2, 5))

            st.success(f"모든 화 크롤링 완료! 저장 경로: {output_dir}")

        except Exception as e:
            st.error(f"오류 발생: {e}")
