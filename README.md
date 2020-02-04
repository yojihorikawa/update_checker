# update_checker
特定仮想通貨のアップデート状況を蓄積します。

# 設定
###### Docker系
BeautifulSoup4, tweepy, etc...
全部は覚えてない。。import文から察してください。

###### keys.json
/src/keys.jsonを作成。
TwitterのAPIアクセスから下記を記載してペースト。

{
  "Consumer_key": "",
  "Consumer_secret": "",
  "Access_token": "",
  "Access_secret": ""
}

###### config.json
必要な仮想通貨の情報を記載。
hp_newsのクローラーは未実装。

# 使い方
/usr/bin/python3 /src/checker.py >> /src/`date +\%Y\%m\%d`.log

python2系で試してないので動くかどうか不明。

# 結果
Mac101:src yoji_horikawa$ cat 20200130.log | grep Stellar
[Medium] Project: Stellar, Title: "Stellar Winter Roundup 2019" is added.
[Medium] Project: Stellar, Title: "SDFâ€™s Next Steps" is added.
:
:
[Git Releaase] Project: Stellar, Title: "v12.3.0rc3" is added.
[Git Releaase] Project: Stellar, Title: "v12.3.0rc2" is added.
:
:
[Twitter] Project: Stellar, text: "Demand for #blockchain solutions is growing... @DenelleDixon shares the growth strategy for the #Ste..." is added.
[Twitter] Project: Stellar, text: "Hey everyone, just a reminder that the #Stellar test network reset will happen (tomorrow) Wednesday,..." is added.

