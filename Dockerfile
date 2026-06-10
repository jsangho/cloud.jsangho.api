# 1. 파이썬 공식 이미지 가져오기
FROM python:3.13-slim

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 종속성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 나머지 소스 코드 전체 복사
COPY . .

# 5. FastAPI 실행 명령 (8000번 포트로 오픈)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
