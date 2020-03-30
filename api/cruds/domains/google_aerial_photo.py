import urllib
import urllib.error
import urllib.request

class GoogleAerialPhoto:
  API_KEY = None

  def __init__(self, API_KEY):
    self.API_KEY = API_KEY
  
  # 小数点以下を７桁にあわせる
  def float_zfill(self, n:float):
    s = "{0:.7f}".format(n)
    return s

  def get_all_aerial_photo(self, lat: float, lon: float, save_dir: str):
    zoom_list = [18, 19, 20]
    result_list = {}
    for zoom in zoom_list:
      res = self.get_aerial_photo(lat, lon, zoom, save_dir)
      result_list['zoom_{}'.format(zoom)] = res
    return result_list

  def get_aerial_photo(self, lat: float, lon: float, zoom: int, save_dir: str):
    maptype = 'satellite' # hybrid
    # url = "https://map.yahooapis.jp/map/V1/static?appid={ap}&lat={lat}&lon={lon}&z={zoom}&mode=photo".format(
    url = "https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&maptype={maptype}&size=500x500&zoom={zoom}&key={key}".format(
      key=self.API_KEY,
      lat=str(lat),
      lon=str(lon),
      zoom=str(zoom),
      maptype=maptype,
    )
    print(url)
    save_path = './data/cache/{}-{}-{}_{}.png'.format(
      self.float_zfill(lat), self.float_zfill(lon),
      zoom, 'google'
    )
    dst_path = save_dir + save_path

    try:
      data = urllib.request.urlopen(url).read()
      with open(dst_path, mode="wb") as f:
        f.write(data)
    except urllib.error.URLError as e:
      print('Download Error : ')
      print(e)
      # 本当はリトライ３回くらいしたいけどとりあえず
    return save_path


if __name__ == '__main__':
  import os
  from os.path import join, dirname
  from dotenv import load_dotenv

  dotenv_path = join('../../'+dirname(__file__), '.env')
  load_dotenv(dotenv_path)

  photo = GoogleAerialPhoto(os.environ.get("GOOGLE_API_KEY"))
  # result = photo.get_aerial_photo(
  #   lat = 26.1549935,
  #   lon = 127.6885488,
  #   zoom=20,
  #   save_dir='../../',
  # )
  result = photo.get_all_aerial_photo(
    lat = 26.1549935,
    lon = 127.6885488,
    save_dir='../../',
  )
  print(result)
