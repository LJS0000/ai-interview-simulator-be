# Set base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project to container
COPY . /code/

# Create a non-root user and change ownership of the files
RUN useradd -m uwsgiuser && chown -R uwsgiuser /code

# Switch to the new user
USER uwsgiuser

## 파라미터 정리
# FROM: base image 설정. 컨테이너의 시작점.
# RUN: 빌드 프로세스 중에 명령을 실행. 패키지를 설치하거나 필요한 설정 작업을 실행.
# COPY: 호스트에서 컨테이너의 파일 시스템으로 파일을 복사. 애플리케이션 코드를 추가하는 데 적합.
# WORKDIR: 컨테이너 내의 작업 디렉터리를 설정. 후속 명령은 이 위치에서 실행.
# EXPOSE: 컨테이너 포트 지정.
# CMD: 컨테이너의 실행 명령어. 리스트 형태.
# ENV: 컨테이너 환경변수 설정.
# ARG: build-time 인수를 정의. ex)ARG VERSION=latest
# ENTRYPOINT: CMD와 유사하며, d 컨테이너에 대한 진입점을 제공.
# ADD: COPY와 비슷하지만 URL을 처리하고 아카이브의 압축을 자동으로 품.
# VOLUME: 컨테이너 외부에서 데이터를 유지할 수 있는 'VOLUME'을 생성.
# USER: 컨테이너를 실행할 때 사용할 사용자를 지정. 루트로 실행하지 않도록 하여 보안을 강화.
# LABLE: 키-값 형식으로 이미지에 메타데이터를 추가. 이미지 버전 관리 및 문서화.
# ARG: ENV와 유사하지만 빌드 시간 동안에만 사용.
# ONBUILD: 이미지가 다른 이미지의 base로 사용될 때 명령을 실행.
# STOPSIGNAL: 컨테이너를 정상적으로 중지하기 위해 보낼 시스템 호출 신호를 설정.
# HEALTHCHECK: 컨테이너의 상태를 확인하는 명령을 정의. 앱의 상태를 모니터링.
# SHELL: RUN, CMD 및 ENTRYPOINT에서 사용하는 기본 shell을 재정의
# .dockerignore: .gitignore처럼 작동하여 이미지에서 파일을 제외.

