from fastapi import FastAPI
from controllers import *
from images.router import search_forest
from images.schemas import ImageForestSearch

app = FastAPI(
    title='森の中の神社判定API',
    description='森の中にある神社かどうかを判定するよ！',
    version='0.1 beta'
)

# FastAPIのルーティング用関数
app.add_api_route('/', index)
# app.add_api_route("/search_in_the_forest", search_forest, response_model=ImageForestSearch)
app.add_api_route("/search_in_the_forest", search_forest, methods=['POST'])
