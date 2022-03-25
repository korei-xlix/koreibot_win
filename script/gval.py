#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : グローバル値
#####################################################

#####################################################
class gVal() :

#############################
# ※ユーザ自由変更※
	DEF_BD_HOST         = 'localhost'						#データベースホスト名
	DEF_BD_NAME         = 'koreibot'						#データベース名
	DEF_BD_USER         = 'koreibot'						#データベースユーザ名
	DEF_TIMEZONE = 9										# 9=日本時間 最終更新日補正用
	DEF_MOJI_ENCODE = 'utf-8'								#文字エンコード

#############################
# システム情報
	#データversion(文字)
	DEF_CONFIG_VER = "1"

	STR_SystemInfo = {
		"Client_Name"	: "これーぼっと",
		"ProjectName"	: "",
		"github"		: "",
		"Admin"			: "",
		"TwitterURL"	: "",
		"Update"		: "",
		"Version"		: "",
		
		"PythonVer"		: 0,
		"HostName"		: "",
		
		"TimeDate"		: None,
		"NextDay"		: False,
		"Weekend"		: False,
		"RateTimeDate"	: None,
			# 前回実行日時
		"RateLockTD"	: None,
			# 前回ロック日時
		"APIrect"		: "",
		"RunMode"		: "normal"
			# normal= 通常モード
			# setup = セットアップモード
			# init  = 全初期化モード
			# add   = データ追加
			# clear = データクリア
	}

#############################
# ユーザ情報
	STR_UserInfo = {
		"Account"	: "",			#Twitterアカウント名
		"id"		: "",			#Twitter ID(番号)
		"Traffic"	: False,		#Twitterにトラヒックを報告するか
		
		"UserFolder_path"	: ""	#ユーザフォルダパス
	}

#############################
# 自動いいね設定
	STR_AutoFavo = {
		"Rip"		: False,		#リプライを含める
		"Ret"		: False,		#リツイートを含める
		"iRet"		: False,		#引用リツイートを含める
		"Tag"		: True,			#タグを含める
		"PieF"		: False,		#片フォローを含める
		
		"Len"		: 8				#対象範囲(時間)
	}

#############################
# 検索モード
	STR_SearchMode = {}
	# [0]..手動用
	# [1]以降..自動用

#############################
# ユーザ管理情報
	STR_UserAdminInfo = {}

#############################
# トラヒック情報
	STR_TrafficInfo = {
		"timeline"			: 0,	#取得タイムライン数
		"runbot"			: 0,	#Bot実行回数  *
		"runapi"			: 0,	#Twitter API実行回数
		
									#フォロワー監視情報
		"now_myfollow"		: 0,	#現フォロー者数
		"now_follower"		: 0,	#現フォロワー数
		"get_myfollow"		: 0,	#フォロー者獲得数
		"get_follower"		: 0,	#フォロワー獲得数
		"rem_myfollow"		: 0,	#リムーブフォロー者数
		"rem_follower"		: 0,	#リムーブフォロワー数
		
									#内部フォロワー監視情報
		"now_unfollow"		: 0,	#現非フォロワー数
		"now_remove"		: 0,	#現疑似リムーブ数（Twitterリムーブ除く）
		
		"run_unfollow"		: 0,	#非フォロー化実行数
		"run_unfollowrem"	: 0,	#非フォロー化解除数
		"run_autoremove"	: 0,	#自動リムーブ実行数（Twitterリムーブ、疑似リムーブ合計）
		"run_muteremove"	: 0,	#ミュート解除数
		
		"now_agent"			: 0,	#現監視ユーザ数
		"now_vipuser"		: 0,	#現VIPユーザ数
		"get_reaction"		: 0,	#リアクション獲得数
		
									#いいね情報
		"now_favo"			: 0,	#現いいね数
		"get_favo"			: 0,	#いいね実施数
		"rem_favo"			: 0,	#いいね解除数
		
									#ツイート情報
		"send_tweet"		: 0,	#ツイート送信数
		"send_retweet"		: 0,	#リツイート実施数
		
									#データベース情報
		"db_req"			: 0,	#クエリ要求回数  *
		"db_ins"			: 0,	#DB挿入回数  *
		"db_up"				: 0,	#DB更新回数  *
		"db_del"			: 0,	#DB削除回数  *
		
		"update"			: None	#トラヒック更新日時
	}



#############################
# ウェイト情報
	STR_WaitInfo = {
		"zanNum"			: 0,	#残り処理数
		"zanCount"			: 0,	#カウント数(0でウェイト処理)
		"setZanCount"		: 0,	#カウント数(セット値)
		"waitSec"			: 5,	#待ち時間(秒)
		"Skip"				: False	#スキップ待機
	}



#############################
# 除外ユーザ名・除外文字・除外Twitter ID
	STR_ExeUser     = []			#除外ユーザ名
	STR_ExeWord     = []			#除外ワード
	STR_ActionRetweet  = []			#アクションリツイート

	STR_RateExcTweetID = []			#Tweet ID
	STR_ExcTweetID = []				#新規Tweet ID

