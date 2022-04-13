#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : セットアップ
#####################################################

from osif import CLS_OSIF
from filectrl import CLS_File
from db_if import CLS_DB_IF
from twitter_if import CLS_Twitter_IF
from gval import gVal
#####################################################
class CLS_Setup():
#####################################################

#####################################################
# 初期化
#####################################################
	def __init__(self):
		return



#####################################################
# セットアップ
#####################################################
	def Setup( self, inPassWD=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Setup"
		
		CLS_OSIF.sPrn( "Lucibotをセットアップモードで起動しました" + '\n' )
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( inPassWD=inPassWD )
		if wSubRes['Result']!=True :
			return False
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			##DB初期化
			self.__initDB( gVal.OBJ_DB_IF.OBJ_DB )
			CLS_OSIF.sPrn( "データベースを初期化しました" + '\n' )
		
		#############################
		# ユーザチェック
		wSubRes = gVal.OBJ_DB_IF.CheckUserData()
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			return False
		
		wTwitterAccount = wSubRes['Responce']['Account']
		#############################
		# ユーザありの場合
		if wSubRes['Responce']['detect']==True :
			wStr = "ユーザ " + wTwitterAccount + " は既に登録されています。キーの変更をおこないますか？" + '\n'
			CLS_OSIF.sPrn( wStr )
			wSelect = CLS_OSIF.sInp( "変更する？(y/N)=> " )
			if wSelect!="y" :
				###キャンセル
				wStr = "ユーザデータは正常でした。" + '\n'
				CLS_OSIF.sPrn( wStr )
				
				gVal.OBJ_DB_IF.Close()
				wRes['Result'] = True
				return wRes
		
		### ※ユーザ変更あり
		
		#############################
		# Twitterキーの入力と接続テスト
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wSubRes = gVal.OBJ_Tw_IF.SetTwitter( wTwitterAccount )
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			return False
		
		#############################
		# ユーザを登録、もしくは更新する
		wSubRes = gVal.OBJ_DB_IF.SetUserData( wSubRes['Responce'] )
		if wSubRes['Result']!=True :
			gVal.OBJ_DB_IF.Close()
			return False
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		return True



#####################################################
# 全初期化
#   作業ファイルとDBを全て初期化する
#####################################################
	def AllInit(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "AllInit"
		
		#############################
		# 実行の確認
		wStr = "データベースと全ての作業ファイルをクリアします。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "よろしいですか？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		#############################
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがなければ作成する
			if CLS_File.sMkdir( gVal.DEF_USERDATA_PATH )!=True :
				wRes['Reason'] = "フォルダの作成に失敗しました: path=" + gVal.DEF_USERDATA_PATH
				CLS_OSIF.sErr( wRes )
				return False
		
		#############################
		# DBに接続 (接続情報の作成)
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True :
			return False
		
		#############################
		# DB初期化
		self.__initDB( gVal.OBJ_DB_IF.OBJ_DB )
		CLS_OSIF.sPrn( "データベースを初期化しました" + '\n' )
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		CLS_OSIF.sPrn( "全初期化が正常終了しました。" )
		
		#############################
		# セットアップの確認
		wStr = "続いてセットアップを続行しますか。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "セットアップする？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		###入力の手間を省くため、パスワードを引き継ぐ
		self.Setup()
		return True



#####################################################
# クリア
#   一部のDBを初期化する
#####################################################
	def Clear(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Clear"
		
		#############################
		# 実行の確認
		wStr = "ログと、キーユーザ検索データ用のデータベースをクリアします。" + '\n'
		CLS_OSIF.sPrn( wStr )
		wSelect = CLS_OSIF.sInp( "よろしいですか？(y/N)=> " )
		if wSelect!="y" :
			##キャンセル
			return True
		
		#############################
		# DBに接続 (接続情報の作成)
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True :
			return False
		
		#############################
		# DB初期化
		self.__create_TBL_LOG_DATA( gVal.OBJ_DB_IF.OBJ_DB )
		
		#############################
		# 終わり
		gVal.OBJ_DB_IF.Close()
		CLS_OSIF.sPrn( "クリアが正常終了しました。" )
		
		return True



#####################################################
# データベースの初期化
#####################################################
	def __initDB( self, inDBobj ):
		self.__create_TBL_USER_DATA( inDBobj )
		self.__create_TBL_FAVOUSER_DATA( inDBobj )
		self.__create_TBL_LOG_DATA( inDBobj )
		self.__create_TBL_TRAFFIC_DATA( inDBobj )
		return True

	#####################################################
	def __allDrop( self, inDBobj ):
		wQuery = "drop table if exists tbl_user_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_favouser_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_log_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_traffic_data ;"
		inOBJ_DB.RunQuery( wQuery )
		return True



#####################################################
# テーブル作成: TBL_USER_DATA
#####################################################
	def __create_TBL_USER_DATA( self, inOBJ_DB, inTBLname="tbl_user_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"apikey      TEXT  NOT NULL," + \
					"apisecret   TEXT  NOT NULL," + \
					"acctoken    TEXT  NOT NULL," + \
					"accsecret   TEXT  NOT NULL," + \
					"bearer      TEXT  NOT NULL," + \
					"locked      BOOL  DEFAULT false," + \
					"lupdate     TIMESTAMP," + \
					"trendtag    TEXT," + \
					"favodate    TIMESTAMP," + \
					" PRIMARY KEY ( twitterid ) ) ;"

##					"twitterid   記録したユーザ(Twitter ID)
##					"apikey      Twitter Devで取ったAPI key
##					"apisecret   Twitter Devで取ったAPI secret
##					"acctoken    Twitter Devで取ったAccess Token Key
##					"accsecret   Twitter Devで取ったAccess Token secret
##					"locked      
##					"lupdate     
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_LOG_DATA
#####################################################
	def __create_TBL_LOG_DATA( self, inOBJ_DB, inTBLname="tbl_log_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"level       CHAR(1) DEFAULT '-'," + \
					"log_class   TEXT  NOT NULL," + \
					"log_func    TEXT  NOT NULL," + \
					"reason      TEXT  NOT NULL," + \
					"lupdate     TIMESTAMP" + \
					" ) ;"
		
##					"twitterid   記録したユーザ(Twitter ID)
##					"level       ログレベル
##					"log_class   ログクラス
##					"log_func    ログ関数
##					"reason      理由
##					"lupdate     記録日時
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_FAVOUSER_DATA
#####################################################
	def __create_TBL_FAVOUSER_DATA( self, inOBJ_DB, inTBLname="tbl_favouser_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"regdate     TIMESTAMP," + \
					"id          TEXT  NOT NULL," + \
					"screen_name TEXT  NOT NULL," + \
					"senddate    TIMESTAMP," + \
					"sended      BOOL  DEFAULT false," + \
					"send_cnt      INTEGER DEFAULT 0," + \
					"favo_cnt      INTEGER DEFAULT 0," + \
					"now_favo_cnt  INTEGER DEFAULT 0," + \
					"favo_id       TEXT  NOT NULL," + \
					"favo_date     TIMESTAMP " + \
					" ) ;"
		
##					"twitterid   記録したユーザ(Twitter ID)
###					"regdate     登録日
###					"id          Twitter ID
###					"screen_name Twitter ユーザ名(英語)
###					"senddate    最終送信日
###					"sended      送信済か (False=送信対象)
###					"send_cnt      送信回数(累計)
###					"favo_cnt      いいね回数(累計)
###					"now_favo_cnt  いいね回数(前回記録～現在まで)
###					"favo_id       最終いいねツイートID
###					"favo_date     最終いいねツイート日時
###
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_TRAFFIC_DATA
#####################################################
	def __create_TBL_TRAFFIC_DATA( self, inOBJ_DB, inTBLname="tbl_traffic_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"regdate     TIMESTAMP," + \
					"update      TIMESTAMP," + \
					"day         TEXT  NOT NULL," + \
					"reported  BOOL  DEFAULT false," + \
					"timeline  INTEGER DEFAULT 0," + \
					"runbot      INTEGER DEFAULT 0," + \
					"runapi      INTEGER DEFAULT 0," + \
					"now_favo  INTEGER DEFAULT 0," + \
					"rem_favo  INTEGER DEFAULT 0," + \
					"get_reaction  INTEGER DEFAULT 0," + \
					"send_tweet    INTEGER DEFAULT 0," + \
					"db_req      INTEGER DEFAULT 0," + \
					"db_ins      INTEGER DEFAULT 0," + \
					"db_up       INTEGER DEFAULT 0," + \
					"db_del      INTEGER DEFAULT 0 " + \
					" ) ;"
		
		inOBJ_DB.RunQuery( wQuery )
		return



