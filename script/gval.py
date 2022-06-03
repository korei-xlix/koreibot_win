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
###		"ProjectName"	: "",
		"github"		: "",
		"Admin"			: "",
###		"TwitterURL"	: "",
###		"Update"		: "",
###		"Version"		: "",
###		
		"PythonVer"		: 0,
		"HostName"		: "",
		
		"TimeDate"		: None,
###		"NextDay"		: False,
###		"Weekend"		: False,
		"RateTimeDate"	: None,
			# 前回実行日時
		"RateLockTD"	: None,
			# 前回ロック日時
		"APIrect"		: "",
		
		"EXT_FilePath"	: None,
		
		"RunMode"		: "normal"
			# normal= 通常モード
			# setup = セットアップモード
			# init  = 全初期化モード
			# clear = データクリア
	}

#############################
# ユーザ情報
	STR_UserInfo = {
		"Account"	: "",			#Twitterアカウント名
		"id"		: "",			#Twitter ID(番号)
		"Traffic"	: False,		#Twitterにトラヒックを報告するか
		"TrendTag"	: "",			#トレンドタグ設定
		"FavoDate"	: None,			#いいね者送信日時(直近)
		
		"ListName"	: "",			#リスト通知 リスト名
		"ListDate"	: None,			#リスト通知日時
###		"LFavoName"	: "",			#リストいいね リスト名
		"LFavoDate"	: None			#リストいいね日時
	}

