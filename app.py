import os
import time
import zipfile
from io import BytesIO
import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
import shutil


# Headless Chrome 바이너리 설치
def install_headless_chrome():
    """Headless Chrome 바이너리를 다운로드하고 실행 경로를 설정합니다."""
    chrome_url = "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb"
    chrome_deb = "/tmp/google-chrome-stable_current_amd64.deb"

    # Chrome 바이너리 다운로드
    if not os.path.exists(chrome_deb):
        st.write("Headless Chrome 바이너리를 다운로드 중...")
        subprocess.run(["wget", chrome_url, "-O", chrome_deb], check=True)

    # Chrome 바이너리 설치
    st.write("Headless Chrome을 설치 중...")
    result = subprocess.run(["dpkg", "-i", chrome_deb], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        st.write("의존성 설치 중...")
        subprocess.run(["apt-get", "-f", "install", "-y"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Selenium ChromeDriver 초기화
def init_driver():
    """Selenium ChromeDriver를 초기화합니다."""
    chrome_path = shutil.which("google-chrome")
    if not chrome_path:
        raise ValueError("Chrome 브라우저를 찾을 수 없습니다. 설치를 확인하세요.")

    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 브라우저를 백그라운드에서 실행
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # ChromeDriver 서비스 초기화
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


# Streamlit 앱 설정
st.title("노벨피아 소설 크롤러")
st.write("Selenium을 사용하여 노벨피아 소설을 크롤링합니다.")

# Headless Chrome 설치 실행
try:
    install_headless_chrome()
except Exception as e:
    st.error(f"Headless Chrome 설치 중 오류 발생: {e}")

# 사용자 입력
url = st.text_input("소설 페이지 URL을 입력하세요:", "https://novelpia.com/novel/222765")
output_dir = "novel_contents"

if st.button("크롤링 시작"):
    if not url or "novelpia.com" not in url:
        st.error("올바른 노벨피아 URL을 입력하세요.")
    else:
        try:
            # Selenium 드라이버 초기화
            driver = init_driver()
            driver.get(url)

            # 소설 제목 가져오기
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
                time.sleep(2)  # 대기 시간 추가 (크롤링 방지 우회)

                # 화 내용 가져오기
                content = driver.find_element(By.CLASS_NAME, "novel-content").text

                # 파일로 저장
                file_path = os.path.join(output_dir, f"{idx:03d}_{ep['title']}.txt")
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.write(f"{ep['title']} 저장 완료: {file_path}")

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

            # Selenium 드라이버 종료
            driver.quit()

        except Exception as e:
            st.error(f"오류 발생: {e}")
