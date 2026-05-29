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
from core.database import (
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
from matrix.app.keymaker import get_keymaker
from friday13th.app.models.role import UserRole
from friday13th.app.schemas.user_schema import UserSchema
from friday13th.app.controllers.user_controller import UserController
from kayfabe.app.controllers.ple_controller import PleController
from titanic.adapter.inbound.api.v1.james_router import router as james_router
from titanic.adapter.inbound.api.v1.walter_router import router as walter_router
from kayfabe.app.exceptions import PleAuthRequiredError
from kayfabe.app.controllers.ranking_controller import RankingController
from kayfabe.app.controllers.result_controller import ResultController
from kayfabe.app.schemas.ple_schema import (
    BatchPredictionRequestSchema,
    BatchResultsRequestSchema,
    LinkPredictionsSchema,
    MatchResultUpdateSchema,
    PleAiStatsSchema,
    PleBoardSchema,
    PleEventSummarySchema,
    PleEventSyncSchema,
    PredictionRequestSchema,
)
from kayfabe.app.schemas.ranking_schema import RankingsResponseSchema
from kayfabe.app.schemas.result_schema import PleResultsResponse

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


class SignupRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., alias="userId", min_length=1, description="회원가입 ID")
    nickname: str = Field(..., min_length=1, description="회원가입 닉네임")
    email: str = Field(..., min_length=1, description="회원가입 이메일")
    password: str = Field(..., min_length=1, description="회원가입 비밀번호")
    password_confirm: str = Field(
        ...,
        alias="passwordConfirm",
        min_length=1,
        description="회원가입 비밀번호 확인",
    )


class SignupResponse(BaseModel):
    message: str
    nickname: str
    email: str
    role: UserRole


class LoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_id: str = Field(..., alias="userId", min_length=1, description="로그인 ID")
    password: str = Field(..., min_length=1, description="로그인 비밀번호")


class LoginResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: str
    id: int = Field(alias="userId", description="회원 DB id (예측·순위 연동)")
    login_id: str = Field(alias="loginId", description="로그인 ID")
    nickname: str
    email: str
    role: UserRole


class UserProfileResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(alias="userId")
    login_id: str = Field(alias="loginId")
    nickname: str
    email: str
    role: UserRole


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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(james_router)
app.include_router(walter_router)


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


def _ple_http_error(exc: Exception) -> HTTPException:
    if isinstance(exc, LookupError):
        return HTTPException(status_code=404, detail=str(exc) or "Not found")
    if isinstance(exc, PleAuthRequiredError):
        return HTTPException(status_code=401, detail=str(exc) or "로그인이 필요합니다.")
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail=str(exc))
    raise exc


@app.get(
    "/ple/events",
    response_model=list[PleEventSummarySchema],
    response_model_by_alias=True,
)
async def list_ple_events(db: AsyncSession = Depends(get_db)):
    """Neon에 동기화된 PLE 이벤트 목록."""
    return await PleController(db).list_events()


@app.get(
    "/ple/ai-stats",
    response_model=PleAiStatsSchema,
    response_model_by_alias=True,
)
async def get_ple_ai_stats(db: AsyncSession = Depends(get_db)):
    """AI 예측 누적 적중률·최근 채점 기록."""
    return await PleController(db).get_ai_stats()


