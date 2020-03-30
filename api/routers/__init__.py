from fastapi import FastAPI

from .search_forest import *

import sys
sys.path.append('../')
from schemas import Coordinates, ImageForestSearch

app = FastAPI(
    title='森の中の神社判定API',
    description='森の中にある神社かどうかを判定するよ！',
    version='0.1 beta'
)

# app.add_api_route("/search_in_the_forest", search_forest, methods=['POST'])
app.add_api_route("/search_in_the_forest", search_forest, methods=['POST'], response_model=ImageForestSearch)
