import streamlit as st
import os

def main():
    st.title("YouTube File Uploader without Automation or API")
    st.markdown(
        "이 앱은 사용자가 로컬 파일 경로를 입력하고, YouTube 업로드 링크를 제공합니다. "
        "자동화 없이 수동 업로드를 지원합니다."
    )

    # 파일 경로 입력
    file_path = st.text_input("업로드할 파일 경로를 입력하세요 (예: /path/to/video.mp4):")
    title = st.text_input("YouTube 제목:")
    description = st.text_area("YouTube 설명:")
    visibility = st.selectbox("공개 상태 선택", options=["public", "private", "unlisted"], index=0)

    # 파일 확인
    if st.button("파일 확인"):
        if not os.path.exists(file_path):
            st.error("파일이 존재하지 않습니다. 경로를 확인하세요.")
        else:
            file_size = os.path.getsize(file_path)
            st.success(f"파일이 확인되었습니다: {file_path}")
            st.write(f"파일 크기: {file_size / (1024 * 1024):.2f} MB")

    # YouTube 업로드 안내
    if st.button("YouTube 업로드 안내"):
        if not os.path.exists(file_path):
            st.error("유효한 파일 경로를 입력하세요.")
        else:
            st.success("YouTube 업로드 준비 완료!")
            st.markdown("### YouTube 업로드 안내")
            st.write("다음 정보를 사용하여 YouTube 업로드를 완료하세요:")
            st.markdown("[YouTube 업로드 링크](https://www.youtube.com/upload)")
            st.write("**제목:**", title)
            st.write("**설명:**", description)
            st.write("**공개 상태:**", visibility)

if __name__ == "__main__":
    main()