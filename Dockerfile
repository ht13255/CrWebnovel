FROM python:3.9-slim

# 필수 의존성 설치
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxi6 \
    libgconf-2-4 \
    libxrender1 \
    libxtst6 \
    libxrandr2 \
    libgtk-3-0 \
    google-chrome-stable

# 작업 디렉토리 설정
WORKDIR /app

# 코드 복사 및 의존성 설치
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Streamlit 실행
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]