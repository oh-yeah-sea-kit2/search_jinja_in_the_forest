import os

from google_aerial_photo import GoogleAerialPhoto
from yahoo_aerial_photo import YahooAerialPhoto
from judgment_in_the_forest import ForestJudgment
from image_check import equal_image

class PointForest:
  lat = None
  lon = None
  # model_file = "model/output_graph.pb"
  # label_file = "model/output_labels.txt"

  def __init__(self, lat: float, lon: float):
    self.lat = lat
    self.lon = lon

  # 小数点以下を７桁にあわせる
  def float_zfill(self, n:float):
    s = "{0:.7f}".format(n)
    return s
  
  # 緯度経度から航空写真を取得
  def get_aerial_photo(self, YAHOO_API_KEY, GOOGLE_API_KEY, save_dir):
    lat = self.lat
    lon = self.lon
    zoom_list = [18, 19, 20]
    source = 'yahoo'
    # save_dir = '../../'
    results = {}

    for zoom in zoom_list:
      # 保存先パス
      save_path = './data/cache/{lat}-{lon}-{zoom}_{source}.png'.format(
        lat=self.float_zfill(lat),lon=self.float_zfill(lon),zoom=zoom,source=source
      )
      # キャッシュを確認
      if not os.path.isfile(save_dir + save_path):
        print('Get from YAHOO')
        photo = YahooAerialPhoto(YAHOO_API_KEY)
        results = photo.get_all_aerial_photo(lat=lat,lon=lat, save_dir='../../')
      if zoom == 18:
        results[18] = save_dir + save_path
      elif zoom == 19:
        results[19] = save_dir + save_path
      elif zoom == 20:
        results[20] = save_dir + save_path
      
    # ３つの高度の航空写真を確認（同一画像になっていないこと）
    if equal_image(results[18], results[19]) or equal_image(results[18], results[20]):
      print('Get from GOOGLE')
      # Googleから取得
      photo = GoogleAerialPhoto(GOOGLE_API_KEY)
      results = photo.get_all_aerial_photo(lat=lat, lon=lat, save_dir='../../')
    
    if equal_image(results[18], results[19]) and equal_image(results[18], results[20]):
      return {
        'error': 'all image same',
        'detail': results,
      }
    elif equal_image(results[18], results[19]) or equal_image(results[18], results[20]):
      return {
        'error': 'two image same',
        'detail': results,
      }

    return results
  
  
  # 航空写真を機械学習判定
  def judgment_forest(self, file_name:str, model_file:str, label_file:str):
    fj = ForestJudgment(
      model_file=model_file,
      label_file=label_file,
    )
    result = fj.judgment_in_the_forest(file_name)
    return result

  # ３高度に対して判定した結果からレベルを判定
  def judgment_forest_level(self, judg_results):
    forest_count = 0
    for label, ratio in judg_results.items():
      if label == 'forest':
        forest_count += 1
    return forest_count

  def get_result(self,
    YAHOO_API_KEY, GOOGLE_API_KEY, save_dir,
    model_file, label_file):
    results = {}
    judg_results = {}
    # 緯度経度から航空写真を取得
    photos = self.get_aerial_photo(YAHOO_API_KEY, GOOGLE_API_KEY, save_dir)
    if ('error' in photos):
      results = {
        'level': None,
        'error': photos['error'],
        'detail': photos['detail'],
      }
      return results
    
    for zoom, photo in photos.items():
      # 航空写真を機械学習判定
      judg_result = self.judgment_forest(photo, model_file, label_file)
      judg_results[zoom] = judg_result
    # ３高度に対して判定した結果からレベルを判定
    result = self.judgment_forest_level(judg_results)
    results = {
      'level': result,
      'detail': judg_results
    }
    return results

if __name__ == '__main__':
  import pprint
  import os
  from os.path import join, dirname
  from dotenv import load_dotenv

  dotenv_path = join('../../'+dirname(__file__), '.env')
  load_dotenv(dotenv_path)
  save_dir = '../../'
  pf = PointForest(lat = 26.1549935,lon = 127.6885488)
  # result = pf.get_aerial_photo(os.environ.get("YAHOO_API_KEY"), os.environ.get("GOOGLE_API_KEY"), save_dir)
  # print(result)

  result = pf.get_result(
    os.environ.get("YAHOO_API_KEY"), os.environ.get("GOOGLE_API_KEY"), save_dir,
    save_dir + "./data/model/output_graph.pb",
    save_dir + "./data/model/output_labels.txt"
  )
  pprint.pprint(result)