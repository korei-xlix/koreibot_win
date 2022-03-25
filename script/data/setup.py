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
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがなければ作成する
			if CLS_File.sMkdir( gVal.DEF_USERDATA_PATH )!=True :
				wRes['Reason'] = "フォルダの作成に失敗しました: path=" + gVal.DEF_USERDATA_PATH
				CLS_OSIF.sErr( wRes )
				return False
		
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
		self.Add()
		return True



#####################################################
# データ追加モード
#####################################################
	def Add( self, inPassWD=None, inDBInit=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Setup"
		wRes['Func']  = "Add"
		
		CLS_OSIF.sPrn( "追加データをデータベースに追加します" + '\n' )
		
		#############################
		# ユーザフォルダの存在チェック
		if CLS_File.sExist( gVal.DEF_USERDATA_PATH )!=True :
			## フォルダがないと失敗扱い
			wRes['Reason'] = "ユーザフォルダがありません: path=" + gVal.DEF_USERDATA_PATH
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# デフォルトの除外ユーザ・文字の読み出し
		# ・除外ファイルの解凍
		# ・読み出し
		# ・解凍の削除
		
		###デフォルト除外文字ファイルの解凍
		wExcWordArc_Path = gVal.DEF_STR_FILE['ExcWordArc']											#アーカイブ
		wMelt_ExcWordArc_Path = gVal.DEF_USERDATA_PATH + gVal.DEF_STR_FILE['Melt_ExcWordArc_path']	#アーカイブ解凍先
		if CLS_File.sArciveMelt( inSrcPath=wExcWordArc_Path, inDstPath=gVal.DEF_USERDATA_PATH )!=True :
			wRes['Reason'] = "デフォルト除外文字ファイルの解凍に失敗しました: srcpath=" + wExcWordArc_Path + " dstpath=" + wMelt_ExcWordArc_Path
			CLS_OSIF.sErr( wRes )
			return False
		
		###ローカルに読み出し
		wFilePath = gVal.DEF_USERDATA_PATH + gVal.DEF_STR_FILE['Melt_ExcUser']
		wARR_ExcUser = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcUser )!=True :
			wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
			CLS_OSIF.sErr( wRes )
			return False
		
		wFilePath = gVal.DEF_USERDATA_PATH + gVal.DEF_STR_FILE['Melt_ExcWord']
		wARR_ExcWord = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ExcWord )!=True :
			wRes['Reason'] = "解凍ファイルが見つかりません: path=" + wFilePath
			CLS_OSIF.sErr( wRes )
			return False
		
		wFilePath = gVal.DEF_USERDATA_PATH + gVal.DEF_STR_FILE['Melt_ActionRetweet']
		wARR_ActionRetweet = []
		if CLS_File.sReadFile( wFilePath, outLine=wARR_ActionRetweet )!=True :
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
		wSubRes = gVal.OBJ_DB_IF.Connect()
		if wSubRes['Result']!=True or wSubRes['Responce']!=True :
			return False
		
		#############################
		# データベースを初期化する
		# ※初期化しないほうが便利
		if inDBInit==True :
			self.__create_TBL_EXC_USER( gVal.OBJ_DB_IF.OBJ_DB )
			self.__create_TBL_EXC_WORD( gVal.OBJ_DB_IF.OBJ_DB )
			self.__create_TBL_ACTION_RETWEET( gVal.OBJ_DB_IF.OBJ_DB )
			self.__create_TBL_FOLLOW_AGENT( gVal.OBJ_DB_IF.OBJ_DB )
			self.__create_TBL_AUTO_RETWEET( gVal.OBJ_DB_IF.OBJ_DB )
		
		#############################
		# 除外ユーザ名、文字、プロファイルの設定
		wSubRes = gVal.OBJ_DB_IF.SetExeUser( wARR_ExcUser )
		if wSubRes['Result']!=True :
			return False
		wSubRes = gVal.OBJ_DB_IF.SetExeWord( wARR_ExcWord )
		if wSubRes['Result']!=True :
			return False
		wSubRes = gVal.OBJ_DB_IF.SetActionRetweet( wARR_ActionRetweet )
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
		self.__create_TBL_FOLLOW_AGENT( gVal.OBJ_DB_IF.OBJ_DB )
		self.__create_TBL_AUTO_RETWEET( gVal.OBJ_DB_IF.OBJ_DB )
		
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
		self.__create_TBL_LOG_DATA( inDBobj )
		self.__create_TBL_FAVO_DATA( inDBobj )
		self.__create_TBL_FOLLOWER_DATA( inDBobj )
		self.__create_TBL_EXC_USER( inDBobj )
		self.__create_TBL_EXC_WORD( inDBobj )
		self.__create_TBL_ACTION_RETWEET( inDBobj )
		self.__create_TBL_FOLLOW_AGENT( inDBobj )
		self.__create_TBL_AUTO_RETWEET( inDBobj )
		self.__create_TBL_TRAFFIC_DATA( inDBobj )
		return True

	#####################################################
	def __allDrop( self, inDBobj ):
		wQuery = "drop table if exists tbl_user_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_log_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_favo_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_follower_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_exc_user ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_exc_word ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_traffic_data ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_action_retweet ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_follow_agent ;"
		inOBJ_DB.RunQuery( wQuery )
		wQuery = "drop table if exists tbl_auto_retweet ;"
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
# テーブル作成: TBL_FAVO_DATA
#####################################################
	def __create_TBL_FAVO_DATA( self, inOBJ_DB, inTBLname="tbl_favo_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"regdate     TIMESTAMP," + \
					"limited     BOOL  DEFAULT false," + \
					"removed     BOOL  DEFAULT false," + \
					"id          TEXT  NOT NULL," + \
					"user_id     TEXT  NOT NULL," + \
					"text        TEXT  NOT NULL," + \
					"created_at  TIMESTAMP" + \
					" ) ;"
		
