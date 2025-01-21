# streamlit_novelpia_selenium_crawler.py

import os
import time
import zipfile
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import streamlit as st

# Streamlit 설정
st.title("노벨피아 소설 크롤러")
st.write("Selenium을 사용해 동적 콘텐츠를 크롤링합니다.")

# 사용자 입력
url = st.text_input("소설 페이지 URL을 입력하세요:", "https://novelpia.com/novel/222765")
output_dir = "novel_contents"

if st.button("크롤링 시작"):
    if "novelpia.com" not in url:
        st.error("올바른 노벨피아 URL을 입력하세요.")
    else:
        try:
            # Chrome WebDriver 설정
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # 백그라운드 실행
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")

            service = Service("path/to/chromedriver")  # 크롬 드라이버 경로 설정
            driver = webdriver.Chrome(service=service, options=chrome_options)

            # 사이트 열기
            driver.get(url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "episode-item")))

            # 소설 기본 정보
            title = driver.title
            st.write(f"**소설 제목**: {title}")

            # 저장 디렉토리 확인 및 생성
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            # 화별 정보 가져오기
            episodes = driver.find_elements(By.CLASS_NAME, "episode-item")
            episode_links = []
            for ep in episodes:
                ep_title = ep.find_element(By.CLASS_NAME, "title").text
                ep_link = ep.find_element(By.TAG_NAME, "a").get_attribute("href")
                episode_links.append({"title": ep_title, "link": ep_link})

            # 각 화 크롤링 및 저장
            for idx, ep in enumerate(episode_links, start=1):
                st.write(f"크롤링 중: {ep['title']} ({idx}/{len(episode_links)})")

                # 각 화로 이동
                driver.get(ep["link"])
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "novel-content"))
                )

                # 화 내용 가져오기
                content = driver.find_element(By.CLASS_NAME, "novel-content").text

                # 파일로 저장
                file_path = os.path.join(output_dir, f"{idx:03d}_{ep['title']}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.write(f"{ep['title']} 저장 완료: {file_path}")

                # 딜레이 추가
                time.sleep(2)

            # ZIP 압축 생성
            zip_buffer = BytesIO()
            with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
                for file_name in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file_name)
                    zip_file.write(file_path, arcname=file_name)

            zip_buffer.seek(0)

            # 다운로드 버튼 추가
            st.success(f"모든 화 크롤링 완료! 다운로드 버튼을 클릭하세요.")
            st.download_button(
                label="소설 전체 다운로드 (ZIP)",
                data=zip_buffer,
                file_name=f"{title}.zip",
                mime="application/zip",
            )

            # 드라이버 종료
            driver.quit()

        except Exception as e:
            st.error(f"오류 발생: {e}")
