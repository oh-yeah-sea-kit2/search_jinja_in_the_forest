# search_jinja_in_the_forest

## 現在開発環境構築中…
- Dockerコンテナを変えたほうがいいかも…
- ConohaVPSで動かすことを想定するとコンテナは別のもののほうが良さげ

## 判定実行
- cd src
- python label_image.py --graph=output_graph.pb --labels=output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=/tmp/share/not_forest/45-1859073_141-1391882_20.png

## コマンド
- docker-compose exec web bash

