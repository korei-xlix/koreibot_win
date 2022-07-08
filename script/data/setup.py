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
###	def Setup( self, inPassWD=None ):
	def Setup( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Setup"
		
		CLS_OSIF.sPrn( "セットアップモードで起動しました" + '\n' )
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
###		wSubRes = gVal.OBJ_DB_IF.Connect( inPassWD=inPassWD )
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
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
###	def AllInit(self):
	def AllInit( self, inData ):
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
		# DBに接続 (接続情報の作成)
		gVal.OBJ_DB_IF = CLS_DB_IF()
###		wSubRes = gVal.OBJ_DB_IF.Connect()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
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
# データ追加モード
#####################################################
###	def Add( self, inWordOnly=False, inDBInit=False ):
	def Add( self, inData, inWordOnly=False, inDBInit=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Add"
		
		if inWordOnly==False :
			CLS_OSIF.sPrn( "〇 追加データをデータベースに追加します" + '\n' )
		else:
			CLS_OSIF.sPrn( "● 禁止ワードをデータベースに追加します" + '\n' )
		
		#############################
		# データアーカイブのあるフォルダの存在チェック
		if CLS_File.sExist( gVal.STR_SystemInfo['EXT_FilePath'] )!=True :
			## フォルダがないと失敗扱い
			wRes['Reason'] = "アーカイブのフォルダがありません: path=" + str( gVal.STR_SystemInfo['EXT_FilePath'] )
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# デフォルトの除外ユーザ・文字の読み出し
		# ・除外ファイルの解凍
		# ・読み出し
		# ・解凍の削除
		
		###デフォルト除外文字ファイルの解凍
		#    アーカイブのフォルダパス
		#    アーカイブ解凍先
		wExcWordArc_Path      = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['ExcWordArc']
		wMelt_ExcWordArc_Path = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path']
		if CLS_File.sArciveMelt( inSrcPath=wExcWordArc_Path, inDstPath=wMelt_ExcWordArc_Path )!=True :
			wRes['Reason'] = "デフォルト除外文字ファイルの解凍に失敗しました: srcpath=" + wExcWordArc_Path + " dstpath=" + wMelt_ExcWordArc_Path
			CLS_OSIF.sErr( wRes )
			return False
		
		###ローカルに読み出し
		#    除外データ 文字列ファイル
		wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ExcWord']
		wARR_ExcWord = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcWord )!=True :
			wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
			CLS_OSIF.sErr( wRes )
			return False
		
		if inWordOnly==False :
			#    禁止ユーザ
			wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ExcUser']
			wARR_ExcUser = []
			if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcUser )!=True :
				wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
				CLS_OSIF.sErr( wRes )
				return False
			
			#    リストいいね指定ファイル
			wFilePath = str( gVal.STR_SystemInfo['EXT_FilePath'] ) + gVal.DEF_STR_FILE['Melt_ExcWordArc_path'] + gVal.DEF_STR_FILE['Melt_ListFavo']
			wARR_ListFavo = []
			if CLS_File.sReadFile( wFilePath, outLine=wARR_ListFavo )!=True :
				wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
				CLS_OSIF.sErr( wRes )
				return False
		
		###解凍したフォルダ削除
		if CLS_File.sRmtree( wMelt_ExcWordArc_Path )!=True :
			wRes['Reason'] = "解凍フォルダの削除に失敗しました: path=" + wMelt_ExcWordArc_Path
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# DBに接続 (接続情報の作成)
		gVal.OBJ_DB_IF = CLS_DB_IF()
###		wSubRes = gVal.OBJ_DB_IF.Connect()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
		if wSubRes['Result']!=True or wSubRes['Responce']!=True :
			return False
		
		#############################
		# データベースを初期化する
		# ※初期化しないほうが便利
		if inDBInit==True and inWordOnly==False :
			self.__create_TBL_EXC_WORD( gVal.OBJ_DB_IF.OBJ_DB )
		
		#############################
		# 除外ユーザ名、文字、プロファイルの設定
		wSubRes = gVal.OBJ_DB_IF.SetExeWord( wARR_ExcWord )
		if wSubRes['Result']!=True :
			return False
		
		if inWordOnly==False :
			#############################
			# 禁止ユーザの設定
			wSubRes = gVal.OBJ_DB_IF.SetExeUser( wARR_ExcUser )
			if wSubRes['Result']!=True :
				return False
			
			#############################
			# リストいいね指定の設定
			wSubRes = gVal.OBJ_DB_IF.SetListFavo( wARR_ListFavo )
			if wSubRes['Result']!=True :
				return False
		
		#############################
		# DBを閉じる
		gVal.OBJ_DB_IF.Close()
		
		#############################
		# 正常終了
		CLS_OSIF.sPrn( "データの追加が正常終了しました。" )
		return True



