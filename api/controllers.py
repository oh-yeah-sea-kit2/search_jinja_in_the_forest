from starlette.requests import Request

def index(request: Request):
    return {"test": "Hello"}
