from pydantic import BaseModel, validator

class Coordinates(BaseModel):
  lat: float
  lon: float
  @validator('lat')
  def lat_within_range(cls, v):
    if not -90 <= v <= 90:
      raise ValueError('Latitude outside allowed range')
    return v
  
  @validator('lon')
  def lon_within_range(cls, v):
    if not -180 <= v <= 180:
      raise ValueError('Longitude outside allowed range')
    return v

class ForestSearchDetail(BaseModel):
  label: str
  persent: float

class ForestSearchDetailZoomNumber(BaseModel):
  zoom_18: ForestSearchDetail
  zoom_19: ForestSearchDetail
  zoom_20: ForestSearchDetail

# search_jinja_in_the_forestの判定結果として返す構造体
class ImageForestSearch(BaseModel):
  result: int
  detail: ForestSearchDetailZoomNumber



