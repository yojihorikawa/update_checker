# update_checker
特定仮想通貨のアップデート状況を蓄積します。

# update_checker
特定仮想通貨のアップデート状況を蓄積します。

# 使い方
/usr/bin/python3 /src/checker.py >> /src/`date +\%Y\%m\%d`.log

python2系で試してないので動くかどうか不明。

#設定
######Docker系
BeautifulSoup4, tweepy, etc...
全部は覚えてない。。import文から察してください。

######keys.json
TwitterのAPIアクセスから下記を記載してペースト
{
  "Consumer_key": "",
  "Consumer_secret": "",
  "Access_token": "",
  "Access_secret": ""
}

######config.json
必要な仮想通貨の情報を記載。
hp_newsのクローラーは未実装。
