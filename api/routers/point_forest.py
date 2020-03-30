from pydantic import Schema

import sys
sys.path.append('../')
from schemas import *
from cruds.domains.point_forest import PointForest

# @router.get("/search_in_the_forest", response_model=ImageForestSearch)
async def search_forest(*, coordinates: Coordinates):
    pf = PointForest(lat=coordinates.lat, lon=coordinates.lon)
    result = pf.get_result()
    return result
