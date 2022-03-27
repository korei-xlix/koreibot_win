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
　　[Twitter Dev](https://developer.twitter.com/)
  
[Sign Up]を押します。  
  

2.必要事項を入力します。  

* What's your name?  
  Twitter Dev上のユーザ名を入れます。  
* What country are you based in?  
  国籍を選択します。  
* What's your use case?  
  用途を選択します。「Making a bot」Bot作成でいいと思います。  
* Will you make Twitter content or derived...  
  政府関連が利用できるようにするか。「No」でもいいと思います。  
* Want updates?  
  Twitter Devのお知らせメールを受け取るか？チェックなしでもいいと思いますね。  
  
「Next」を押します  
  
2. 規約を読んで、チェックして  
「Submit」を押します  
  

3.Twitter Devからメールアドレスに認証メールが来るのでチェックします。  
 最初の画面で App Name を指定されます。  
 最初のアプリの名称を入力します。「Korei Bot」とか？  

4. API Key、API Sercret Key、Bearer Token をメモします。  
  
「Skip to Dashbord」を押します  
  

ここからダッシュボードの設定作業です。  
  
5.左のバーから Projects & Apps → Project 1 → アプリ名 をクリックします。  
  
6.App detailsのEditをクリックします。  
  ここでアプリのアイコンのアップロードと、Descriptionの入力をおこないます。  
  審査対象になるかもしれませんので、必ず詳細を入力してください。  
  
7.User authentication settingsでSetupを押してください。  
  
  OAuth 1.0aを有効にします。  
  App permissionsをRead and write and Direct messageに設定  
  Callback URI はGithubのURLでも入れてください。（アプリでは使いません）
  Website URL はホームページのURIです。なければTwitterのプロフでも  
  
「Save」を押します  
  
8. 上のKeys and tokensを押して、Access Token and Secretを押します。  
  Access token、Access token Secretをメモします。  

ここからアプリの審査を通します。  
これに受かっておかないと、アプリが遮断される場合があります。（というか100％遮断されるので）  
  
9.左のバーから Projects & Apps → Project 1 をクリックします。  
  Do you need higher levels of access? で「Apply for Elevated」をクリックします。  
  

10. What's your current coding skill でスキルレベルを選択します。  
  
「Next」を押します  
  

11.各項目にbotを作成する用途を英語で入力していきます。ここで入力した内容でTwitterの審査を受けることになります。
　botの目的をはっきり説明しないと審査が通らない場合があるようです。
　英語で入力するように言われてますが、日本語でもばっちり大丈夫です。
　このbotを利用するときは以下のように入力してください。

**In your words**
主に以下の機能を持ったbotアプリケーションです。  
制御はPythonでコンソールからおこないます。データの管理でPostgre SQLも使います。  
  
以下のような機能をもちます。

●Twitterトレンドをつぶやきます。
コンソールからのコマンドで現在のTwitterトレンドをつぶやきます。  
なお、既に前の時間でつぶやいたトレンドツイートは削除し、新しい情報として自分のタイムラインに残すようにします。  
  
●一定期間を過ぎた、いいねの解除をします。
既に付けた"いいね"のうち一定期間を過ぎたものを"いいね解除する"します。例えば、現時刻から3日を超えた時点でつけたいいねを解除したりです。なおbotでいいねを付けることはありません。
  

ほかにも出たエラーをデータベースに記録するようにしますが、このエラー制御、トラヒック情報などはアプリ内部管理のものであり、Twitterには影響はありません。  


**Are you planning to analyze Twitter data?**
計画はありません。トレンド情報についてもアプリ内部で格納したり、その情報を利用してビジネスなどの処理をおこないません。またbotが収集したデータをTwitter上、その他外部に公開することはありません。  

**Will your app use Tweet, Retweet, like, follow, or Direct Message functionality?**
トレンドのツイート、いいね一覧をロードする機能は使います。しかし、それにより分析、ビジネスなどの処理はおこないません。トレンドツイートの組み立てに利用したり、いいね一覧のクリーン化をおこなうだけです。もしかしたら、近い将来、リストを制御する機能も使うかもしれません。  

**Do you plan to display Tweets or aggregate data about Twitter content outside of Twitter?**
ビジネス目的のツイート分析ではなく個人の利用を目的としています。トレンドツイートの組み立てに利用したり、いいね一覧のクリーン化をおこなうだけです。正直ビジネスには向かないアプリケーションだと思いますが、トレンド機能を利用すればそういった展開はできる可能性はあります。が、わたし自身そういう考えは全くありません。

**Will your product, service or analysis make Twitter content or derived information available to a government entity?**
このbotで作成されたデータやCSVを政府機関に提示することは考えてません。また当方は政府機関などとは関係ありません。
しかし、そういった機関から要求があればデータを提出できると思います。
  
「Next」を押します。  
「Next」を押します。  
規約を読み、ボックスをチェックして「Submit」を押します  
  

12.Twitterに登録されたメールアドレスに確認メールが送られていますので、「Confirm your email」をクリックします。
　利用開始は審査結果メールを受けてからになります。メールが来るまでお待ちください。1日くらいで返事がきます。
　なお前提条件にあったとおり、何度もしつこく質問されると思いますが、根気よく回答してあげてください。


汗かきながら書いたメールのやりとりが上手くいき、審査に受かると、Twitterから
「Your Twitter developer account application has been approved!」の開発許諾メールを受けとれます。
おめでとう！これでようやく次に進めます。




***
::Project= Korei bot  
::Admin= Korei (@korei-xlix)  
::github= https://github.com/korei-xlix/  
::Homepage= https://koreixlix.wixsite.com/profile  
