from fastapi import FastAPI
from src.setup import create_app


app: FastAPI = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app="run_http:app", host="0.0.0.0", port=8000, loop="uvloop")