##					"twitterid   記録したユーザ(Twitter ID)
##					"regdate     DB登録日時
##					"limited     ファボ期限切れ =ファボ解除対象
##					"removed     ファボ解除済み
##					"id          ツイート ID
##					"user_id     ツイート ユーザID
##					"text        ツイート 内容
##					"created_at  ツイート 日時
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_FOLLOWER_DATA
#####################################################
	def __create_TBL_FOLLOWER_DATA( self, inOBJ_DB, inTBLname="tbl_follower_data" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"twitterid   TEXT  NOT NULL," + \
					"regdate     TIMESTAMP," + \
					"r_myfollow  BOOL  DEFAULT false," + \
					"r_remove    BOOL  DEFAULT false," + \
					"rc_myfollow BOOL  DEFAULT false," + \
					"rc_follower BOOL  DEFAULT false," + \
					"rc_blockby  BOOL  DEFAULT false," + \
					"foldate     TIMESTAMP," + \
					"adm_agent   BOOL  DEFAULT false," + \
					"vipuser     BOOL  DEFAULT false," + \
					"un_follower BOOL  DEFAULT false," + \
					"un_fol_lock BOOL  DEFAULT false," + \
					"un_fol_cnt  INTEGER DEFAULT 0," + \
					"limited     BOOL  DEFAULT false," + \
					"removed     BOOL  DEFAULT false," + \
					"get_agent   BOOL  DEFAULT false," + \
					"id          TEXT  NOT NULL," + \
					"name        TEXT  NOT NULL," + \
					"screen_name TEXT  NOT NULL," + \
					"lastcount   INTEGER," + \
					"lastdate    TIMESTAMP," + \
					"reason      TEXT," + \
					"favo_id      TEXT," + \
					"favo_date    TIMESTAMP," + \
					"favo_cnt    INTEGER DEFAULT 0," + \
					"favo_f_cnt  INTEGER DEFAULT 0," + \
					"r_favo_id   TEXT," + \
					"r_favo_date TIMESTAMP," + \
					"r_favo_cnt  INTEGER DEFAULT 0," + \
					"r_favo_f_cnt INTEGER DEFAULT 0, " + \
					"rt_cnt      INTEGER DEFAULT 0," + \
					"tordate     TIMESTAMP," + \
					"tor_cnt     INTEGER DEFAULT 0," + \
					"week_cnt    INTEGER DEFAULT 0 " + \
					" ) ;"
		
##					"twitterid   記録したユーザ(Twitter ID)
##					"regdate     DB登録日時
##					
##					"r_myfollow  1度でもフォローしたことがある
##					"r_remove    1度でもリムーブされたことがある
##					"rc_myfollow 前のチェックでフォローしてた
##					"rc_follower 前のチェックでフォローされてた（フォロワー）
##					"rc_blockby  前のチェックでブロックを検出した
##					"foldate     最初にフォローした日
##					
##					"adm_agent   botの管理下に置く true=管理下(normal,un_followerユーザ)
##					"un_follower 非フォロワー      true=非フォロワー(un_followerユーザ)
##					"limited     自動リムーブ対象 or 非フォロワー化対象
##					"removed     botからリムーブ処理済み
##					"get_agent   候補にセレクト済み（定期でリセット）
##					
##					"id          ユーザTwitter ID【一意】
##					"user_name   ユーザ名
##					"screen_name スクリーン名
##					"lastcount   最後のツイート数
##					"lastdate    最後のツイートの日時
##					"reason      メモ変わり
##					
##					"favo_id     botからファボった相手ツイートID
##					"favo_date   botからファボった日時
##					"favo_cnt    botからファボった回数
##					"favo_f_cnt  botからのファボ処理が連続して失敗した回数
##					"r_favo_id   相手がファボったツイートID
##					"r_favo_date 相手がファボった日時
##					"r_favo_cnt  相手がファボった回数
##					"rt_cnt      連続リツイート回数
##					"arashi_cnt  荒らし連続回数
##					"arashi_r_id 荒らし理由 None=荒らしではない
##					"tordate     トロフィー獲得日時
##					"tor_cnt     トロフィー獲得回数
		
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
					"choice      BOOL  DEFAULT true," + \
					"word        TEXT  NOT NULL, " + \
					" PRIMARY KEY ( word ) ) ;"
		
##					"regdate     DB登録日時
##					"keyword     検索キーワード
		
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
					"choice      BOOL  DEFAULT true," + \
					"word        TEXT  NOT NULL, " + \
					" PRIMARY KEY ( word ) ) ;"
		
##					"regdate     DB登録日時
##					"keyword     検索キーワード
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_ACTION_RETWEET
#####################################################
	def __create_TBL_ACTION_RETWEET( self, inOBJ_DB, inTBLname="tbl_action_retweet" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"regdate     TIMESTAMP," + \
					"choice      BOOL  DEFAULT true," + \
					"word        TEXT  NOT NULL, " + \
					" PRIMARY KEY ( word ) ) ;"
		
##					"regdate     DB登録日時
##					"keyword     検索キーワード
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_FOLLOW_AGENT
#####################################################
	def __create_TBL_FOLLOW_AGENT( self, inOBJ_DB, inTBLname="tbl_follow_agent" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"regdate     TIMESTAMP," + \
					"id          TEXT  NOT NULL, " + \
					" PRIMARY KEY ( id ) ) ;"
		
		inOBJ_DB.RunQuery( wQuery )
		return



#####################################################
# テーブル作成: TBL_AUTO_RETWEET
#####################################################
	def __create_TBL_AUTO_RETWEET( self, inOBJ_DB, inTBLname="tbl_auto_retweet" ):
		#############################
		# テーブルのドロップ
		wQuery = "drop table if exists " + inTBLname + ";"
		inOBJ_DB.RunQuery( wQuery )
		
		#############################
		# テーブル枠の作成
		wQuery = "create table " + inTBLname + "(" + \
					"regdate     TIMESTAMP," + \
					"id          TEXT  NOT NULL, " + \
					" PRIMARY KEY ( id ) ) ;"
		
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
					"now_myfollow    INTEGER DEFAULT 0," + \
					"now_follower    INTEGER DEFAULT 0," + \
					"get_myfollow    INTEGER DEFAULT 0," + \
					"get_follower    INTEGER DEFAULT 0," + \
					"rem_myfollow    INTEGER DEFAULT 0," + \
					"rem_follower    INTEGER DEFAULT 0," + \
					"now_unfollow  INTEGER DEFAULT 0," + \
					"now_remove    INTEGER DEFAULT 0," + \
					"run_unfollow      INTEGER DEFAULT 0," + \
					"run_unfollowrem   INTEGER DEFAULT 0," + \
					"run_autoremove    INTEGER DEFAULT 0," + \
					"run_muteremove    INTEGER DEFAULT 0," + \
					"now_agent     INTEGER DEFAULT 0," + \
					"now_vipuser   INTEGER DEFAULT 0," + \
					"get_reaction  INTEGER DEFAULT 0," + \
					"now_favo  INTEGER DEFAULT 0," + \
					"get_favo  INTEGER DEFAULT 0," + \
					"rem_favo  INTEGER DEFAULT 0," + \
					"send_tweet    INTEGER DEFAULT 0," + \
					"send_retweet  INTEGER DEFAULT 0," + \
					"db_req      INTEGER DEFAULT 0," + \
					"db_ins      INTEGER DEFAULT 0," + \
					"db_up       INTEGER DEFAULT 0," + \
					"db_del      INTEGER DEFAULT 0 " + \
					" ) ;"
		
		inOBJ_DB.RunQuery( wQuery )
		return



