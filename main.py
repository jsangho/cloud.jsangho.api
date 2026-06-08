import asyncio
import json
import logging
import os
import sys
from contextlib import asynccontextmanager

if sys.platform == "win32":
    # Anaconda(numpy/scipy) + uvicorn --reload 종료 시 forrtl error (200) 방지
    os.environ.setdefault("FOR_DISABLE_CONSOLE_CTRL_HANDLER", "1")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# `backend/apps/*`를 최상위 패키지로 import 하기 위한 경로 보정
# (PowerShell에서 PYTHONPATH 설정 없이도 `python -m uvicorn main:app` 실행 가능)
_APPS_DIR = os.path.join(os.path.dirname(__file__), "apps")
if _APPS_DIR not in sys.path:
    sys.path.insert(0, _APPS_DIR)

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.ext.asyncio import AsyncSession

from imitation_game.adapter.db_health_adapter import DbHealthAdapter
from core.matrix.grid_oracle_database_manager import (
    AsyncSessionLocal,
    attach_neon_sql_logging,
    configure_db_logging,
    dispose_engine,
    engine,
    get_db,
    init_db,
    rollback_readonly,
)
from social_network.app.doro_director import DoroDirector
from core.matrix.vault_keymaker_secret_manager import get_keymaker
from friday13th.adapter.inbound.api import friday13th_router
from kayfabe.adapter.inbound.api import kayfabe_router
from titanic.adapter.inbound.api import titanic_router
keymaker = get_keymaker()
logger = logging.getLogger("uvicorn.error")


class ChatRequest(BaseModel):
    """채팅 요청 본문. 사용자 메시지를 JSON으로 전달합니다."""

    message: str = Field(..., min_length=1, description="사용자 메시지")


class ChatResponse(BaseModel):
    reply: str


class SeoulWeatherResponse(BaseModel):
    city: str
    temp_c: float
    description: str
    condition_id: int


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_db_logging()
    if engine is not None:
        attach_neon_sql_logging(engine)
    try:
        await init_db()
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="Jsangho Main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(titanic_router)
app.include_router(friday13th_router)
app.include_router(kayfabe_router)


@app.middleware("http")
async def log_auth_requests(request: Request, call_next):
    """로그인·회원가입 요청이 들어오면 uvicorn 터미널에 먼저 표시합니다."""
    if request.url.path in ("/login", "/signup") and request.method == "POST":
        logger.info("[API] %s %s", request.method, request.url.path)
    return await call_next(request)


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}

@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    """
    JSON 본문 `{"message": "..."}` 를 받아 Gemini 답변 문자열을 반환합니다.
    """
    if not keymaker.is_gemini_ready():
        if not keymaker.get_gemini_api_key():
            raise HTTPException(
                status_code=503,
                detail="GEMINI_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
            )
        raise HTTPException(
            status_code=503,
            detail=(
                "Gemini 패키지가 설치되지 않았습니다. "
                "backend 폴더에서 `pip install -r requirements.txt` 후 서버를 재시작하세요."
            ),
        )

    model = keymaker.get_gemini_model()
    try:
        response = model.generate_content(req.message)
    except Exception as e:
        err = str(e)
        if "429" in err or "quota" in err.lower() or "ResourceExhausted" in type(e).__name__:
            raise HTTPException(
                status_code=429,
                detail=(
                    "Gemini API 무료 할당량을 초과했거나, 이 프로젝트에 무료 할당량이 "
                    "활성화되지 않았습니다(limit: 0). "
                    "1~2분 후 다시 시도하거나, "
                    "https://aistudio.google.com/apikey 에서 새 키를 발급하고 "
                    "https://ai.dev/rate-limit 에서 사용량을 확인하세요. "
                    "계속되면 Google AI Studio에서 결제(빌링) 연결 후 무료 한도가 켜집니다."
                ),
            ) from e
        raise HTTPException(
            status_code=502,
            detail=f"Gemini 호출 실패: {e!s}",
        ) from e

    try:
        text = (response.text or "").strip()
    except ValueError as e:
        feedback = getattr(response, "prompt_feedback", None)
        raise HTTPException(
            status_code=400,
            detail=f"응답 텍스트를 읽을 수 없습니다: {e!s}. prompt_feedback={feedback}",
        ) from e

    if not text:
        reason = None
        if getattr(response, "candidates", None):
            c0 = response.candidates[0]
            reason = getattr(c0, "finish_reason", None)
        raise HTTPException(
            status_code=502,
            detail=(
                "모델이 비어 있는 응답을 반환했습니다."
                + (f" (finish_reason={reason})" if reason else "")
            ),
        )

    return ChatResponse(reply=text)


@app.get("/weather/seoul", response_model=SeoulWeatherResponse)
def read_seoul_weather() -> SeoulWeatherResponse:
    """OpenWeatherMap으로 서울 현재 기온·날씨를 조회합니다 (`OPENWEATHER_API_KEY`)."""
    if not keymaker.is_openweather_ready():
        raise HTTPException(
            status_code=503,
            detail="OPENWEATHER_API_KEY가 설정되지 않았습니다. backend/.env 에 키를 넣어 주세요.",
        )
    try:
        data = keymaker.get_seoul_current_weather()
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=502, detail=str(e)) from e
    return SeoulWeatherResponse(**data)


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await DbHealthAdapter.neon_time_check(db)


@app.get("/doro/data")
def read_doro_data():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 파일(CSV) 읽기 기반 엔드포인트는 제거되었습니다.",
    )


if __name__ == "__main__":
    import uvicorn

    # Windows: --reload 시 WatchFiles가 프로세스를 끊을 때 forrtl/libifcoremd 충돌 발생
    use_reload = sys.platform != "win32"

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    config = uvicorn.Config(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=use_reload,
        loop="asyncio",
    )
    server = uvicorn.Server(config)
    try:
        asyncio.run(server.serve())
    except KeyboardInterrupt:
        logger.info("서버를 종료했습니다.")
