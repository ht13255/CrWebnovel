# Python 베이스 이미지
FROM python:3.9-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y wget unzip curl gnupg \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Python 라이브러리 설치
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# 앱 복사 및 실행
COPY . /app
WORKDIR /app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]
