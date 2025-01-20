import streamlit as st
import requests
import os

# Google Drive 파일 다운로드 함수
def download_from_drive(share_link, output_path):
    """Google Drive 공유 링크에서 파일을 다운로드합니다."""
    try:
        # 공유 링크에서 파일 ID 추출
        if "/d/" not in share_link:
            raise ValueError("올바르지 않은 Google Drive 공유 링크입니다.")
        file_id = share_link.split('/d/')[1].split('/')[0]
        download_url = f"https://drive.google.com/uc?id={file_id}&export=download"

        # 파일 다운로드
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

# Streamlit 앱 실행
def main():
    st.title("Google Drive to YouTube Uploader without API or ChromeDriver")
    st.markdown("이 앱은 Google Drive에서 파일을 다운로드한 후 YouTube에 업로드를 안내합니다.")

    # 사용자 입력
    share_link = st.text_input("Google Drive 공유 링크:")
    title = st.text_input("YouTube 제목:")
    description = st.text_area("YouTube 설명:")

    if st.button("파일 다운로드"):
        try:
            # Google Drive 파일 다운로드
            st.write("Google Drive 파일 다운로드 중...")
            file_path = download_from_drive(share_link, "downloaded_video.mp4")
            st.success("파일 다운로드 완료! 파일 이름: downloaded_video.mp4")

            # 다운로드된 파일 경로 표시
            st.write("파일 경로:", os.path.abspath(file_path))

            # YouTube 업로드 안내
            st.markdown("### 유튜브 업로드 안내")
            st.write("YouTube 업로드 페이지로 이동하여 파일을 직접 업로드하세요:")
            st.markdown("[YouTube 업로드 링크](https://www.youtube.com/upload)")
            st.write("제목:", title)
            st.write("설명:", description)

            # 다운로드된 파일 삭제 옵션
            if st.checkbox("파일 삭제"):
                os.remove(file_path)
                st.success("로컬 파일 삭제 완료!")

        except Exception as e:
            st.error(f"오류 발생: {e}")

if __name__ == "__main__":
    main()