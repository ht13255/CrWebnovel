import streamlit as st
from PIL import Image
import pytesseract
import os
import requests
from bs4 import BeautifulSoup

st.title("소설 크롤러 및 이미지 OCR 변환기")

# 크롤링 및 OCR 기능 선택
option = st.selectbox(
    "기능을 선택하세요:",
    ["문피아 크롤링", "네이버 시리즈 크롤링", "노벨피아 크롤링", "이미지 텍스트 추출(OCR)"]
)

if option in ["문피아 크롤링", "네이버 시리즈 크롤링", "노벨피아 크롤링"]:
    # URL 입력
    novel_url = st.text_input("소설 페이지 링크를 입력하세요:")
    if st.button("크롤링 시작"):
        if not novel_url:
            st.error("소설 링크를 입력하세요.")
        else:
            try:
                # 크롤링 처리
                if option == "문피아 크롤링":
                    file_path = crawl_moonpia(novel_url)
                elif option == "네이버 시리즈 크롤링":
                    file_path = crawl_naver_series(novel_url)
                elif option == "노벨피아 크롤링":
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

elif option == "이미지 텍스트 추출(OCR)":
    # 이미지 업로드
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["png", "jpg", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드된 이미지", use_column_width=True)
        
        if st.button("텍스트 추출 시작"):
            try:
                # 이미지에서 텍스트 추출
                text = pytesseract.image_to_string(image, lang="kor+eng")
                
                # 추출된 텍스트 저장
                file_path = "extracted_text.txt"
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                
                st.success("텍스트 추출 완료!")
                st.text_area("추출된 텍스트", text, height=300)
                
                # 다운로드 버튼 제공
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="텍스트 다운로드",
                        data=file,
                        file_name="extracted_text.txt",
                        mime="text/plain"
                    )
            except Exception as e:
                st.error(f"오류 발생: {e}")

st.info("크롤링 및 OCR 변환이 완료된 후, 추출된 데이터를 다운로드하세요.")