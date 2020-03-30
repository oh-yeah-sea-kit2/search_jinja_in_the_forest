from sqlalchemy import Column, String, DateTime, Float, Integer
from datetime import datetime

import sys
sys.path.append('../')
from db import Base


class PointAerialPhoto(Base):
  """
  PointAerialPhotoテーブル
  image_path  : 保存先のパス(主キー)
  lat         : 緯度
  lon         : 経度
  zoom_level  : zoom値
  source      : イメージ取得元
  date        : 取得時刻
  """
  __tablename__ = 'point_aerial_photo'
  image_path  = Column('image_path', String(256), primary_key=True)
  lat         = Column('lat', Float)
  lon         = Column('lon', Float)
  zoom_level  = Column('zoom_level', Integer)
  source      = Column('source', String(256))
  date        = Column('date', DateTime, default=datetime.now(), nullable=False)

  # 小数点以下を７桁にあわせる
  def float_zfill(self, n:float):
    s = "{0:.7f}".format(n)
    return s
  
  def __init__(self, 
    lat: float, lon: float, zoom_level: int, source: str, date: datetime = datetime.now()):
    
    self.image_path = './data/cache/{}-{}-{}_{}.png'.format(
      self.float_zfill(lat), self.float_zfill(lon),
      zoom_level, source
    )
    self.lat = lat
    self.lon = lon
    self.zoom_level = zoom_level
    self.source = source
    self.date = date

  def __str__(self):
    return self.image_path + \
      ': lat -> ' + str(self.lat) + \
      ', lon -> ' + str(self.lon) + \
      ', zoom_level -> ' + str(self.zoom_level) + \
      ', source -> ' + self.source + \
      ', date -> ' + self.date.strftime('%Y/%m/%d - %H:%M:%S')