#############################
# トラヒック情報
	STR_TrafficInfo = {
		"timeline"			: 0,	#取得タイムライン数
		"runbot"			: 0,	#Bot実行回数  *
		"runapi"			: 0,	#Twitter API実行回数
		
									#いいね情報
		"now_favo"			: 0,	#現いいね数
		"get_favo"			: 0,	#いいね実施数
		"rem_favo"			: 0,	#いいね解除数
		
									#リアクション
		"get_reaction"		: 0,	#リアクション受信数
		
									#ツイート情報
		"send_tweet"		: 0,	#ツイート送信数
		
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
# Timeline調整数
	DEF_STR_TLNUM = {
														# いいね管理
###		"forFavoRemSec"		: 172800,					#   いいね解除時間 2日 (60x60x24)x2
		"favoTweetLine"		: 40,						#   いいね時 対象ユーザツイート取得ライン数
###		"favoCancelNum"		: 20,						#   いいね時 連続スキップでキャンセル
		"favoCancelNum"		: 8,						#   いいね時 連続スキップでキャンセル
###		"autoRepFavoSec"	: 172800,					#   自動おかえしいいね時間 2日 (60x60x24)x2
		"autoRepFavo"		: True,						#   自動おかえしいいね True=有効
		"getUserTimeLine"	: 40,						#   相手ユーザ取得タイムライン数
		
														# 周回待ち要
		"defWaitCount"		: 16,						#   デフォルト待ち回数
		"defWaitSec"		: 5,						#   デフォルト待ち時間(秒)
		"defWaitSkip"		: 10,						#   デフォルトスキップ時間(秒)
		"defLongWaitSec"	: 60,						#   デフォルト 長い待ち時間(秒)
		
														# リアクションチェック
		"reactionTweetLine"			: 40,				#   リアクションチェック時の自ツイート取得ライン数
		"reactionTweetLine_Short"	: 8,				#   リアクションチェック時の自ツイート取得ライン数(ショート時)
###		"forReactionSec"			: 10800,			#   リアクションまでの期間   3時間  60x60x3
		"forReactionSec"			: 3600,				#   リアクションまでの期間   1時間  60x60
		"forReactionTweetSec"		: 172800,			#   リアクションに反応するツイート期間 2日 (60x60x24)x2
		
														# リストいいね
		"forListFavoSec"			: 86400,			#   リストいいねまでの期間   1日  60x60x24
###		"forListFavoMyFollowSec"	: 86400,			#   リストいいね フォロー者への期間   1日  (60x60x24)x1
###		"forListFavoNoFollowSec"	: 345600,			#   リストいいね フォロー外への期間   4日  (60x60x24)x4
		"forListFavoMyFollowSec"	: 14400,			#   リストいいね フォロー者への期間   4時間  60x60x4
		"forListFavoNoFollowSec"	: 259200,			#   リストいいね フォロー外への期間   3日  (60x60x24)x3
		"forOverListFavoCount"		: 3,				#   外部いいね数(1ユーザ)
		
														# いいね送信
###		"favoSendsSec"		: 10,						# いいね送信までの期間      7日 (60x60x24)x7
		"favoSendsSec"		: 604800,					# いいね送信までの期間      7日 (60x60x24)x7
		"favoDataDelSec"	: 7776000,					# いいね情報削除までの期間  90日 (60x60x24)x90
###		"favoSendsCnt"		: 1,						# いいね送信対象 いいね回数
###		"favoSendsCnt"		: 2,						# いいね送信対象 いいね回数
		"favoSendsCnt"		: 3,						# いいね送信対象 いいね回数
		
														# ユーザ管理
		"forGetUserSec"		: 600,						#   ユーザ取得間隔  10分  60x10
		"forFollowerConfirmSec"	: 86400,				#   フォロワー状態の更新 期間   1日  (60x60x24)x1
		
														# キーワードいいね
		"KeywordTweetLen"		: 40,					#   キーワードいいねツイート取得数
		"forKeywordTweetSec"	: 28800,				#   キーワードいいね いいね期間   8時間  60x60x8
		"forKeywordObjectTweetSec"	: 86400,			#   キーワードいいね 対象いいね期間   1日  (60x60x24)x1
		
		"resetAPISec"		: 900,						# APIリセット周期 15分 60x15
		"forLockLimSec"		: 120,						# 排他保持時間     2分 60x2 
		"logShortLen"		: 100,						# ログ表示 ショートモード
		
		"(dummy)"			: ""
	}

#############################
# リアクション禁止
	DEF_STR_NOT_REACTION = [
		"korei_xlix",
		"korei_dev",
		"korei_comm",
		"korei_send",
		"galaxy_fleet"
	]

#############################
# ファイルパス
#   ファイルは語尾なし、フォルダは_path
###	DEF_DATAPATH = "data/"
###
	DEF_STR_FILE = {
									# readme.md ファイルパス
		"Readme"				: "readme.md",
		
									# 除外データアーカイブ ファイル名
		"ExcWordArc"			: "/DEF_ExcWordArc.zip",
									# 除外データアーカイブ 解凍先フォルダパス
		"Melt_ExcWordArc_path"	: "/DEF_ExcWordArc",
									# 除外データ 文字列ファイルパス(フォルダ付き)
		"Melt_ExcWord"			: "/DEF_ExcWordArc/DEF_ExcWord.txt",
									# リストいいね指定ファイル
		"Melt_ListFavo"			: "/DEF_ExcWordArc/DEF_ListFavo.txt",
		
		"(dummy)"				: 0
	}

	DEF_DISPPATH = "script/disp/"

	DEF_STR_DISPFILE = {
		"MainConsole"			: DEF_DISPPATH + "main_console.disp",
		"UserAdminConsole"		: DEF_DISPPATH + "useradmin_console.disp",
		"KeywordConsole"		: DEF_DISPPATH + "keyword_console.disp",
		"(dummy)"				: 0
	}

#############################
# 定数
	DEF_LOCK_LOOPTIME = 2									#ロック解除待ち
	DEF_LOCK_WAITCNT  = 30									#  待ち時間: DEF_LOCK_LOOPTIME * DEF_LOCK_WAITCNT
	DEF_TEST_MODE     = "bottest"							#テストモード(引数文字)
	DEF_DATA_BOUNDARY = "|,|"

	DEF_SCREEN_NAME_SIZE = 24



#############################
# 変数
	FLG_Test_Mode    = False								#テストモード有無
	
	OBJ_Tw_IF = ""											#Twitter I/F
	OBJ_DB_IF = ""											#DB I/F
	OBJ_L     = ""											#ログ用
	
	ARR_ExeWord = {}										# 除外文字データ
###	ARR_ExeWordKey = []
	ARR_ListFavo = {}										# リストいいね指定