#####################################################
# クリア
#   一部のDBを初期化する
#####################################################
###	def Clear(self):
	def Clear( self, inData ):
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
###		wSubRes = gVal.OBJ_DB_IF.Connect()
		wSubRes = gVal.OBJ_DB_IF.Connect( inData )
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
		self.__create_TBL_TWITTER_DATA( inDBobj )
		self.__create_TBL_FAVOUSER_DATA( inDBobj )
		self.__create_TBL_LOG_DATA( inDBobj )
		self.__create_TBL_TRAFFIC_DATA( inDBobj )
		self.__create_TBL_EXC_WORD( inDBobj )
		self.__create_TBL_EXC_USER( inDBobj )
		self.__create_TBL_CAUTION_TWEET( inDBobj )
		self.__create_TBL_SEARCH_WORD( inDBobj )
		self.__create_TBL_LIST_FAVO( inDBobj )
		return True

	#####################################################
	def __allDrop( self, inDBobj ):
		wQuery = "drop table if exists tbl_user_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_twitter_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_favouser_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_log_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_traffic_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_exc_word ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_exc_user ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_caution_tweet ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_search_word ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_list_favo ;"
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
					"regdate     TIMESTAMP," + \
					"locked      BOOL  DEFAULT false," + \
					"lupdate     TIMESTAMP," + \
					"fst_date    TIMESTAMP," + \
					"end_date    TIMESTAMP," + \
					"week_date   TIMESTAMP," + \
					"day_date    TIMESTAMP," + \
					"trendtag    TEXT," + \
					"list_id     TEXT," + \
					"list_name   TEXT," + \
					" PRIMARY KEY ( twitterid ) ) ;"

##					"twitterid   記録したユーザ(Twitter ID)
##					"regdate     登録日時
##					"locked      排他ロック true=ロックON
##					"lupdate     排他日時
##					"fst_date    処理開始日時(最終実行)
##					"end_date    処理終了日時(最終実行)
##					"week_date   週間 開始日時
##					"day_date    1日  開始日時
##					"trendtag    トレンド送信タグ
##					"list_id     リスト通知 リストID(数値)
##					"listname    リスト通知 リスト名
##
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_TWITTER_DATA
#####################################################
	def __create_TBL_TWITTER_DATA( self, inOBJ_DB, inTBLname="tbl_twitter_data" ):
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
					"bearer      TEXT  NOT NULL " + \
					" PRIMARY KEY ( twitterid ) ) ;"

##					"twitterid   記録したユーザ(Twitter ID)
##					"apikey      Twitter Devで取ったAPI key
##					"apisecret   Twitter Devで取ったAPI secret
##					"acctoken    Twitter Devで取ったAccess Token Key
##					"accsecret   Twitter Devで取ったAccess Token secret
##					"bearer      Twitter Devで取ったbearer
##
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
					"twitterid     TEXT  NOT NULL," + \
					"regdate       TIMESTAMP," + \
					"upddate       TIMESTAMP," + \
					"id            TEXT  NOT NULL," + \
					"screen_name   TEXT  NOT NULL," + \
					"level_tag     TEXT  NOT NULL," + \
					"send_date     TIMESTAMP," + \
					"send_cnt      INTEGER DEFAULT 0," + \
					"rfavo_id      TEXT  NOT NULL," + \
					"rfavo_date    TIMESTAMP," + \
					"rfavo_cnt     INTEGER DEFAULT 0," + \
					"rfavo_n_cnt   INTEGER DEFAULT 0," + \
					"pfavo_id      TEXT  NOT NULL," + \
					"pfavo_date    TIMESTAMP, " + \
					"pfavo_cnt     INTEGER DEFAULT 0," + \
					"list_date     TIMESTAMP," + \
					"myfollow      BOOL  DEFAULT false," + \
					"myfollow_date TIMESTAMP, " + \
					"follower      BOOL  DEFAULT false," + \
					"follower_date TIMESTAMP, " + \
					"flg_save      BOOL  DEFAULT false " + \
					" ) ;"
		
