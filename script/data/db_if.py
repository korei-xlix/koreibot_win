#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : Database I/F
#####################################################
from postgresql_use import CLS_PostgreSQL_Use

from osif import CLS_OSIF
from gval import gVal
#####################################################
class CLS_DB_IF() :
#####################################################
	OBJ_DB = ""				#DBオブジェクト
	CHR_PassWD = None
	
	ARR_FollowerDataID = []		#  フォロワー情報ID

#####################################################
# Init
#####################################################
	def __init__(self):
		return



#####################################################
# フォロワー情報
#####################################################
#####################################################
# フォロワー情報 フォロワーID一覧取得
#####################################################
	def GetFollowerDataID(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFollowerDataID"
		
		#############################
		# DBのフォロワー一覧取得(idのみ)
		wQuery = "select id from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		#############################
		# リスト型に整形
		wARR_RateFollowers = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateFollowers )
		
		self.ARR_FollowerDataID = []
		self.ARR_FollowerDataID = wARR_RateFollowers
		#############################
		# 正常
		wRes['Responce'] = wARR_RateFollowers
		wRes['Result'] = True
		return wRes

	#####################################################
	def GetFollowerDataID_List(self):
		return self.ARR_FollowerDataID

	#####################################################
	def CheckFollowerData( self, inID ):
		if str( inID ) not in self.ARR_FollowerDataID :
			return False
		return True



