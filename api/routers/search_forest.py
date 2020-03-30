import sys
sys.path.append('../')
from schemas import Coordinates
from cruds.domains import PointForest
from setting import config

# @router.get("/search_in_the_forest", response_model=ImageForestSearch)
async def search_forest(*, coordinates: Coordinates):
    save_dir = './'

    pf = PointForest(lat=coordinates.lat, lon=coordinates.lon)
    result = pf.get_result(
        config['YAHOO_API_KEY'], config['GOOGLE_API_KEY'], save_dir,
        config['model_file'], config['label_file']
    )
    print(result)
    return result
