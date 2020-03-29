from .schemas import Coordinates
from pydantic import Schema

# @router.get("/search_in_the_forest", response_model=ImageForestSearch)
async def search_forest(*, coordinates: Coordinates):
    # 緯度経度から航空写真を取得
    # 航空写真を機械学習判定
    # ３高度に対して判定した結果からレベルを判定
    return {
        'lat': coordinates.lat,
        'lon': coordinates.lon,
    }
