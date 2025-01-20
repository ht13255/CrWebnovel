import streamlit as st
import os
from novel_crawler import crawl_moonpia  # 문피아 크롤러
from webnovel_crawler import crawl_naver_series  # 네이버 시리즈 크롤러
from novelpia_crawler import crawl_novelpia  # 노벨피아 크롤러

st.title("소설 크롤러 및 TXT 변환기")

# 크롤러 선택
option = st.selectbox(
    "크롤링할 사이트를 선택하세요:",
    ["문피아", "네이버 시리즈", "노벨피아"]
)

# URL 입력
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