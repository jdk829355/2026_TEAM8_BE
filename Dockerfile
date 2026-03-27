# backend/Dockerfile
FROM python:3.13-slim

# 작업 디렉토리 설정
WORKDIR /app

# 시스템 의존성 설치 (PostgreSQL 관련 등 필요시)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# uv 설치 (가장 빠르고 공식적인 설치 방법)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 의존성 파일 복사 (pyproject.toml, uv.lock 등)
COPY pyproject.toml uv.lock* ./

# 가상환경 생성 및 의존성 설치
# --system 옵션을 주면 컨테이너 전역 파이썬 환경에 바로 설치하여 관리하기 편합니다.
# 하지만 uv의 강력한 격리 기능을 위해 가상환경을 만들고 uv run으로 실행하는 것을 권장합니다.
RUN uv sync --frozen --no-dev

# 애플리케이션 코드 복사
COPY . .

# 실행 명령어는 docker-compose.yml에서 덮어씁니다. (backend, worker, beat 역할 분리)