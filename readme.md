# これーbot win
**～取扱説明書 兼 設計仕様書～**  


# システム概要 <a name="aSystemSummary"></a>
python3で作成したWindows環境下で動くことを前提にしたTwitter支援用botです。  
* 現在のトレンドをツイートします。
* 一定期間がを過ぎたいいねを解除します。いいねリストをクリーンにします。




# 目次 <a name="aMokuji"></a>
* [システム概要](#aSystemSummary)
* [前提](#aPremise)
* [デフォルトエンコードの確認](#aDefEncode)
* [セットアップ手順](#aSetup)
* [起動方法](#aStart)
* [アップデート手順](#aUpdate)
* [運用方法](#aHowtoUnyou)
* [機能説明](#aFunction)
* [本リポジトリの規約](#aRules)
* [参考記事](#aReference)




# 前提 <a name="aPremise"></a>
* Twitterの審査に受かること (！大前提！)
* python3（v3.8.5で確認）
* postgreSQL（Windows版）
* Windows 10
* twitterアカウント
* githubアカウント
* デフォルトエンコード：utf-8

> **Twitterの審査について**
> 本アプリを使用するにはTwitterの審査に受かってAPI登録する必要があります。  
> Twitterの審査については別ドキュメント [Twitter審査要項](/twitter_examination.md) を参照ください。  




# デフォルトエンコードの確認　★初回のみ <a name="aDefEncode"></a>
本ソフトはデフォルトエンコード**utf-8**で動作することを前提に設計してます。
utf-8以外のエンコードでは誤動作を起こす場合があります。
pythonのデフォルトエンコードを確認したり、utf-8に設定する方法を示します。

```
# python
>>> import sys
>>> sys.getdefaultencoding()
'utf-8'
  utf-8が表示されればOKです。

>> exit
  ここでCtrl+Z を入力してリターンで終了します。
```

もしutf-8でなければWindowsの環境変数に PYTHONUTF8=1 を追加します。  
「スタート」→「システムの詳細設定 で検索」→「詳細設定」→「環境変数」  
ここに **変数名=PYTHONUTF8、変数値=1** を追加する。  
設定したら上記エンコードの確認を再実行して確認しましょう。  




# セットアップ手順 <a name="aSetup"></a>

1. pythonと必要なライブラリをインストールします。  
	インストーラを以下から取得します。基本的に * web-based installer を使います。  
	入手したインストーラで好きな場所にセットアップします。  
	    [python HP](https://www.python.org/)  
	  
	Add Python x.x to Path はチェックしたほうがいいです。  
	その他はデフォルトか、環境にあわせてオプションを選択しましょう。  
	インストールが終わったらテストしてみます。  
	```
	# python -V
	Python 3.8.5
	  ※Windowsの場合、python3ではなく、pythonらしいです
	
	# pip3 install requests requests_oauthlib psycopg2
	～中略～
	
	# pip3 list
	～以下省略～
	```

2. postgreSQLをインストールします。  
	1. インストーラを以下から取得します。  
		    [postgresql HP](https://www.postgresql.org/download/)  
		Windows 32bit or 64bit 形式を選択します。  

	2. インストーラに従ってインストールします。  
		postgreSQLのスーパーユーザは postgres になります。  
		**パスワードは忘れずに覚えておきましょう**  
		スタックビルダは必要に応じてセットアップしてください。（特に不要です）  

	3. 環境変数を設定します。  
		「スタート」→「システムの詳細設定 で検索」→「詳細設定」→「環境変数」  
		ここのPathにpostgreSQLのbinフォルダを追加します。  
		```
		例：
		C:\Program Files\PostgreSQL\13\bin
		```

	4. 追加したらOKを押します。  

	5. 動作テストします。  
		```
		# psql --version
		psql (PostgreSQL) 13.0
		
		psql -U postgres
		
		=>
		
		=> \q
		　※エラーがでなければOKです
		```

3. botで使うデータベースを作成します。  
	```
	# createuser -U postgres koreibot
	# createdb -U postgres -O koreibot koreibot
	パスワードはスーパーユーザ[postgres]のものです
	
	スーパーユーザ[postgres]でログインする
	# psql postgres -U postgres
	
	データベースのパスワードを設定する。
	=> alter role koreibot with password '[DBパスワード]';
	=> alter role koreibot with login;
	=> \q  
	この操作でDBのユーザ名、データベース名は koreibot になります。
	
	# psql -U koreibot koreibot
	[DBパスワード]でログインする
	
	=>
	
	=> \q
	　※エラーがでなければOKです
	```

4. botソースの管理アプリとしてWindows版のgithubデスクトップを使います。  
	1. githubデスクトップをインストールします。  
		　　[githubデスクトップ](https://desktop.github.com)  

	2. githubの自分のアカウントに本家リポジトリをFork（コピー）する。  
		　　[botリポジトリ](https://github.com/korei-xlix/koreibot_win)  
		の右上あたりの[Fork]ボタンを押してください。  
		すると、自分のアカウントに[自垢名 / koreibot_win]というリポジトリができます。  

	3. githubデスクトップで1項でForkしたリポジトリから自PCにクローンをダウンロードします。  
		githubデスクトップのCurrent repository→Add→Cloneを選択します。  
		任意のフォルダを選択してCloneを押してください。  

	4. 自分のブランチを作ります。  
		githubデスクトップのCurrent branch→New branchで任意の名前を入力します。  

5. DOSのコマンドラインを起動します。  

6. 以下を入力します。  
	```
	# cd [Koreibotのインストールフォルダ]
	# python run.py init
	```

7. データベースの全初期化と、ユーザ登録を実施します。画面に従って入力します。  
	以下の情報が必要となります。
	
	* koreibotのデータベースパスワード
	* Twitterアカウント名
	* Twitter Devで取ったAPI key
	* Twitter Devで取ったAPI secret key
	* Twitter Devで取ったAccess token
	* Twitter Devで取ったAccess token secret

**セットアップはここで完了です**  

8. botを起動します。  
	```
	# cd [botのインストールフォルダ]
	# python run.py [twitterアカウント名] [botのデータベースパスワード]
	```
  
**起動すると、コンソール画面が起動します。**  




# 起動方法 <a name="aStart"></a>

起動はDOSのコマンドラインからおこないます。  

1. DOSのコマンドラインを起動します。  

2. 以下を入力します。  
	```
	# cd [botのインストールフォルダ]
	# python run.py [twitterアカウント名] [botのデータベースパスワード]
	```

**起動すると、コンソール画面が起動します。**  
  

## オプション起動

以下は各調整用のオプション起動です。  

#### テストモード起動
	起動時、後ろに bottest を付けることでテストモードが起動します。  
	**開発時に使用ください。**  

	1. DOSのコマンドラインを起動します。  
	
	2. 以下を入力します。  
		```
		# cd [botのインストールフォルダ]
		# python run.py [twitterアカウント名] [botのデータベースパスワード] bottest
		```
	
	**起動すると、コンソール画面が起動します。**  

#### ユーザセットアップ
	Twitterのアカウントを追加したり、APIを変更する際に使用ください。  
	```
	# python run.py setup
	```

#### ログクリア
	ログやトラヒックを初期化する際に使用ください。  
	```
	# python run.py clear
	```

#### 除外データの追加
	除外データを追加する際に使用ください。  
	除外データは以下のテキストを編集します。  
	```
	\datta\DEF_ExcWordArc
	
	プロフィール、ユーザ名の除外
	　　DEF_ExcUser.txt
	
	ツイート文の除外
	　　DEF_ExcWord.txt
	
	アクションリツイートのデータ
	　　DEF_ActionRetweet.txt
	```
	
	以下のコマンドでデータベースに追加されます。  
	```
	# python run.py add
	```

#### 全初期化
	botのデータベースを全て初期化します。アップデートでDBの構成が変更された際に使用ください。  
	```
	# python run.py init
	```




# アップデート手順 <a name="aUpdate"></a>
botリポジトリのmasterから最新版をpullする方法です。  

1. githubデスクトップを起動します。  

2. 自分のKoreibotリポジトリを選択し、Current branchをクリックします。  

3. New branchをクリックし、バックアップ用のブランチを作成します。  
	名前はわかりやすいように。

4. ブランチを[main]に切り替えます。  

5. [Fetch Origin]をクリックします。  

6. [Puch]をクリックします。  
	ここまでで、自分のリポジトリの[main]と、自PCのソースに最新が反映されてます。  

> **もし不具合があったら...？**  
>	3項で保存したブランチに切り替えると、自PC側にアップデート前のソースが戻ってきます。  
>	以後、アップデートがあったら[main]に切り替えて[Fetch]すれば、修正後のソースが反映されます。  




# 機能説明 <a name="aFunction"></a>

botの各機能を以下に説明します。  
コマンドを実行するには、画面のプロンプトに指定のコマンドを入力します。  
コマンドは全て\マークの後、半角英字を入力します。  


## 自動監視【 \a 】
いいねクリア、いいね監視、いいね送信を全て行います。  


## トレンドツイート【 \tt 】
Twitterのトレンドワードをツイートします。  
トレンドワードをツイートすることでインプレッションを獲得できる可能性があります。  
過去にツイートしたトレンドワードは削除されます。  




# 本リポジトリの規約 <a name="aRules"></a>
* 素材の改造、流用、配布について。  
  * このリポジトリ配下のソースの改造、改造物の配布は自由にやってください。  
    その際の著作権は放棄しません。  
  * 未改造物の再配布、クローンしたあと未改造のまま放置することは禁止とします。  
* 著作権について。
  * 著作権は放棄しません。
  * 別に著作権表記のある素材の利用については、各自で許諾を取得ください。  
    当方では責任を負いません。  
* 免責事項について。
  * 当ソースを使用したことによる不具合、損害について当方は責任を持ちません。  
    全て自己責任でお願いします。  
  * Web上やSNS上、オンライン上で発生した、わたしが関知していないトラブル、損害については、  
    一切責任を負いません。各自でご対応をお願いします。  
* 当ソースの仕様、不具合についての質問は受け付けません。自己解析、自己対応でお願いします。  
* このリポジトリに含まれるファイル構成を変えたり、消したりしないでください。誤動作の原因となります。  
* その他、ご意見、ご要望については、開発者ホームページを参照ください。  




# 参考記事 <a name="aReference"></a>
**※敬称略**  
* [Windows 上の Python で UTF-8 をデフォルトにする（methane）](https://qiita.com/methane/items/9a19ddf615089b071e71)




***
::Project= Korei bot  
::Admin= Korei (@korei-xlix)  
::github= https://github.com/korei-xlix/  
::Homepage= https://koreixlix.wixsite.com/profile  
