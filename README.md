# slack_bot
rasberrypiにおけるslackbot(python)向けのスクリプトです。  
chunithmnetにおいてスクレイピングをするためのコードです。
## 必要ライブラリ
* chrome-driver(自分のchromeのバージョンにあわせて入れてください。)
* beautifulsoup4
## 各コードについての説明  
### best.py
chunithmnetにおいてchuniviewer向けのスクリプトを実行し、結果をslackに返すスクリプトです。  
chunithmnet有料コースとchuniviewerへの会員登録が必須になります。  
### chunithm.py  
chunithmにおいて楽曲すべてのプレイ回数ランキング(master)を作成するスクリプトです。  
サーバー負荷をかけないためにかなりの実行時間がかかります。
### friendvs.py  
friendvsを取得してslackに実行結果を返します。
### friendvs_multi.py
friendをすべて取得してfriend全員のある曲に関するランキングを生成するスクリプトです。  
