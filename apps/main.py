from fastapi import FastAPI

try:
    from titanic.app.james import James
except ModuleNotFoundError:
    from apps.titanic.app.james import James

try:
    from doro.app.doro_director import DoroDirector
except ModuleNotFoundError:
    from apps.doro.app.doro_director import DoroDirector

app = FastAPI(title="JSangHo Main Page")

@app.get("/")
def root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}

@app.get("/titanic/data")
def read_titanic_data():
    james = James()
    df = james.get_data()

    return df.to_dict(orient="records")

@app.get("/doro/data")
def read_doro_data():
    dd = DoroDirector()
    df = dd.get_data()

    return df.to_dict(orient="records")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("apps.main:app", host="127.0.0.1", port=8000, reload=True)