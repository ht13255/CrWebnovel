import streamlit as st
import requests
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
import time

# ChromeDriver 생성 함수
def create_chrome_driver():
    """ChromeDriver를 생성 및 초기화합니다."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # GUI 비활성화
    options.add_argument("--no-sandbox")  # 안전 모드 비활성화
    options.add_argument("--disable-dev-shm-usage")  # 메모리 부족 문제 해결
    options.add_argument("--disable-gpu")  # GPU 비활성화 (필요 시)
    options.add_argument("--remote-debugging-port=9222")  # 디버깅 포트
    options.add_argument("--log-level=3")  # 로그 레벨 낮춤

    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    except WebDriverException as e:
        st.error("ChromeDriver 초기화 실패. Chrome 및 ChromeDriver 버전을 확인하세요.")
        raise Exception(f"ChromeDriver 초기화 실패: {e}")

# Google Drive 파일 다운로드 함수
def download_from_drive(share_link, output_path):
    """Google Drive 공유 링크에서 파일을 다운로드합니다."""
    try:
        if "/d/" not in share_link:
            raise ValueError("올바르지 않은 Google Drive 공유 링크입니다.")
        file_id = share_link.split('/d/')[1].split('/')[0]
        download_url = f"https://drive.google.com/uc?id={file_id}&export=download"
        response = requests.get(download_url, stream=True)
        if response.status_code == 200:
            with open(output_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            return output_path
        else:
            raise Exception("Google Drive 링크가 유효하지 않습니다.")
    except Exception as e:
        raise Exception(f"Google Drive 다운로드 오류: {e}")

# YouTube 업로드 함수
def upload_to_youtube(file_path, title, description, visibility, email, password):
    """YouTube에 영상을 업로드합니다."""
    driver = create_chrome_driver()
    try:
        # YouTube 로그인 페이지로 이동
        driver.get("https://www.youtube.com/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Sign in']"))).click()

        # Google 계정 로그인
        email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_input.send_keys(email)
        email_input.send_keys(Keys.RETURN)

        time.sleep(2)  # 페이지 로드 대기
        password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='password']")))
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)

        # YouTube 업로드 페이지로 이동
        driver.get("https://www.youtube.com/upload")
        time.sleep(5)

        # 파일 업로드
        file_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
        file_input.send_keys(os.path.abspath(file_path))

        # 제목 입력
        title_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "textbox")))
        title_input.clear()
        title_input.send_keys(title)

        # 설명 입력
        description_box = driver.find_elements(By.ID, "textbox")[1]
        description_box.clear()
        description_box.send_keys(description)

        # 공개 상태 설정
        visibility_menu = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//tp-yt-paper-radio-button[@name='{visibility}']")))
        visibility_menu.click()

        # 업로드 완료 대기
        WebDriverWait(driver, 300).until(EC.text_to_be_present_in_element((By.XPATH, "//span[text()='Checks complete']"), "Checks complete"))

        st.success("YouTube 업로드가 성공적으로 완료되었습니다!")
    except TimeoutException:
        raise Exception("YouTube 업로드 과정에서 시간이 초과되었습니다.")
    except Exception as e:
        raise Exception(f"YouTube 업로드 오류: {e}")
    finally:
        driver.quit()

# Streamlit 앱 실행
def main():
    st.title("Google Drive to YouTube Uploader")
    st.markdown("이 앱은 Google Drive의 공유 링크에서 파일을 다운로드한 후 YouTube에 업로드합니다.")

    # 사용자 입력
    share_link = st.text_input("Google Drive 공유 링크:")
    title = st.text_input("YouTube 제목:")
    description = st.text_area("YouTube 설명:")
    visibility = st.selectbox("공개 상태 선택", options=["public", "private", "unlisted"], index=0)
    email = st.text_input("Google 이메일:")
    password = st.text_input("Google 비밀번호:", type="password")

    if st.button("업로드 시작"):
        try:
            st.write("Google Drive 파일 다운로드 중...")
            file_path = download_from_drive(share_link, "downloaded_video.mp4")
            st.success("파일 다운로드 완료!")

            st.write("YouTube 업로드 중...")
            upload_to_youtube(file_path, title, description, visibility, email, password)

            # 다운로드한 파일 삭제
            os.remove(file_path)
            st.success("작업 완료! 로컬 파일 삭제됨.")

        except Exception as e:
            st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()