#############################
# Timeline調整数
	DEF_STR_TLNUM = {
														# ユーザ管理
		"forGetUserSec"		: 600,						#   ユーザ取得間隔  10分  60x10
		
														# いいね管理
		"forFavoriteSec"	: 28800,					#   いいね実施間隔 8時間  60x60x8
		"forFavoRemSec"		: 172800,					#   いいね解除時間 2日 (60x60x24)x2
		"favoTweetLine"		: 40,						#   いいね時 対象ユーザツイート取得ライン数
		"consRetweetLimit"	: 3,						#   連続リツイート上限 カウント回数
		"forFavoritePeriodSec"	: 43200,				#   いいね対象期間  12時間以内  60x60x12
		"normalFavoRand"	: 10,						#   通常いいね 非フォロー時の抽選値  1-100
														#     小さいほど受かりにくい
		"forChoFavoSec"		: 432000,					#   ちょっかいいいね実施間隔  5日  (60x60x24)x5
		
		"forFollowRemSec"	: 172800,					# 片フォロー→自動リムーブまでの期間  2日 (60x60x24)x2
														# 非フォロー化・疑似リムーブ関係
		"forUnfollowSec"	: 432000,					#   非フォロー化までの期間      5日 (60x60x24)x5
		"forUnfollowRemSec"	: 172800,					#   非フォロー化解除までの期間  2日 (60x60x24)x2
		"forSoftRemSec"		: 2592000,					#   疑似リムーブまでの期間 30日 (60x60x24)x30
		"forUnfollowLockCount"	: 3,					#   非フォローロック回数  この回数非フォロー化になると解除されなくなる
		
														# リアクション関係
		"forReactionSec"		: 3600,					#   リアクションチェック 実行間隔  60分  60x60
		"reactionTweetLine"		: 40,					#   リアクションチェック時の自ツイート取得ライン数
		"reactionRetweetLine"	: 200,					#   リアクションツイート取得ライン数
		
														# 自動フォロー関係
		"autoNewFollowNum"		: 1,					#   Autoフォロー1回でのフォロー回数
		"manualNewFollowNum"	: 5,					#   手動フォロー1回でのフォロー回数
		
														# フォローサーチ関係
		"followSearchLine"	: 200,						#   フォローサーチで取得するタイムライン数
		"fsTweetNum"		: 2,						#   フォローサーチ ツイート選定数
		"fsUserNum"			: 10,						#   フォローサーチ ユーザ選定数
		"followSearchWaitSec"	: 60,					#   フォローサーチ 周回待ち
		"followSearchWaitCount"	: 8,					#   フォローサーチ 周回カウント
		"followSearchSkipRange"	: 8,					#   フォローサーチ スキップ許容数
		
														# 週末関係
		"weekendHour"		: 22,						#   週末 時間
		"weekendWeek"		: "4",						#   週末 曜日 0=月,1=火,2=水,3=木,4=金,5=土,6=日
		
														# 周回待ち要
		"defWaitCount"		: 16,						#   デフォルト待ち回数
		"defWaitSec"		: 5,						#   デフォルト待ち時間(秒)
		"defWaitSkip"		: 10,						#   デフォルトスキップ時間(秒)
		"defLongWaitSec"	: 60,						#   デフォルト 長い待ち時間(秒)
		
		"UserAliveLine"		: 100,						# ユーザ活動 ツイート取得ライン数
		"UserAliveSec"		: 43200,					# ユーザ活動非活性期間 12時間  60x60x12
		"UserAliveRetweetRange"	: 0.2,					# ユーザ活動 リツイート許容範囲（割合）
		
		"resetAPISec"		: 900,						# APIリセット周期 15分 60x15
		"forLockLimSec"		: 120,						# 排他保持時間     2分 60x2 
		"logShortLen"		: 100,						# ログ表示 ショートモード
		
		"(dummy)"			: ""
	}

#############################
# ファイルパス
#   ファイルは語尾なし、フォルダは_path
	DEF_DATAPATH = "data/"

	DEF_STR_FILE = {
		"Readme"				: "readme.md",
		"ExcWordArc"			: DEF_DATAPATH + "DEF_ExcWordArc.zip",
		
		"Melt_ExcWordArc_path"	: "DEF_ExcWordArc",
		"Melt_ExcWord"			: "DEF_ExcWordArc/DEF_ExcWord.txt",
		"Melt_ExcUser"			: "DEF_ExcWordArc/DEF_ExcUser.txt",
		"Melt_ActionRetweet"	: "DEF_ExcWordArc/DEF_ActionRetweet.txt",
		"(dummy)"				: 0
	}

	DEF_DISPPATH = "script/disp/"

	DEF_STR_DISPFILE = {
		"MainConsole"			: DEF_DISPPATH + "main_console.disp",
		"SearchConsole"			: DEF_DISPPATH + "search_console.disp",
		"KeyuserConsole"		: DEF_DISPPATH + "keyuser_console.disp",
		"UserAdminConsole"		: DEF_DISPPATH + "useradmin_console.disp",
		"AutoFavoConsole"		: DEF_DISPPATH + "autofavo_console.disp",
		
		"(dummy)"				: 0
	}

#############################
# 荒らし理由
	DEF_STR_ARASHI_REASON_ID = {
		0	: "Not Arashi",
		10	: "Hash Tag",
		11	: "Hash and URL",
		20	: "China User Name",
		21	: "China Word",
		99	: "Manual Designation"
	}

#############################
# 定数
	DEF_PROF_SUBURL = "/web/accounts/"						#プロフ用サブURL
	DEF_TOOT_SUBURL = "/web/statuses/"						#トゥート用サブURL

	DEF_LOCK_LOOPTIME = 2									#ロック解除待ち
	DEF_LOCK_WAITCNT  = 30									#  待ち時間: DEF_LOCK_LOOPTIME * DEF_LOCK_WAITCNT
	DEF_TEST_MODE     = "bottest"							#テストモード(引数文字)
	DEF_DATA_BOUNDARY = "|,|"



#############################
# 変数
	FLG_Test_Mode    = False								#テストモード有無
	
	STR_DomainREM = []										#除外ドメイン
	STR_WordREM   = []										#禁止ワード
	
	OBJ_Tw_IF = ""											#Twitter I/F
	OBJ_DB_IF = ""											#DB I/F
	OBJ_L     = ""											#ログ用

	ARR_FollowKouho = {}									#候補ユーザ