##					"twitterid     記録したユーザ(Twitter ID)
##					"regdate       登録日時
##					"upddate       更新日時(最終)
##					"id            Twitter ID(数値)
##					"screen_name   Twitter ユーザ名(英語)
##					"level_tag     レベルタグ(ユーザの親密度 指標)
##					"send_date     トロフィー送信日時
##					"send_cnt      トロフィー送信回数(累計)
##					"rfavo_id      いいね受信(このユーザがいいねした) ツイートID
##					"rfavo_date    いいね受信日時
##					"rfavo_cnt     いいね受信回数(総数)
##					"rfavo_n_cnt   いいね受信回数(今周)
##					"pfavo_id      いいね送信(このユーザのツイート) ツイートID
##					"pfavo_date    いいね送信日時
##					"pfavo_cnt     いいね送信回数(総数)
##					"list_date     リスト日時
##					"myfollow      フォロー者 true=フォロー者
##					"myfollow_date フォロー日時
##					"follower      フォロワー(被フォロー) true=フォロワー
##					"follower_date 被フォロー日時
##					"flg_save      自動削除禁止 true=削除しない
###
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_LIST_FAVO
#####################################################
	def __create_TBL_LIST_FAVO( self, inOBJ_DB, inTBLname="tbl_list_favo" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"id          TEXT  NOT NULL," + \
					"list_name   TEXT  NOT NULL," + \
					"user_id     TEXT  NOT NULL," + \
					"screen_name TEXT  NOT NULL," + \
					"valid       BOOL  DEFAULT true," + \
					"follow      BOOL  DEFAULT false, " + \
					"caution     BOOL  DEFAULT false, " + \
					"sensitive   BOOL  DEFAULT false, " + \
					"auto_rem    BOOL  DEFAULT false " + \
					" ) ;"
		
##					"twitterid   記録したユーザ(Twitter ID)
##					"id          Listのid
##					"list_name   Listの名前
##					"user_id     Listのユーザのid
##					"screen_name Listのユーザのscreen_name
##					"valid       有効か True=有効
##					"follow      フォロー者、フォロワーを含める
##					"caution     リストフォロー時警告を出す
##					"sensitive   センシティブツイートを含める
##					"auto_rem    自動リムーブ有効
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_EXC_WORD
#####################################################
	def __create_TBL_EXC_WORD( self, inOBJ_DB, inTBLname="tbl_exc_word" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"regdate     TIMESTAMP," + \
					"word        TEXT  NOT NULL, " + \
					"report      BOOL  DEFAULT false," + \
					" PRIMARY KEY ( word ) ) ;"
		
##					"regdate     DB登録日時
##					"word        禁止ワード
##					"report      true= 通報対象
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_EXC_USER
#####################################################
	def __create_TBL_EXC_USER( self, inOBJ_DB, inTBLname="tbl_exc_user" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"regdate     TIMESTAMP," + \
					"screen_name TEXT  NOT NULL, " + \
					"report      BOOL  DEFAULT false," + \
					"vip         BOOL  DEFAULT false," + \
					"rel_date    TIMESTAMP," + \
					"memo        TEXT, " + \
					" PRIMARY KEY ( screen_name ) ) ;"
		
##					"regdate     DB登録日時
##					"screen_name 禁止ユーザ名
##					"report      true= 通報対象
##					"vip         true= 監視外(ログ記録なし)
##					"rel_date    禁止解除日時(noneは自動解除しない)
##					"memo        自由記載(メモ)
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_CAUTION_TWEET
#####################################################
	def __create_TBL_CAUTION_TWEET( self, inOBJ_DB, inTBLname="tbl_caution_tweet" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"regdate     TIMESTAMP," + \
					"tweet_id    TEXT  NOT NULL," + \
					"id          TEXT  NOT NULL," + \
					"screen_name TEXT  NOT NULL, " + \
					" PRIMARY KEY ( id ) ) ;"
		
##					"regdate     DB登録日時
##					"tweet_id    Tweet ID
##					"id          ユーザID
##					"screen_name ユーザ名
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_SEARCH_WORD
#####################################################
	def __create_TBL_SEARCH_WORD( self, inOBJ_DB, inTBLname="tbl_search_word" ):
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
					"word        TEXT  NOT NULL, " + \
					"hit_cnt     INTEGER DEFAULT 0," + \
					"favo_cnt    INTEGER DEFAULT 0," + \
					"update_date TIMESTAMP," + \
					"valid       BOOL  DEFAULT false " + \
					" ) ;"
		
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
					"now_favo    INTEGER DEFAULT 0," + \
					"get_favo    INTEGER DEFAULT 0," + \
					"rem_favo    INTEGER DEFAULT 0," + \
					"get_reaction  INTEGER DEFAULT 0," + \
					"send_tweet    INTEGER DEFAULT 0," + \
					"db_req      INTEGER DEFAULT 0," + \
					"db_ins      INTEGER DEFAULT 0," + \
					"db_up       INTEGER DEFAULT 0," + \
					"db_del      INTEGER DEFAULT 0 " + \
					" ) ;"
		
		inOBJ_DB.RunQuery( wQuery )
		return



