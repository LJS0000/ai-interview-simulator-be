# 공식 Python 런타임을 부모 이미지로 사용
FROM python:3.8-slim-buster

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /code

# 시스템 dependencies 설치
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
  build-essential \
  python3-dev \
  libpcre3-dev \
  gcc \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# dependencies 설치
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# 사용자 추가 및 권한 변경
RUN adduser --disabled-password --gecos '' myuser
RUN chown -R myuser:myuser /code
USER myuser

# 프로젝트 복사
COPY . .

# 8000포트 개방
EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]
