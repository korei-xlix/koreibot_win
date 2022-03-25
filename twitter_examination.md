# Twitter審査要項


# このドキュメントについて <a name="aHowto"></a>
Twitter APIを使用するには、Twitterで審査を受けて通らないと利用できません。  
審査はわりと厳しく、何度かやりとりをする必要があります。  
本ドキュメントはアクセスキーの入手方法、このbotの審査を通すための要領を示すものです。  


# 目次 <a name="aMokuji"></a>
* [システム概要](#iSystemSummary)




<a id="iGetTwitter"></a>
## Twitter APIの取得方法　★初回のみ
1.以下、twitterのサイトにtwitterアカウントでログインします。
　　[Twitter API](https://apps.twitter.com/app/new)

2～5 までの項目ではDeveropper Accountの設定をおこないます。
  ※設定済なら6へ進む

2.「Create an app」をクリックします。

3.HObby list→Making botをクリックしてNextを押します。

4.各項目を入力し、Nextを押します。
　**bot登録するには電話番号を登録する必要があります。**「Add a valid」で登録します。
　What country do you live in? はJapanを選択します。
　What would you like us to call you? はDeveropper Accountでのユーザ名（英数字）を入力します。
　Want updates about the Twitter API? は必要に応じてチェックします。

5.各項目にbotを作成する用途を英語で入力していきます。ここで入力した内容でTwitterの審査を受けることになります。
　botの目的をはっきり説明しないと審査が通らない場合があるようです。
　英語で入力するように言われてますが、日本語でもばっちり大丈夫です。
　このbotを利用するときは以下のように入力してください。

**In your words**
主にフォロワーからのアクションの管理をおこなうためのbotで利用します。
フォロワーからのフォロー、いいねは、一時的に通知があったことは分かっても、過去に遡って詳細は覚えきれません。そこでbotでフォローの有無、いいねの回数履歴を検知して、データベースに格納して後で閲覧できるようにします。
またTwitterのトレンドをつぶやいたユーザを抽出して、こちらからのフォローの有無を判断する材料にもしたいです。

以下のような機能をもちます。

●フォロワーのフォロー、リフォローの状態管理をおこないます。
フォロー、被フォローの状態をデータベースに格納します。また過去に遡って、一度でもフォローしたことがある状態、一度でもリムーブされたことがある状態、ブロックされたことがあるかもデータベースに格納します。
この状態を管理しておくことで、もし一度フォローが外れても、再フォローするか、リアクションに対して応答するかの指標にしたいです。

●フォロワーのリアクションを管理します。
フォロワーからのいいね、リツイート、引用リツイート、リプライの回数、日時をデータベースに格納します。これにより、よくアクションをしてくれるユーザを把握したいです。
またもしアクションが少なければ内部で"非フォロー化"といったステータスをつけて、リアクションに応答する頻度レベルを調整したいです。非フォロー化がさらに進行することで、内部で"疑似リムーブ"として、リアクションに応答することがないようにしたいです。
ユーザによってはリフォローは期待するけど、リアクションは期待しない方もいらっしゃると思いますので、それらに対する反応の指標にしたいです。

●トロフィーを配布します。
フォロワーからのリアクションを計測し、週一でランキングを発表し、1位の方を発表（ツイート）します。またそれと同時にトロフィーを発行し、過去に遡ってトロフィーの獲得数も管理したり、同時に発表します。

●Twitterトレンドをつぶやいたユーザを抽出します。
Twitterトレンドをつぶやいたユーザを抽出し、フォロワーのフォロー数、フォロワー数からリフォローが期待できるかどうかを判断し、期待出来たらリストに抽出しフォローの有無の指標にしたいです。
またデータベースに格納されたユーザであれば、過去のフォローの状況に遡って、再フォローが期待できるかも判断します。

●一定期間を過ぎた、いいねの解除をします。
既に付けた"いいね"のうち一定期間を過ぎたものを"いいね解除する"します。例えば、現時刻から3日を超えた時点でつけたいいねを解除したりです。
botでいいねを付けることはありません。

●実行の規制をおこないます。
Twitterへの負荷を軽減するため、実行間隔をbotで制御します。たとえば、bot実行したとき、前回の実行が10分前であったら以降の処理を行わず、botの動作を停止します。10分を過ぎた実行は処理されます。この仕様によって手動実行でもcronによる定期実行でも対応できる上、Twitterサーバへの負荷が少なくなると考えてます。

なおbotはアップデートして将来的に別の機能をつけたり、機能を改良したりします。

**Are you planning to analyze Twitter data?**
分析というより、ツイートやユーザの抽出、絞り込みをおこないます。ユーザの抽出、絞り込み動作については、フォロー数、フォロワーの数、ツイートの内容から判断していきます。なお、botが収集したデータをTwitter上、その他外部に公開することはありません。

**Will your app use Tweet, Retweet, like, follow, or Direct Message functionality?**
タイムラインをロードする機能、フォロー一覧をロードする機能、フォロワー一覧をロードする機能、いいね一覧をロードする機能、指定のいいねを解除する機能、指定ユーザをリスト（過去にアンフォローされたユーザ）へ追加する機能は使います。

**Do you plan to display Tweets or aggregate data about Twitter content outside of Twitter?**
ビジネス目的のツイート分析ではなく個人の利用を目的としています。botによりフォロワーの利用状況を把握したり、わたしのTwitterの運用を支援したりします。あくまで過去に遡って、再フォローするか、リアクションに応答するかの指標とします。

**Will your product, service or analysis make Twitter content or derived information available to a government entity?**
このbotで作成されたデータやCSVを政府機関に提示することは考えてません。また当方は政府機関などとは関係ありません。
しかし、そういった機関から要求があればデータを提出できると思います。


Nextを押します。「Looks good!」を押します。

6.規約を読み、By clicking on the box～のボックスをチェックして「Submit Application」をクリックします。






7.Twitterに登録されたメールアドレスに確認メールが送られていますので、「Confirm your email」をクリックします。
　利用開始は審査結果メールを受けてからになります。メールが来るまでお待ちください。1日くらいで返事がきます。
　なお前提条件にあったとおり、何度もしつこく質問されると思いますが、根気よく回答してあげてください。


汗かきながら書いたメールのやりとりが上手くいき、審査に受かると、Twitterから
「Your Twitter developer account application has been approved!」の開発許諾メールを受けとれます。
おめでとう！これでようやく次に進めます。








6.メールをクリックして、Welcome to the Twitter Developer Platformでアプリ名を入力します。
　アプリ名は後でdashbordで変えられます。

7.以下をメモします。**この情報は厳重に保管してください**

* API key
* API secret key
* Bearer token

8.[Skip to dashboard]をクイックし、[Yes, I saved then]をクリックします。
　以後はdashbord画面で管理します。

9.Setting画面で必要事項を入力します。

**App Details**
App name
　変える場合入力する。
Description
　アプリの説明。わかりやすいように。
App permissions
　Read and Write, and Direct Messages　を指定してください。
　DMはトラヒック報告で使用します。

**Authentication settings**
Enable 3rd party authentication
　有効にしてください。
Callback URLs
　必須。コールバックしませんが自分のブログURLなど適当でいいです。（他人のサイトURLは絶対ダメ！）
Website URL
　必須。https://github.com/lucida3rd/lucibot_win2　などにしておくと、botの説明に飛べます。（わたしのgithubです）

10.keys and tokensに切り替えます。**この情報は厳重に保管してください**
Authentication TokensのAccess Token & Secretの[Generate]をクリックして以下をメモします。

* Access token
* Access token secret

4つの情報はあとで設定します。

* API key
* API secret key
* Access token
* Access token secret

> 最悪忘れてしまってもリセットして取り直すことができます。
> ただキーを流出させるのはリスクが大きすぎるので注意しましょう。










***
::Project= Korei bot  
::Admin= Korei (@korei-xlix)  
::github= https://github.com/korei-xlix/  
::Homepage= https://koreixlix.wixsite.com/profile  
