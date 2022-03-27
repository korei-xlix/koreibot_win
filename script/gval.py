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
###		"NextDay"		: False,
###		"Weekend"		: False,
		"RateTimeDate"	: None,
			# 前回実行日時
		"RateLockTD"	: None,
			# 前回ロック日時
		"APIrect"		: "",
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
		"Traffic"	: False			#Twitterにトラヒックを報告するか
	}

#############################
# トラヒック情報
	STR_TrafficInfo = {
		"timeline"			: 0,	#取得タイムライン数
		"runbot"			: 0,	#Bot実行回数  *
		"runapi"			: 0,	#Twitter API実行回数
		
									#いいね情報
		"now_favo"			: 0,	#現いいね数
		"rem_favo"			: 0,	#いいね解除数
		
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
		"forFavoRemSec"		: 172800,					#   いいね解除時間 2日 (60x60x24)x2
		"favoTweetLine"		: 40,						#   いいね時 対象ユーザツイート取得ライン数
		
														# 周回待ち要
		"defWaitCount"		: 16,						#   デフォルト待ち回数
		"defWaitSec"		: 5,						#   デフォルト待ち時間(秒)
		"defWaitSkip"		: 10,						#   デフォルトスキップ時間(秒)
		"defLongWaitSec"	: 60,						#   デフォルト 長い待ち時間(秒)
		
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
		"(dummy)"				: 0
	}

	DEF_DISPPATH = "script/disp/"

	DEF_STR_DISPFILE = {
		"MainConsole"			: DEF_DISPPATH + "main_console.disp",
		"(dummy)"				: 0
	}

#############################
# 定数
	DEF_LOCK_LOOPTIME = 2									#ロック解除待ち
	DEF_LOCK_WAITCNT  = 30									#  待ち時間: DEF_LOCK_LOOPTIME * DEF_LOCK_WAITCNT
	DEF_TEST_MODE     = "bottest"							#テストモード(引数文字)
	DEF_DATA_BOUNDARY = "|,|"



#############################
# 変数
	FLG_Test_Mode    = False								#テストモード有無
	
	OBJ_Tw_IF = ""											#Twitter I/F
	OBJ_DB_IF = ""											#DB I/F
	OBJ_L     = ""											#ログ用