#####################################################
# フォロワー情報 フォロワー情報取得
#####################################################
	def GetFollowerDataOne( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFollowerDataOne"
		
		wRes['Responce'] = None
		#############################
		# DBのフォロワー一覧取得(idのみ)
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"id = '" + str( inID ) + "' " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		#############################
		# 1個取得できたか
		if len(wResDB['Responce']['Data'])==0 :
			## ないのは正常で返す(ResponceはNoneのまま)
			wRes['Result'] = True
			return wRes
		if len(wResDB['Responce']['Data'])!=1 :
			## 1個ではない
			wRes['Reason'] = "Get data is failed : id=" + str(inID)
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateFollowers = {}
		self.OBJ_DB.ChgDict( wResDB['Responce']['Collum'], wResDB['Responce']['Data'], outDict=wARR_RateFollowers )
		
		wRes['Responce'] = wARR_RateFollowers[0]
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# フォロワー情報 初期挿入
#####################################################
	def InsertFollowerData( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "Connect"
		
		#############################
		# ユーザ情報の加工
		wID = str( inData['id'] )
		wUserName = str( inData['name'] ).replace( "'", "''" )
		wScreenName = str( inData['screen_name'] )
		
		#############################
		# 重複チェック
		if wID in self.ARR_FollowerDataID :
			##失敗
			wRes['Reason'] = "ID is exist : id=" + wID
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 時間の取得
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
		wDefTimeDate = "1901-01-01 00:00:00"
		
		#############################
		# SQLの作成
		wQuery = "insert into tbl_follower_data values ("
		wQuery = wQuery + "'" + gVal.STR_UserInfo['Account'] + "', "
		wQuery = wQuery + "'" + wTimeDate + "', "
		
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "'" + wTimeDate + "', "
		
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		
		wQuery = wQuery + "'" + wID + "', "
		wQuery = wQuery + "'" + wUserName + "', "
		wQuery = wQuery + "'" + wScreenName + "', "
		
		wQuery = wQuery + "0, "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		
		wQuery = wQuery + "'', "
		
		wQuery = wQuery + "'', "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "0, "
		
		wQuery = wQuery + "'', "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "0, "
		
		wQuery = wQuery + "0, "
		
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "0 "
		
		wQuery = wQuery + ") ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_ins'] += 1
		
		self.ARR_FollowerDataID.append( wID )
		#############################
		# 正常
		wRes['Result'] = True
		return wRes




#####################################################
# DBふぁぼ取得
#####################################################
	def GetFavoData(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_TwitterMain"
		wRes['Func']  = "GetFavoData"
		
		#############################
		# DBのいいね一覧取得
		wQuery = "select * from tbl_favo_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		#############################
		# 辞書型に整形
		wARR_RateFavo = {}
		self.OBJ_DB.ChgDict( wResDB['Responce']['Collum'], wResDB['Responce']['Data'], outDict=wARR_RateFavo )
		
		### 添え字をIDに差し替える
		wKeylist = wARR_RateFavo.keys()
		wARR_DBData = {}
		for wIndex in wKeylist :
			wID = str( wARR_RateFavo[wIndex]['id'] )
			wARR_DBData.update({ wID : wARR_RateFavo[wIndex] })
		
		wRes['Responce'] = wARR_DBData
		wRes['Result']   = True
		return wRes



#####################################################
# ふぁぼ情報 初期挿入
#####################################################
	def InsertFavoData( self, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertFavoData"
		
		#############################
		# ユーザ情報の加工
		wTweetID = str( inData["id"] )
		wID      = str( inData["user_id"] )
		wText    = inData["text"].replace( "'", "''" )
		
		#############################
		# 重複チェック
		
		### SQLの作成
		wQuery = " twitterid = '" + gVal.STR_UserInfo['Account'] + "' and "
		wQuery = wQuery + " id = '" + wID + "' "
		
		### SQLの実行
		wResDB = self.OBJ_DB.RunExist( "tbl_favo_data", wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		if wResDB['Responce']==True :
			##重複あり
			wRes['Reason'] = "Data is exist"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 時間の取得
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
		
		#############################
		# SQLの作成
		wQuery = "insert into tbl_favo_data values ("
		wQuery = wQuery + "'" + gVal.STR_UserInfo['Account'] + "', "
		wQuery = wQuery + "'" + wTimeDate + "', "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "'" + str( wTweetID ) + "', "
		wQuery = wQuery + "'" + str( wID ) + "', "
		wQuery = wQuery + "'" + str( wText ) + "', "
		wQuery = wQuery + "'" + str( inData['created_at'] ) + "' "
		wQuery = wQuery + ") ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_ins'] += 1
		
		self.ARR_FollowerDataID.append( wID )
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def InsertFavoData_Tweet( self, inUserID, inData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertFavoData_Tweet"
		
		#############################
		# 組み立て
		wData = {
			"id"		: inData['id'],
			"user_id"	: str( inUserID ),
			"text"		: inData['text'],
			"created_at" : inData['created_at']
		}
		
		#############################
		# DB追加
		wSubRes = self.InsertFavoData( wData )
		if wSubRes['Result']!=True :
			wRes['Reason'] = wSubRes['Reason']
			return wRes
		
		wRes['Result'] = True
		return wRes



#####################################################
# DB接続
#####################################################
	def Connect( self, inPassWD=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "Connect"
		
		if self.CHR_PassWD==None :
			wPassword = inPassWD
		else:
			wPassword = self.CHR_PassWD
		
		wRes['Responce'] = False
		#############################
		# パスワードが未設定なら入力を要求する
		if wPassword==None :
			wStr = "データベースに接続します。データベースのパスワードを入力してください。" + '\n'
			wStr = wStr + "  Hostname=" + gVal.DEF_BD_HOST + " Database=" + gVal.DEF_BD_NAME + " Username=" + gVal.DEF_BD_USER
			CLS_OSIF.sPrn( wStr )
			
			###入力受け付け
			wPassword = CLS_OSIF.sGpp( "Password: " )
		
		#############################
		# Postgreオブジェクトの作成
		self.OBJ_DB = CLS_PostgreSQL_Use()
		
		#############################
		# テスト
		wResDBconn = self.OBJ_DB.Create( gVal.DEF_BD_HOST, gVal.DEF_BD_NAME, gVal.DEF_BD_USER, wPassword )
		wResDB = self.OBJ_DB.GetDbStatus()
		if wResDBconn!=True :
			wRes['Reason'] = "DBの接続に失敗しました: reason=" + wResDB['Reason']
			CLS_OSIF.sErr( wRes )
			
			self.__connectFailView()
			return wRes
		
		#############################
		# 結果の確認
		if wResDB['Init']!=True :
			wRes['Reason'] = "DBが初期化できてません"
			CLS_OSIF.sErr( wRes )
			
			self.__connectFailView()
			return wRes
		
		#############################
		# 接続は正常
		self.CHR_PassWD = wPassword		#再ログイン用保存
		CLS_OSIF.sPrn( "データベースへ正常に接続しました。" + '\n' )
		wRes['Result'] = True
		
		#############################
		# DBの状態チェック
		wSubRes = self.CheckDB()
		if wSubRes['Result']!=True :
			return False
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			CLS_OSIF.sPrn( "テーブルが構築されていません" + '\n' )
			
			self.__connectFailView()
			return wRes
		
		###全て正常
		wRes['Responce'] = True
		return wRes

	def __connectFailView(self):
		if gVal.FLG_Test_Mode==False :
			return	#テストモードでなければ終わる
		
		#############################
		# DB接続情報を表示
		wStr =        "******************************" + '\n'
		wStr = wStr + "HOST    : " + gVal.DEF_BD_HOST + '\n'
		wStr = wStr + "DB NAME : " + gVal.DEF_BD_NAME + '\n'
		wStr = wStr + "DB USER : " + gVal.DEF_BD_USER + '\n'
		wStr = wStr + "******************************" + '\n'
		CLS_OSIF.sPrn( wStr )
		return



#####################################################
# DB切断
#####################################################
	def Close(self):
		self.OBJ_DB.Close()
		return True



#####################################################
# クエリ実行
#####################################################
	def RunQuery( self, inQuery=None, inTraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "RunQuery"
		
		#############################
		# 実行
		wResDB = self.OBJ_DB.RunQuery( inQuery )
		
		#############################
		# 実行結果の取得
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒックの計測
		if inTraffic==True :
			gVal.STR_TrafficInfo['db_req'] += 1
			
			if wResDB['Command']=="insert" or wResDB['Command']=="create" :
				gVal.STR_TrafficInfo['db_ins'] += 1
			elif wResDB['Command']=="update" :
				gVal.STR_TrafficInfo['db_up'] += 1
			elif wResDB['Command']=="delete" or wResDB['Command']=="drop" :
				gVal.STR_TrafficInfo['db_del'] += 1
		
		#############################
		# 正常
		wRes['Responce'] = wResDB['Responce']
		wRes['Result'] = True
		return wRes

	#####################################################
	# 辞書型に整形
	def ChgDict( self, inData ):
		wARR_DBData = {}
		self.OBJ_DB.ChgDict( inData['Collum'], inData['Data'], outDict=wARR_DBData )
		return wARR_DBData

	#####################################################
	# リスト型に整形
	def ChgList( self, inData ):
		wARR_DBData = []
		self.OBJ_DB.ChgList( inData['Data'], outList=wARR_DBData )
		return wARR_DBData

	#####################################################
	# 添え字をIDに差し替える
	def ChgDataID( self, inData ):
		wKeylist = inData.keys()
		
		wARR_RateData = {}
		for wIndex in wKeylist :
			wID = str( inData[wIndex]['id'] )
			wARR_RateData.update({ wID : inData[wIndex] })
		
		return wARR_RateData



#####################################################
# チェックデータベース
#####################################################
	def CheckDB(self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CheckDB"
		
		#############################
		# DBの状態チェック
		wResDB = self.OBJ_DB.RunTblExist( "tbl_user_data" )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##クエリ失敗
			wRes['Reason'] = "DBの状態チェック失敗: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Responce'] = wResDB['Responce']
		wRes['Result'] = True
		return wRes



#####################################################
# チェックユーザデータ
#####################################################
	def CheckUserData(self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CheckUserData"
		
		wRes['Responce'] = {}
		wRes['Responce'].update({
			"Account"   : None,
			"detect"    : False
		})
		
		#############################
		# TwitterIDの入力
		wStr = "Lucibotで使うユーザ登録をおこないます。" + '\n'
		wStr = wStr + "ここではTwitter IDと、Twitter Devで取得したキーを登録していきます。" + '\n'
		wStr = wStr + "Twitter IDを入力してください。"
		CLS_OSIF.sPrn( wStr )
		wTwitterAccount = CLS_OSIF.sInp( "Twitter ID？=> " )
		
		wRes['Responce']['Account'] = str( wTwitterAccount )
		#############################
		# ユーザ登録の確認 and 抽出
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + wTwitterAccount + "'" + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		##登録あり
		if len(wResDB['Responce']['Data'])==1 :
			wRes['Responce']['detect'] = True
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# ユーザデータ設定
#####################################################
	def SetUserData( self, inUserData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetUserData"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wStr = "PC時間取得失敗" + '\n'
			CLS_OSIF.sPrn( wStr )
			wTD['TimeDate'] = "1901-01-01 00:00:00"
		### wTD['TimeDate']
		
		#############################
		# テーブルチェック
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + inUserData['Account'] + "'" + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 登録してなければデータベースに登録する
		if len(wResDB['Responce']['Data'])==0 :
			wQuery = "insert into tbl_user_data values (" + \
						"'" + inUserData['Account'] + "'," + \
						"'" + inUserData['APIkey'] + "'," + \
						"'" + inUserData['APIsecret'] + "'," + \
						"'" + inUserData['ACCtoken'] + "'," + \
						"'" + inUserData['ACCsecret'] + "'," + \
						"'" + inUserData['Bearer'] + "'," + \
						"False," + \
						"'" + str(wTD['TimeDate']) + "' " + \
						") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
			wStr = "データベースにユーザ " + inUserData['Account'] + " を登録しました。" + '\n'
			CLS_OSIF.sPrn( wStr )
		#############################
		# 登録されていればキーを更新する
		elif len(wResDB['Responce']['Data'])==1 :
			wQuery = "update tbl_user_data set " + \
					"apikey = '"    + inUserData['APIkey'] + "', " + \
					"apisecret = '" + inUserData['APIsecret'] + "', " + \
					"acctoken = '"  + inUserData['ACCtoken'] + "', " + \
					"accsecret = '" + inUserData['ACCsecret'] + "', " + \
					"bearer = '" + inUserData['Bearer'] + "', " + \
					"locked = False, " + \
					"lupdate = '" + str(wTD['TimeDate']) + "' " + \
					"where twitterid = '" + inUserData['Account'] + "' ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
			wStr = "データベースのユーザ " + inUserData['Account'] + " を更新しました。" + '\n'
			CLS_OSIF.sPrn( wStr )
		
		else:
			###ありえない
			wStr = "データベースにユーザ " + inUserData['Account'] + " は複数登録されています。" + '\n'
			CLS_OSIF.sPrn( wStr )
			self.OBJ_DB.Close()
			return False
		
		#############################
		# =正常
		wStr = "ユーザデータ " + inUserData['Account'] + " を更新しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 除外ユーザ名
#####################################################
	def GetExeUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeUser"
		
		#############################
		# データベースから除外ユーザ名を取得
		wQuery = "select word from tbl_exc_user " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		gVal.STR_ExeUser = []
		#############################
		# アーカイブの除外ユーザ名を検索
		#   データベースになければ登録する
		# 除外ユーザ名を登録する
		wFLG_newAdd = False
		for wWord in wARR_RateWord :
			gVal.STR_ExeUser.append( wWord )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetExeUser( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetExeUser"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wStr = "PC時間取得失敗" + '\n'
			CLS_OSIF.sPrn( wStr )
			wTD['TimeDate'] = "1901-01-01 00:00:00"
		### wTD['TimeDate']
		
		#############################
		# データベースから除外ユーザ名を取得
		wQuery = "select word from tbl_exc_user " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		gVal.STR_ExeUser = []
		#############################
		# アーカイブの除外ユーザ名を検索
		#   データベースになければ登録する
		# 除外ユーザ名を登録する
		wFLG_newAdd = False
		for wWord in inARRData :
			if wWord in wARR_RateWord :
				###既登録
				gVal.STR_ExeUser.append( wWord )
				continue
			
			wFLG_newAdd = True
			wWord = wWord.replace( "'", "''" )
			wQuery = "insert into tbl_exc_user values (" + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"True," + \
						"'" + wWord + "'" + \
						") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return False
			
			###追加
			gVal.STR_ExeUser.append( wWord )
			CLS_OSIF.sPrn( "除外ユーザ名が追加されました: " + wWord )
		
		#############################
		# =正常
		if wFLG_newAdd==False :
			CLS_OSIF.sPrn( "新規の除外ユーザ名はありませんでした" )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 除外文字
#####################################################
	def GetExeWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeWord"
		
		#############################
		# データベースから除外文字を取得
		wQuery = "select word from tbl_exc_word " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		gVal.STR_ExeWord = []
		#############################
		# アーカイブの除外文字を検索
		#   データベースになければ登録する
		# 除外文字を登録する
		wFLG_newAdd = False
		for wWord in wARR_RateWord :
			gVal.STR_ExeWord.append( wWord )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetExeWord( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetExeWord"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wStr = "PC時間取得失敗" + '\n'
			CLS_OSIF.sPrn( wStr )
			wTD['TimeDate'] = "1901-01-01 00:00:00"
		### wTD['TimeDate']
		
		#############################
		# データベースから除外文字を取得
		wQuery = "select word from tbl_exc_word " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		gVal.STR_ExeWord = []
		#############################
		# アーカイブの除外文字を検索
		#   データベースになければ登録する
		# 除外文字を登録する
		wFLG_newAdd = False
		for wWord in inARRData :
			if wWord in wARR_RateWord :
				###既登録
				gVal.STR_ExeWord.append( wWord )
				continue
			
			wFLG_newAdd = True
			wWord = wWord.replace( "'", "''" )
			wQuery = "insert into tbl_exc_word values (" + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"True," + \
						"'" + wWord + "'" + \
						") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return False
			
			###追加
			gVal.STR_ExeWord.append( wWord )
			CLS_OSIF.sPrn( "除外文字が追加されました: " + wWord )
		
		#############################
		# =正常
		if wFLG_newAdd==False :
			CLS_OSIF.sPrn( "新規の除外文字はありませんでした" )
		
		wRes['Result'] = True
		return wRes



#####################################################
# アクションリツイート
#####################################################
	def GetActionRetweet(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetActionRetweet"
		
		#############################
		# データベースからアクションリツイート文字を取得
		wQuery = "select word from tbl_action_retweet " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateFollow = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateFollow )
		
		gVal.STR_ActionRetweet = []
		#############################
		# アーカイブのアクションリツイート文字を検索
		#   データベースになければ登録する
		# 除外文字を登録する
		wFLG_newAdd = False
		for wWord in wARR_RateFollow :
			gVal.STR_ActionRetweet.append( wWord )
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetActionRetweet( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetActionRetweet"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wStr = "PC時間取得失敗" + '\n'
			CLS_OSIF.sPrn( wStr )
			wTD['TimeDate'] = "1901-01-01 00:00:00"
		### wTD['TimeDate']
		
		#############################
		# データベースからアクションリツイート文字を取得
		wQuery = "select word from tbl_action_retweet " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		### リスト型に整形
		wARR_RateFollow = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateFollow )
		
		gVal.STR_ActionRetweet = []
		#############################
		# アーカイブの除外文字を検索
		#   データベースになければ登録する
		# 除外文字を登録する
		wFLG_newAdd = False
		for wWord in inARRData :
			if wWord in wARR_RateFollow :
				###既登録
				gVal.STR_ActionRetweet.append( wWord )
				continue
			
			wFLG_newAdd = True
			wWord = wWord.replace( "'", "''" )
			wQuery = "insert into tbl_action_retweet values (" + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"True," + \
						"'" + wWord + "'" + \
						") ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return False
			
			###追加
			gVal.STR_ActionRetweet.append( wWord )
			CLS_OSIF.sPrn( "アクションリツイート文字が追加されました: " + wWord )
		
		#############################
		# =正常
		if wFLG_newAdd==False :
			CLS_OSIF.sPrn( "新規のアクションリツイート文字はありませんでした" )
		
		wRes['Result'] = True
		return wRes



#####################################################
# フォロー者候補
#####################################################
	def CheckFollowAgent( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "AddFollowAgent"
		
		wID = str( inID )
		wRes['Responce'] = False
		#############################
		# 重複チェック
		
		### SQLの作成
		wQuery = " id = '" + wID + "' "
		
		### SQLの実行
		wResDB = self.OBJ_DB.RunExist( "tbl_follow_agent", wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		if wResDB['Responce']==True :
			##重複あり
			return wRes
		
		#############################
		# 時間の取得
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
		
		#############################
		# SQLの作成
		wQuery = "insert into tbl_follow_agent values ("
		wQuery = wQuery + "'" + wTimeDate + "', "
		wQuery = wQuery + "'" + str( wID ) + "' "
		wQuery = wQuery + ") ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_ins'] += 1
		
		#############################
		# =正常
		wRes['Responce'] = True	#重複なし
		wRes['Result'] = True
		return wRes

	#####################################################
	def ClearFollowAgent(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ClearFollowAgent"
		
		#############################
		# SQLの作成
		wQuery = "delete tbl_follow_agent "
		wQuery = wQuery + " ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# 自動リツイート
#####################################################
	def CheckAutoRetweet( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CheckAutoRetweet"
		
		wID = str( inID )
		wRes['Responce'] = False
		#############################
		# 重複チェック
		
		### SQLの作成
		wQuery = " id = '" + wID + "' "
		
		### SQLの実行
		wResDB = self.OBJ_DB.RunExist( "tbl_auto_retweet", wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_req'] += 1
		
		if wResDB['Responce']==True :
			##重複あり
			return wRes
		
		#############################
		# 時間の取得
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
		
		#############################
		# SQLの作成
		wQuery = "insert into tbl_auto_retweet values ("
		wQuery = wQuery + "'" + wTimeDate + "', "
		wQuery = wQuery + "'" + str( wID ) + "' "
		wQuery = wQuery + ") ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		gVal.STR_TrafficInfo['db_ins'] += 1
		
		#############################
		# =正常
		wRes['Responce'] = True	#重複なし
		wRes['Result'] = True
		return wRes

	#####################################################
	def ClearAutoRetweet(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ClearAutoRetweet"
		
		#############################
		# SQLの作成
		wQuery = "delete tbl_auto_retweet "
		wQuery = wQuery + " ;"
		
		#############################
		# SQLの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