@app.get(
    "/rankings",
    response_model=RankingsResponseSchema,
    response_model_by_alias=True,
)
async def list_rankings(
    limit: int = 120,
    nickname: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """
    PLE 승부예측 순위 (점수·적중률).
    경기 결과(ple_matches.winner_pick) 확정 시 pick 일치분이 자동 집계됩니다.
    nickname 쿼리로 내 순위(myRank)를 함께 조회할 수 있습니다.
    """
    return await RankingController(db).list_rankings(limit=limit, nickname=nickname)


@app.get(
    "/ple/{slug}",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def get_ple_board(
    slug: str,
    client_id: str | None = None,
    user_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """PLE 경기 보드(카드·사이트 투표·내 예측)."""
    try:
        return await PleController(db).get_board(
            slug, client_id=client_id, user_id=user_id
        )
    except LookupError as e:
        raise _ple_http_error(e) from e


@app.post(
    "/ple/{slug}/sync-from-client",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def sync_ple_from_client(
    slug: str,
    payload: PleEventSyncSchema,
    db: AsyncSession = Depends(get_db),
):
    """프론트 매치 카드를 Neon에 upsert."""
    if payload.slug != slug:
        raise HTTPException(status_code=400, detail="URL slug와 본문 slug가 일치하지 않습니다.")
    try:
        return await PleController(db).sync_event(payload)
    except ValueError as e:
        raise _ple_http_error(e) from e


@app.post(
    "/ple/link-predictions",
    response_model_by_alias=True,
)
async def link_ple_predictions(
    body: LinkPredictionsSchema,
    db: AsyncSession = Depends(get_db),
):
    """(레거시) 로그인 필수 정책 이후 신규 예측에는 사용하지 않습니다."""
    raise HTTPException(
        status_code=410,
        detail="예측은 로그인 후 저장됩니다. link-predictions API는 더 이상 사용하지 않습니다.",
    )


@app.post(
    "/ple/{slug}/predictions/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def predict_ple_batch(
    slug: str,
    body: BatchPredictionRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    """경기 예측 일괄 저장."""
    try:
        return await PleController(db).predict_batch(slug, body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@app.post(
    "/ple/{slug}/results/batch",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def set_ple_results_batch(
    slug: str,
    body: BatchResultsRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    """경기 결과 일괄 등록."""
    try:
        return await PleController(db).set_results_batch(slug, body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@app.post(
    "/ple/{slug}/matches/{match_key}/predict",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def predict_ple_match(
    slug: str,
    match_key: str,
    body: PredictionRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    """경기 예측 1회 저장 (Neon ple_predictions)."""
    try:
        return await PleController(db).predict(slug, match_key, body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@app.post(
    "/ple/{slug}/matches/{match_key}/result",
    response_model=PleBoardSchema,
    response_model_by_alias=True,
)
async def set_ple_match_result(
    slug: str,
    match_key: str,
    body: MatchResultUpdateSchema,
    db: AsyncSession = Depends(get_db),
):
    """경기 결과 등록·갱신 (Neon ple_matches)."""
    try:
        return await PleController(db).set_result(slug, match_key, body)
    except (LookupError, ValueError) as e:
        raise _ple_http_error(e) from e


@app.get("/ple/{slug}/live")
async def ple_live_board(
    slug: str,
    client_id: str,
    request: Request,
    user_id: int | None = None,
):
    """보드 스냅샷 SSE (예측·결과 반영)."""

    async def event_stream():
        if AsyncSessionLocal is None:
            yield f"data: {json.dumps({'error': 'DATABASE_URL not configured'})}\n\n"
            return
        try:
            while True:
                if await request.is_disconnected():
                    return
                try:
                    async with AsyncSessionLocal() as session:
                        board = await PleController(session).get_board(
                            slug, client_id=client_id, user_id=user_id
                        )
                        await rollback_readonly(session)
                except LookupError as e:
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
                    return
                except asyncio.CancelledError:
                    return
                payload = board.model_dump(mode="json", by_alias=True)
                yield f"data: {json.dumps(payload, default=str)}\n\n"
                try:
                    await asyncio.sleep(3)
                except asyncio.CancelledError:
                    return
        except asyncio.CancelledError:
            return

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@app.get("/doro/data")
def read_doro_data():
    raise HTTPException(
        status_code=410,
        detail="프로젝트 내부 파일(CSV) 읽기 기반 엔드포인트는 제거되었습니다.",
    )


@app.get("/results", response_model=PleResultsResponse)
async def list_ple_results(
    year: int = 2026,
    db: AsyncSession = Depends(get_db),
):
    controller = ResultController(db)
    return await controller.list_results(year)

#회원가입
@app.post("/signup", response_model=SignupResponse)
async def signup(req: SignupRequest, db: AsyncSession = Depends(get_db)):
    logger.info("[API] POST /signup — userId=%s", req.user_id)
    user_schema = UserSchema(
        login_id=req.user_id.strip(),
        nickname=req.nickname,
        email=req.email, 
        password=req.password,
        password_confirm=req.password_confirm,
        role=UserRole.USER,
    )

    user_controller = UserController(db)
    await user_controller.save_user(user_schema)

    return SignupResponse(
        message="회원가입이 완료되었습니다.",
        nickname=req.nickname,
        email=req.email,
        role=UserRole.USER,
    )


@app.post("/login", response_model=LoginResponse, response_model_by_alias=True)
async def login(req: LoginRequest, db: AsyncSession = Depends(get_db)):
    login_id = req.user_id.strip()
    logger.info("[API] POST /login — userId=%s", login_id)

    user_controller = UserController(db)
    user = await user_controller.login_user(login_id, req.password)

    return LoginResponse(
        message="로그인되었습니다.",
        id=user.id,
        login_id=user.login_id or login_id,
        nickname=user.nickname,
        email=user.email,
        role=UserRole(user.role),
    )


@app.get("/users/{user_id}", response_model=UserProfileResponse, response_model_by_alias=True)
async def get_user_profile(user_id: int, db: AsyncSession = Depends(get_db)):
    logger.info("[API] GET /users/%s", user_id)
    user_controller = UserController(db)
    user = await user_controller.get_user_by_id(user_id)
    return UserProfileResponse(
        id=user.id,
        login_id=user.login_id or "",
        nickname=user.nickname,
        email=user.email,
        role=UserRole(user.role),
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
