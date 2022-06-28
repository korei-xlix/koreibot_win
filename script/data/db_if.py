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

	DEF_TIMEDATE = "1901-01-01 00:00:00"



#####################################################
# Init
#####################################################
	def __init__(self):
		return



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
# レコード数取得
#####################################################
	def GetRecordNum( self, inTableName=None, inTraffic=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetRecordNum"
		
		#############################
		# 入力チェック
		if inTableName==None or inTableName=="" :
			##失敗
			wRes['Reason'] = "inTableName is invalid: " + str(inTableName)
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# クエリの作成
		wQuery = "select count(*) from " + inTableName + ";"
		
		#############################
		# 実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		
		#############################
		# 実行結果の取得
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# レコード数の取り出し
		try:
			wNum = int( wResDB['Responce']['Data'][0][0] )
		except ValueError:
			##失敗
			wRes['Reason'] = "Data is failer"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トラヒックの計測
		if inTraffic==True :
			gVal.STR_TrafficInfo['db_req'] += 1
		
		#############################
		# 正常
		wRes['Responce'] = wNum
		wRes['Result'] = True
		return wRes



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
		wStr = "botで使うユーザ登録をおこないます。" + '\n'
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
###			wTD['TimeDate'] = "1901-01-01 00:00:00"
###		### wTD['TimeDate']
			wTD['TimeDate'] = self.DEF_TIMEDATE
		
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
						"'" + str(wTD['TimeDate']) + "'," + \
						"''," + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"''," + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"'" + str(wTD['TimeDate']) + "' " + \
						") ;"
###						"''," + \
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
###			wStr = "データベースにユーザ " + inUserData['Account'] + " を登録しました。" + '\n'
###			CLS_OSIF.sPrn( wStr )
			#############################
			# ログ記録
			wRes['Reason'] = "Insert UserData : " + inUserData['Account']
			gVal.OBJ_L.Log( "T", wRes )
		
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
		wQuery = "select * from tbl_exc_word " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
###		#############################
###		# 添え字をIDに差し替える
###		wARR_RateWord = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wARR_ExeWord = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wKey = wARR_DBData[wIndex]['word']
			wCell = {
				"word"		: wKey,
				"report"	: wARR_DBData[wIndex]['report']
			}
			wARR_ExeWord.update({ wKey : wCell })
		
		gVal.ARR_ExeWord = wARR_ExeWord
###		gVal.ARR_ExeWordKey = list( wARR_ExeWord.keys() )
		
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
###			wTD['TimeDate'] = "1901-01-01 00:00:00"
###		### wTD['TimeDate']
			wTD['TimeDate'] = self.DEF_TIMEDATE
		
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
		
		#############################
		# 登録データを作成する
		wARR_Word = {}
		for wLine in inARRData :
			
			### 通報設定ありか
			#      先頭が @@@ の場合
			wReport = False
			wIfind = wLine.find("@@@")
			if wIfind==0 :
				wLine = wLine.replace( "@@@", "" )
				wReport = True
			
			### ダブり登録は除外
			if wLine in wARR_Word :
				continue
			if wLine=="" or wLine==None :
				continue
			
			### データ登録
			wCell = {
				"word"		: wLine,
				"report"	: wReport
			}
			wARR_Word.update({ wLine : wCell })
		
		#############################
		# データベースに登録する
		wKeylist = list( wARR_Word.keys() )
		for wKey in wKeylist :
			#############################
			# 登録済みの場合
			#   通報情報を更新する
			if wKey in wARR_RateWord :
				wQuery = "update tbl_exc_word set " + \
						"report = " + str(wARR_Word[wKey]['report']) + " " + \
						" ;"
			
			#############################
			# 登録なしの場合
			#   新規登録する
			else :
				wQuery = "insert into tbl_exc_word values (" + \
						"'" + str(wTD['TimeDate']) + "', " + \
						"'" + wKey + "', " + \
						str(wARR_Word[wKey]['report']) + " " + \
						") ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
			#############################
			# 実行結果の表示
			if wKey in wARR_RateWord :
				### 更新
				wStr = "除外文字 更新: "
			else:
				### 新規
				wStr = "除外文字 追加: "
			
			### 通報有無
			if wARR_Word[wKey]['report']==True :
				wStr = wStr + " [〇有] "
			else:
				wStr = wStr + " [  無] "
			
			### 文字
			wStr = wStr + wKey
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースから削除
		#   登録データにないデータをデータベースから抹消する
		for wRateKey in wARR_RateWord :
			#############################
			# 登録データにある場合
			#   スキップする
			if wRateKey in wARR_Word :
				continue
			
			# ※登録なし：削除確定
			wQuery = "delete from tbl_exc_word " + \
					"where word = '" + wRateKey + "' " + \
					" ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
			#############################
			# 実行結果の表示
			wStr = "除外文字 ×削除×: " + wRateKey
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# グローバルを更新する
		gVal.ARR_ExeWord = wARR_Word
		gVal.ARR_ExeWordKeys = list( wARR_Word.keys() )
		
		wRes['Result'] = True
		return wRes



#####################################################
# 禁止ユーザ
#####################################################
	def GetExeUser(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetExeUser"
		
		#############################
		# データベースから禁止ユーザを取得
		wQuery = "select * from tbl_exc_user " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_ExeUser = {}
		#############################
		# 禁止ユーザデータを登録する
		wKeylist = list( wARR_DBData.keys() )
		wListNo = 1
		for wIndex in wKeylist :
			wKey = wARR_DBData[wIndex]['screen_name']
			wCell = {
				"list_number"	: wListNo,
				"screen_name"	: wKey,
				"report"		: wARR_DBData[wIndex]['report']
			}
			wARR_ExeUser.update({ wKey : wCell })
			wListNo += 1
		
		gVal.ARR_NotReactionUser = wARR_ExeUser
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def GetExeUserName( self, inListNumber=-1 ):
		wName = None
		if inListNumber==-1 :
			return wName
		
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		for wKey in wKeylist :
			if gVal.ARR_NotReactionUser[wKey]['list_number']==inListNumber :
				wName = gVal.ARR_NotReactionUser[wKey]['screen_name']
				break
		return wName

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
			wTD['TimeDate'] = self.DEF_TIMEDATE
		
		#############################
		# データベースから禁止ユーザを取得
		wQuery = "select screen_name from tbl_exc_user " + \
					";"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		### リスト型に整形
		wARR_RateWord = []
		self.OBJ_DB.ChgList( wResDB['Responce']['Data'], outList=wARR_RateWord )
		
		#############################
		# 登録データを作成する
		wARR_Word = {}
		wListNo = 1
		for wLine in inARRData :
			
			### 通報設定ありか
			#      先頭が @@@ の場合
			wReport = False
			wIfind = wLine.find("@@@")
			if wIfind==0 :
				wLine = wLine.replace( "@@@", "" )
				wReport = True
			
			### ダブり登録は除外
			if wLine in wARR_Word :
				continue
			if wLine=="" or wLine==None :
				continue
			
			### データ登録
			wCell = {
				"list_number"	: wListNo,
				"screen_name"	: wLine,
				"report"		: wReport
			}
			wARR_Word.update({ wLine : wCell })
			wListNo += 1
		
		#############################
		# データベースに登録する
		wKeylist = list( wARR_Word.keys() )
		for wKey in wKeylist :
			#############################
			# 登録済みの場合
			#   通報情報を更新する
			if wKey in wARR_RateWord :
				wQuery = "update tbl_exc_word set " + \
						"report = " + str(wARR_Word[wKey]['report']) + " " + \
						" ;"
			
			#############################
			# 登録なしの場合
			#   新規登録する
			else :
				wQuery = "insert into tbl_exc_user values (" + \
						"'" + str(wTD['TimeDate']) + "', " + \
						"'" + wKey + "', " + \
						str(wARR_Word[wKey]['report']) + " " + \
						") ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return wRes
			
			#############################
			# 実行結果の表示
			if wKey in wARR_RateWord :
				### 更新
				wStr = "禁止ユーザ 更新: "
			else:
				### 新規
				wStr = "禁止ユーザ 追加: "
			
			### 通報有無
			if wARR_Word[wKey]['report']==True :
				wStr = wStr + " [〇有] "
			else:
				wStr = wStr + " [  無] "
			
			### 文字
			wStr = wStr + wKey
			
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースから削除
		#   登録データにないデータをデータベースから抹消する
		for wRateKey in wARR_RateWord :
			#############################
			# 登録データにある場合
			#   スキップする
			if wRateKey in wARR_Word :
				continue
			
			# ※登録なし：削除確定
			wQuery = "delete from tbl_exc_user " + \
					"where screen_name = '" + wRateKey + "' " + \
					" ;"
			
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return wRes
			
			#############################
			# 実行結果の表示
			wStr = "禁止ユーザ ×削除×: " + wRateKey
			CLS_OSIF.sPrn( wStr )
		
		#############################
		# グローバルを更新する
		gVal.ARR_NotReactionUser = wARR_Word
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def InsertExeUser( self, inName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertExeUser"
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wStr = "PC時間取得失敗" + '\n'
			CLS_OSIF.sPrn( wStr )
			wTD['TimeDate'] = self.DEF_TIMEDATE
		
		#############################
		# ダブりチェック
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wListNo = 1
		for wKey in wKeylist :
			### ダブり登録はNG
			if gVal.ARR_NotReactionUser[wKey]['screen_name']==inName :
				wRes['Reason'] = "Duai Screen_Name: name=" + str(inName)
				CLS_OSIF.sErr( wRes )
				return wRes
		
		#############################
		# 新規登録する
		wQuery = "insert into tbl_exc_user values (" + \
				"'" + str(wTD['TimeDate']) + "', " + \
				"'" + str(inName) + "', " + \
				"False " + \
				") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# リスト番号の取得
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wListNo = 1
		for wKey in wKeylist :
			### ダブり登録はスキップ
			if gVal.ARR_NotReactionUser[wKey]['list_number']==wListNo :
				wListNo += 1
				continue
		
		#############################
		# データ登録
		wCell = {
			"list_number"	: wListNo,
			"screen_name"	: str(inName),
			"report"		: False
		}
		gVal.ARR_NotReactionUser.update({ str(inName) : wCell })
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateExeUser( self, inName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateExeUser"
		
		#############################
		# ダブりチェック
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wFLG_Detect = False
		for wKey in wKeylist :
			### データあり
			if gVal.ARR_NotReactionUser[wKey]['screen_name']==inName :
				wFLG_Detect = True
				break
		if wFLG_Detect!=True :
			wRes['Reason'] = "No data Screen_Name: name=" + str(inName)
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 設定の自動切換え
		wReport = False
		if gVal.ARR_NotReactionUser[inName]['report']==False :
			wReport = True
		
		#############################
		# 変更する
		wQuery = "update tbl_exc_user set " + \
				"report = " + str( wReport ) + " " + \
				"where screen_name = '" + inName + "' " + \
				";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# データ変更
		gVal.ARR_NotReactionUser[inName]['report'] = wReport
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteExeUser( self, inName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteExeUser"
		
		#############################
		# ダブりチェック
		wKeylist = list( gVal.ARR_NotReactionUser.keys() )
		wFLG_Detect = False
		for wKey in wKeylist :
			### データあり
			if gVal.ARR_NotReactionUser[wKey]['screen_name']==inName :
				wFLG_Detect = True
				break
		if wFLG_Detect!=True :
			wRes['Reason'] = "No data Screen_Name: name=" + str(inName)
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# 変更する
		wQuery = "delete from tbl_exc_user where " + \
					"screen_name = '" + inName + "' " + \
					";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# データ削除
		del gVal.ARR_NotReactionUser[inName]
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね指定
#####################################################
###	def GetOtherListFavo(self):
	def GetListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "GetOtherListFavo"
		wRes['Func']  = "GetListFavo"
		
		#############################
		# データベースを取得
		wQuery = "select * from tbl_list_favo " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_Data = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wScreenName = wARR_DBData[wIndex]['screen_name']
			
			wCell = {
###				"screen_name"	: wARR_DBData[wIndex]['screen_name'],
				"screen_name"	: wScreenName,
				"list_name"		: wARR_DBData[wIndex]['list_name'],
###				"list_id"		: wARR_DBData[wIndex]['list_id'],
				"valid"			: wARR_DBData[wIndex]['valid'],
				"follow"		: wARR_DBData[wIndex]['follow'],
				"caution"		: wARR_DBData[wIndex]['caution'],
				"sensitive"		: wARR_DBData[wIndex]['sensitive'],
				"auto_rem"		: wARR_DBData[wIndex]['auto_rem'],
				"update"		: False
			}
			wARR_Data.update({ wIndex : wCell })
		
		gVal.ARR_ListFavo = wARR_Data
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
###	def SetOtherListFavo( self, inARRData ):
	def SetListFavo( self, inARRData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "SetOtherListFavo"
		wRes['Func']  = "SetListFavo"
		
		#############################
		# 登録データを作成する
		wARR_Data = {}
		wIndex = 0
		for wLine in inARRData :
			
			### コメントアウトはスキップ
			wIfind = wLine.find("#")
			if wIfind==0 :
				continue
			
			wARR_Line = wLine.split(",")
			### 要素数が少ないのは除外
###			if len(wARR_Line)!=4 :
###			if len(wARR_Line)!=5 :
			if len(wARR_Line)!=6 :
				continue
			
			### データ登録
###			wFLG_Follow = True if wARR_Line[0]=="***" else False
			### フォロー/フォロワー含むか
			wARR_Line[0] = True if wARR_Line[0]=="***" else False
			### 警告
			wARR_Line[1] = True if wARR_Line[1]=="***" else False
			### センシティブツ
			wARR_Line[2] = True if wARR_Line[2]=="***" else False
			### 自動リムーブ
			wARR_Line[3] = True if wARR_Line[3]=="***" else False
			
			wCell = {
###				"screen_name"	: wARR_Line[0],
###				"id"			: wARR_Line[1],
###				"list_name"		: wARR_Line[2],
###				"list_id"		: wARR_Line[3],
###				"screen_name"	: wARR_Line[1],
###				"id"			: wARR_Line[2],
###				"list_name"		: wARR_Line[3],
###				"list_id"		: wARR_Line[4],
				"screen_name"	: wARR_Line[4],
###				"id"			: wARR_Line[5],
				"list_name"		: wARR_Line[5],
###				"list_id"		: wARR_Line[7],
				"valid"			: True,
###				"follow"		: wFLG_Follow,
###				"caution"		: False,
###				"sensitive"		: False,
				"follow"		: wARR_Line[0],
				"caution"		: wARR_Line[1],
				"sensitive"		: wARR_Line[2],
				"auto_rem"		: wARR_Line[3],
				"update"		: False
			}
			
			wARR_Data.update({ wIndex : wCell })
			wIndex += 1
		
		if len(wARR_Data)==0 :
			##失敗
			wRes['Reason'] = "get no data"
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# レコードを一旦全消す
		wQuery = "delete from tbl_list_favo " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return False
		
		wStr = "tbl_list_favo をクリアしました "
		CLS_OSIF.sPrn( wStr )
		
		#############################
		# データベースに登録する
		wKeylist = list( wARR_Data.keys() )
		for wKey in wKeylist :
			wQuery = "insert into tbl_list_favo values (" + \
					"'" + gVal.STR_UserInfo['Account'] + "', " + \
					"'" + str(wARR_Data[wKey]['screen_name']) + "', " + \
					"'" + str(wARR_Data[wKey]['list_name']) + "', " + \
					"True, " + \
					str(wARR_Data[wKey]['follow']) + ", " + \
					str(wARR_Data[wKey]['caution']) + ", " + \
					str(wARR_Data[wKey]['sensitive']) + ", " + \
					str(wARR_Data[wKey]['auto_rem']) + " " + \
					") ;"
			
###					"'" + str(wARR_Data[wKey]['id']) + "', " + \
###					"'" + str(wARR_Data[wKey]['list_id']) + "', " + \
###
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return wRes
		
		#############################
		# グローバルを更新する
		gVal.ARR_ListFavo = wARR_Data
		
		wRes['Result'] = True
		return wRes

	#####################################################
###	def SaveOtherListFavo(self):
	def SaveListFavo(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "SaveOtherListFavo"
		wRes['Func']  = "SaveListFavo"
		
		wUpdate = False
		#############################
		# 更新があれば
		#   データベースを更新する
		wKeylist = list( gVal.ARR_ListFavo.keys() )
		for wKey in wKeylist :
			if gVal.ARR_ListFavo[wKey]['update']==False :
				### 更新なしはスキップ
				continue
			
			wQuery = "update tbl_list_favo set " + \
					"valid = " + str(gVal.ARR_ListFavo[wKey]['valid']) + ", " + \
					"follow = " + str(gVal.ARR_ListFavo[wKey]['follow']) + ", " + \
					"caution = " + str(gVal.ARR_ListFavo[wKey]['caution']) + ", " + \
					"sensitive = " + str(gVal.ARR_ListFavo[wKey]['sensitive']) + ", " + \
					"auto_rem = " + str(gVal.ARR_ListFavo[wKey]['auto_rem']) + " " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"screen_name = '" + gVal.ARR_ListFavo[wKey]['screen_name'] + "' and " + \
					"list_name = '" + gVal.ARR_ListFavo[wKey]['list_name'] + "' " + \
					";"
			
###					"id = '" + gVal.ARR_ListFavo[wKey]['id'] + "' and " + \
###					"list_id = '" + gVal.ARR_ListFavo[wKey]['list_id'] + "' " + \
			#############################
			# クエリの実行
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return wRes
			
			wUpdate = True
		
		if wUpdate==True :
			CLS_OSIF.sPrn( "リストいいねの設定を更新しました。" )
		
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
###	def SetTrendTag( self ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "SetTrendTag"
###		
###		wTrendTag = None
###		#############################
###		# Twitterキーの入力
###		CLS_OSIF.sPrn( "トレンドタグの設定をおこないます。" )
###		CLS_OSIF.sPrn( "---------------------------------------" )
###		while True :
###			###初期化
###			wTrendTag = None
###			
###			#############################
###			# 実行の確認
###			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
###			if wSelect=="y" :
###				# 完了
###				wRes['Result'] = True
###				return wRes
###			
###			#############################
###			# 入力
###			wStr = "トレンドツイートに設定するトレンドタグを入力してください。"
###			CLS_OSIF.sPrn( wStr )
###			wKey = CLS_OSIF.sInp( "Trend Tag？=> " )
###			if wKey=="" :
###				CLS_OSIF.sPrn( "トレンドタグが未入力です" + '\n' )
###				continue
###			wTrendTag = wKey
###			
###			###ここまでで入力は完了した
###			break
###		
###		#############################
###		# DBに登録する
###		if wTrendTag==None :
###			##失敗
###			wRes['Reason'] = "Trend unset"
###			CLS_OSIF.sErr( wRes )
###			return False
###		else :
###			wQuery = "update tbl_user_data set " + \
###					"trendtag = '" + wTrendTag + "' " + \
###					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###			
###			wResDB = self.OBJ_DB.RunQuery( wQuery )
###			wResDB = self.OBJ_DB.GetQueryStat()
###			if wResDB['Result']!=True :
###				##失敗
###				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
###				CLS_OSIF.sErr( wRes )
###				return False
###			
###			#############################
###			# トレンドタグの更新
###			gVal.STR_UserInfo['TrendTag'] = wTrendTag
###			
###			wStr = "トレンドを更新しました。" + '\n'
###			CLS_OSIF.sPrn( wStr )
###		
###		wRes['Result'] = True
###		return wRes
###
###

#####################################################
# いいね者送信日時 更新
#####################################################
	def UpdateFavoDate( self, inDate ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoDate"
		
		#############################
		# DBに登録する
		wQuery = "update tbl_user_data set " + \
				"favodate = '" + str(inDate) + "' " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return False
		
		#############################
		# いいね者送信日時(直近)の更新
		gVal.STR_UserInfo['FavoDate'] = inDate
		
		wStr = "いいね者送信日時(直近)を更新しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リスト名設定
#####################################################
	def SetListName(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetListName"
		
		wQuery = "update tbl_user_data set " + \
				"trendtag = '" + gVal.STR_UserInfo['TrendTag'] + "', " + \
				"listname = '" + gVal.STR_UserInfo['ListName'] + "', " + \
				"arlistname = '" + gVal.STR_UserInfo['ArListName'] + "' " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

#####################################################
# リスト通知設定
#####################################################
###	def SetListInd( self, inListName ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "SetListInd"
###		
###		if gVal.STR_UserInfo['ListName']==inListName :
###			##失敗
###			wRes['Reason'] = "同じリスト名"
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		if inListName=="" or inListName==None :
###			##失敗
###			wRes['Reason'] = "登録不可の文字列: " + inListName
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		wQuery = "update tbl_user_data set " + \
###				"listname = '" + inListName + "' " + \
###				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###		
###		wResDB = self.OBJ_DB.RunQuery( wQuery )
###		wResDB = self.OBJ_DB.GetQueryStat()
###		if wResDB['Result']!=True :
###			##失敗
###			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		gVal.STR_UserInfo['ListName'] = inListName
###		
###		wStr = "リスト通知設定を更新しました。" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		wRes['Result'] = True
###		return wRes

#####################################################
# リスト通知日時更新
#####################################################
	def UpdateListIndDate(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateListInd"
		
		wRes['Responce'] = False
		
		wQuery = "update tbl_user_data set " + \
				"listdate = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 日付を跨いだか
		wNowDate = str(gVal.STR_SystemInfo['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(gVal.STR_UserInfo['ListDate'])
		wRateDate = wRateDate.split(" ")
		wRateDate = wRateDate[0]
		if wNowDate!=wRateDate :
			### 翌日
			wRes['Responce'] = True
		gVal.STR_UserInfo['ListDate'] = str(gVal.STR_SystemInfo['TimeDate'])
		
		wStr = "リスト通知日時を更新しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# リストいいね設定
#####################################################
###	def SetListFavo( self, inListName ):
###		#############################
###		# 応答形式の取得
###		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
###		wRes = CLS_OSIF.sGet_Resp()
###		wRes['Class'] = "CLS_DB_IF"
###		wRes['Func']  = "SetListFavo"
###		
###		if gVal.STR_UserInfo['LFavoName']==inListName :
###			##失敗
###			wRes['Reason'] = "同じリスト名"
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		if inListName=="" or inListName==None :
###			##失敗
###			wRes['Reason'] = "登録不可の文字列: " + inListName
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		wQuery = "update tbl_user_data set " + \
###				"lfavoname = '" + inListName + "' " + \
###				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###		
###		wResDB = self.OBJ_DB.RunQuery( wQuery )
###		wResDB = self.OBJ_DB.GetQueryStat()
###		if wResDB['Result']!=True :
###			##失敗
###			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		gVal.STR_UserInfo['LFavoName'] = inListName
###		
###		wStr = "リストいいね設定を更新しました。" + '\n'
###		CLS_OSIF.sPrn( wStr )
###		
###		wRes['Result'] = True
###		return wRes

#####################################################
# リストいいね 日時更新
#####################################################
	def UpdateListFavoDate(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateListFavoDate"
		
		wRes['Responce'] = False
		
		wQuery = "update tbl_user_data set " + \
				"lfavdate = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 日付を跨いだか
		wNowDate = str(gVal.STR_SystemInfo['TimeDate'])
		wNowDate = wNowDate.split(" ")
		wNowDate = wNowDate[0]
		wRateDate = str(gVal.STR_UserInfo['LFavoDate'])
		wRateDate = wRateDate.split(" ")
		wRateDate = wRateDate[0]
		if wNowDate!=wRateDate :
			### 翌日
			wRes['Responce'] = True
		gVal.STR_UserInfo['LFavoDate'] = str(gVal.STR_SystemInfo['TimeDate'])
		
		wStr = "リストいいね日時を更新しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



#####################################################
# いいね情報
#####################################################
	def InsertFavoData( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "InsertFavoData"
		
		#############################
		# ユーザ情報の加工
		wID = str(inUser['id'])
		wScreenName = inUser['screen_name']
		
		#############################
		# 時間の取得
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
###		wDefTimeDate = "1901-01-01 00:00:00"
		wDefTimeDate = self.DEF_TIMEDATE
		
		#############################
		# SQLの作成
		wQuery = "insert into tbl_favouser_data values ("
		wQuery = wQuery + "'" + gVal.STR_UserInfo['Account'] + "', "
		wQuery = wQuery + "'" + wTimeDate + "', "
		
		wQuery = wQuery + "'" + wID + "', "
		wQuery = wQuery + "'" + wScreenName + "', "
		
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "0, "
		wQuery = wQuery + "'(none)', "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "'(none)', "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "'" + wDefTimeDate + "', "
		wQuery = wQuery + "False, "
		wQuery = wQuery + "'" + wDefTimeDate + "' "
		
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
		# ログ記録
		wRes['Reason'] = "Insert FavoData : " + wScreenName
		gVal.OBJ_L.Log( "T", wRes )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def GetFavoDataOne( self, inID ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetFavoDataOne"
		
		wRes['Responce'] = None
		#############################
		# DBのいいね情報取得
		wQuery = "select * from tbl_favouser_data where " + \
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
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_RateFavoData = {}
		self.OBJ_DB.ChgDict( wResDB['Responce']['Collum'], wResDB['Responce']['Data'], outDict=wARR_RateFavoData )
		
		wRes['Responce'] = wARR_RateFavoData[0]
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateFavoData( self, inUser, inData, inFavoData, inCountUp=True ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoData"
		
		wID = inUser['id']
		wScreenName = inUser['screen_name']
		
		wFavoID   = str( inData['id'] )
###		wFavoDate = str( inData['created_at'] )
		wFavoDate = str( gVal.STR_SystemInfo['TimeDate'] )
		if inCountUp==True :
			wCnt    = inFavoData['favo_cnt'] + 1
			wNowCnt = inFavoData['now_favo_cnt'] + 1
			wSended = False
		else:
			wCnt    = inFavoData['favo_cnt']
			wNowCnt = inFavoData['now_favo_cnt']
			wSended = True
		
		#############################
		# 更新
		wQuery = "update tbl_favouser_data set " + \
					"sended = " + str(wSended) + ", " + \
					"screen_name = '" + wScreenName + "', " + \
					"favo_cnt = " + str( wCnt ) + ", " + \
					"now_favo_cnt = " + str( wNowCnt ) + ", " + \
					"favo_id = '" + wFavoID + "', " + \
					"favo_date = '" + wFavoDate + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateListFavoData( self, inUser, inFavoID, inFavoData ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateListFavoData"
		
		wID = inUser['id']
		wScreenName = inUser['screen_name']
		
		wFavoID   = str( inFavoID )
		wFavoDate = str( inFavoData )
		
		wRes['Responce'] = False
		#############################
		# 1個取り出す
		wResDBData = gVal.OBJ_DB_IF.GetFavoDataOne( wID )
		if wResDBData['Result']!=True :
			###失敗
			wRes['Reason'] = "GetFavoDataOne is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### DB登録なし
		if wResDBData['Responce']==None :
			### 正常
			wRes['Result'] = True
			return wRes
		
		#############################
		# 更新
		if wResDBData['Responce']['lfavo_id']==wFavoID :
			### いいねIDが同じなら、更新しない
			wRes['Result'] = True
			return wRes
		
		#############################
		# 更新
		wQuery = "update tbl_favouser_data set " + \
					"screen_name = '" + wScreenName + "', " + \
					"lfavo_id = '" + wFavoID + "', " + \
					"lfavo_date = '" + wFavoDate + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Responce'] = True
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateListIndData( self, inUser ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateListIndData"
		
		wID = inUser['id']
		#############################
		# 更新
		wQuery = "update tbl_favouser_data set " + \
					"list_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(wID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SendedFavoData( self, inID, inCnt=-1 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SendedFavoData"
		
		#############################
		# 更新
		if inCnt>=0 :
			wCnt = inCnt + 1
			wQuery = "update tbl_favouser_data set " + \
						"senddate = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', " + \
						"sended = True, " + \
						"send_cnt = " + str( wCnt ) + ", " + \
						"now_favo_cnt = 0 " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(inID) + "' ;"
		else:
			wQuery = "update tbl_favouser_data set " + \
						"sended = True, " + \
						"now_favo_cnt = 0 " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
###	def UpdateFavoDataFollower( self, inID, inFLG_MyFollow=None, inFLG_Follower=None ):
	def UpdateFavoDataFollower( self, inID, inFLG_MyFollow=None, inFLG_Follower=None, inFLG_FavoUpdate=False ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateFavoDataFollower"
		
		#############################
		# 入力チェック
		if inFLG_MyFollow==None and inFLG_Follower==None :
			wRes['Reason'] = "set input is both None"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if inFLG_Follower==None and (inFLG_MyFollow!=True and inFLG_MyFollow!=False) :
			wRes['Reason'] = "set inFLG_MyFollow is not bool"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if inFLG_MyFollow==None and (inFLG_Follower!=True and inFLG_Follower!=False) :
			wRes['Reason'] = "set inFLG_Follower is not bool"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 更新
		
		#############################
		# フォロー者、フォロワーとも更新
		if inFLG_MyFollow!=None and inFLG_Follower!=None :
###			wQuery = "update tbl_favouser_data set " + \
###					"myfollow = " + str(inFLG_MyFollow) + ", " + \
###					"myfollow_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "', " + \
###					"follower = " + str(inFLG_MyFollow) + ", " + \
###					"follower_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
###					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					" and id = '" + str(inID) + "' ;"
			wQuery = "update tbl_favouser_data set "
			if inFLG_FavoUpdate==True :
				wQuery = wQuery + "favo_date = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', "
			wQuery = wQuery + "myfollow = " + str(inFLG_MyFollow) + ", " + \
					"myfollow_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "', " + \
					"follower = " + str(inFLG_MyFollow) + ", " + \
					"follower_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロー者のみ更新
		elif inFLG_MyFollow!=None :
###			wQuery = "update tbl_favouser_data set " + \
###					"myfollow = " + str(inFLG_MyFollow) + ", " + \
###					"myfollow_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
###					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					" and id = '" + str(inID) + "' ;"
			wQuery = "update tbl_favouser_data set "
			if inFLG_FavoUpdate==True :
				wQuery = wQuery + "favo_date = '" + str( gVal.STR_SystemInfo['TimeDate'] ) + "', "
			wQuery = wQuery + "myfollow = " + str(inFLG_MyFollow) + ", " + \
					"myfollow_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inID) + "' ;"
		
		#############################
		# フォロワーのみ更新
		else :
			wQuery = "update tbl_favouser_data set " + \
					"follower = " + str(inFLG_Follower) + ", " + \
					"follower_date = '" + str(gVal.STR_SystemInfo['TimeDate']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					" and id = '" + str(inID) + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteFavoData(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteFavoData"
		
		#############################
		# DBのいいね情報取得(IDのみ)
		wQuery = "select id from tbl_favouser_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' " + \
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
		wARR_DBDataID = gVal.OBJ_DB_IF.ChgList( wResDB['Responce'] )
		
		for wID in wARR_DBDataID :
			wID = str(wID)
			
###			#############################
###			# リストいいねユーザは除外
###			if gVal.OBJ_Tw_IF.CheckFavoUserData( wID )==True :
###				continue
###			
			#############################
			# DBのいいね情報取得
			wQuery = "select * from tbl_favouser_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"id = '" + wID + "' " + \
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
				gVal.OBJ_L.Log( "D", wRes )
				return wRes
			
			#############################
			# 辞書型に整形
			wARR_RateFavoData = {}
			self.OBJ_DB.ChgDict( wResDB['Responce']['Collum'], wResDB['Responce']['Data'], outDict=wARR_RateFavoData )
			wARR_RateFavoData = wARR_RateFavoData[0]	#1個しかないので添え字を消す
			
			#############################
			# 削除対象か
			#   いいね日時とリストいいね日時が初期値の場合
			#     登録日が期間を過ぎてたら削除
			#   いいね日時 もしくは リストいいね日時 が初期値でない場合
			#     いいね日時が期間を過ぎてたら削除
			if str( wARR_RateFavoData['favo_date'] )==self.DEF_TIMEDATE and \
			   str( wARR_RateFavoData['lfavo_date'] )==self.DEF_TIMEDATE :
				wCHR_DelTimeDate = str( wARR_RateFavoData['regdate'] )
			else:
###				wCHR_DelTimeDate = str( wARR_RateFavoData['favo_date'] )
				if str( wARR_RateFavoData['favo_date'] )!=self.DEF_TIMEDATE :
					wCHR_DelTimeDate = str( wARR_RateFavoData['favo_date'] )
				else:
					wCHR_DelTimeDate = str( wARR_RateFavoData['lfavo_date'] )
			
###			wGetLag = CLS_OSIF.sTimeLag( str( wARR_RateFavoData['favo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['favoDataDelSec'] )
			wGetLag = CLS_OSIF.sTimeLag( wCHR_DelTimeDate, inThreshold=gVal.DEF_STR_TLNUM['favoDataDelSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				continue
			
###			wScreenName = str( wARR_RateFavoData[0]['screen_name'] )
			#############################
			# DBから削除
			wQuery = "delete from tbl_favouser_data where " + \
						"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
						"id = '" + wID + "' " + \
						";"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed: RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			gVal.STR_TrafficInfo['db_del'] += 1
			
###			wRes['Reason'] = "Delete FavoData : " + str( wResDB['Responce']['Data']['screen_name'] )
###			wRes['Reason'] = "Delete FavoData : " + wScreenName
###			wRes['Reason'] = "Delete FavoData : " + str( wARR_RateFavoData['screen_name'] )
###			gVal.OBJ_L.Log( "T", wRes )
			wTextReason = "Delete FavoData : " + str( wARR_RateFavoData['screen_name'] )
			gVal.OBJ_L.Log( "T", wRes, wTextReason )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



#####################################################
# 検索ワード
#####################################################
	def GetSearchWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "GetSearchWord"
		
		#############################
		# データベースを取得
		wQuery = "select * from tbl_search_word " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(1): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return False
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		wARR_Data = {}
		#############################
		# 除外文字データを登録する
		wKeylist = list( wARR_DBData.keys() )
		for wIndex in wKeylist :
			wCell = {
				"regdate"		: str(wARR_DBData[wIndex]['regdate']),
				"id"			: str(wARR_DBData[wIndex]['id']),
				"word"			: str(wARR_DBData[wIndex]['word']),
				"hit_cnt"		: wARR_DBData[wIndex]['hit_cnt'],
				"favo_cnt"		: wARR_DBData[wIndex]['favo_cnt'],
				"update_date"	: str(wARR_DBData[wIndex]['update_date']),
				"valid"			: wARR_DBData[wIndex]['valid'],
				"sensitive"		: wARR_DBData[wIndex]['sensitive']
			}
			wARR_Data.update({ str(wARR_DBData[wIndex]['id']) : wCell })
		
		#############################
		# グローバルに反映
		gVal.ARR_SearchData = wARR_Data
		
		#############################
		# =正常
		wRes['Result'] = True
		return wRes

	#####################################################
	def SetSearchWord( self, inWord ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetSearchWord"
		
		#############################
		# 入力チェック
		wWord = inWord.replace( "'", "''" )
		
		wFlg_Detect = False
		wKeylist = list( gVal.ARR_SearchData.keys() )
		for wIndex in wKeylist :
			if gVal.ARR_SearchData[wIndex]['word']==wWord :
				wFlg_Detect = True
				break
		if wFlg_Detect==True :
			##失敗
			wRes['Reason'] = "Dual word input: word=" + wWord
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 登録データを作成する
		wTimeDate = str( gVal.STR_SystemInfo['TimeDate'] )
		wIndex = len( gVal.ARR_SearchData ) + 1
		
		wCell = {
			"regdate"		: wTimeDate,
			"id"			: str(wIndex),
			"word"			: wWord,
			"hit_cnt"		: 0,
			"favo_cnt"		: 0,
			"update_date"	: wTimeDate,
			"valid"			: True,
			"sensitive"		: False
		}
		
		#############################
		# データベースに登録する
		wQuery = "insert into tbl_search_word values (" + \
				"'" + gVal.STR_UserInfo['Account'] + "', " + \
				"'" + str( wCell['regdate'] ) + "', " + \
				"'" + str( wCell['id'] ) + "', " + \
				"'" + str( wCell['word'] ) + "', " + \
				str( wCell['hit_cnt'] ) + ", " + \
				str( wCell['favo_cnt'] ) + ", " + \
				"'" + str( wCell['update_date'] ) + "', " + \
				str( wCell['valid'] ) + ", " + \
				str( wCell['sensitive'] ) + " " + \
				") ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# グローバルを更新する
		gVal.ARR_SearchData.update({ str(wIndex) : wCell })
		
		#############################
		# ログ記録
		wRes['Reason'] = "Insert SearchWord : index=" + str(wIndex) + " word=" + str( wCell['word'] )
		gVal.OBJ_L.Log( "T", wRes )
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def ValidSearchWord( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ValidSearchWord"
		
		#############################
		# インデックスチェック
		wIndex = str(inIndex)
		if wIndex not in gVal.ARR_SearchData :
			wRes['Reason'] = "Index is not found: index=" + inIndex
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 有効/無効の切り替え
		if gVal.ARR_SearchData[wIndex]['valid']==True :
			gVal.ARR_SearchData[wIndex]['valid'] = False
		else:
			gVal.ARR_SearchData[wIndex]['valid'] = True
		
		#############################
		# データベースを更新する
		wQuery = "update tbl_search_word set " + \
					"valid = " + str(gVal.ARR_SearchData[wIndex]['valid']) + " " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"id = '" + wIndex + "' " + \
					";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def SensitiveSearchWord( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SensitiveSearchWord"
		
		#############################
		# インデックスチェック
		wIndex = str(inIndex)
		if wIndex not in gVal.ARR_SearchData :
			wRes['Reason'] = "Index is not found: index=" + inIndex
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# センシティブ設定の切り替え
		if gVal.ARR_SearchData[wIndex]['sensitive']==True :
			gVal.ARR_SearchData[wIndex]['sensitive'] = False
		else:
			gVal.ARR_SearchData[wIndex]['sensitive'] = True
		
		#############################
		# データベースを更新する
		wQuery = "update tbl_search_word set " + \
					"sensitive = " + str(gVal.ARR_SearchData[wIndex]['sensitive']) + " " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"id = '" + wIndex + "' " + \
					";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def UpdateSearchWord( self, inIndex, inWord=None ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "UpdateSearchWord"
		
		#############################
		# インデックスチェック
		wIndex = str(inIndex)
		if wIndex not in gVal.ARR_SearchData :
			wRes['Reason'] = "Index is not found: index=" + inIndex
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 検索ワードの設定
		gVal.ARR_SearchData[wIndex]['word'] = inWord
		
		#############################
		# データベースを更新する
		wQuery = "update tbl_search_word set " + \
					"word = '" + str(gVal.ARR_SearchData[wIndex]['word']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"id = '" + wIndex + "' " + \
					";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def CountSearchWord( self, inIndex, inHitCnt=1, inFavoCnt=1 ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "CountSearchWord"
		
		#############################
		# インデックスチェック
		wIndex = str(inIndex)
		if wIndex not in gVal.ARR_SearchData :
			wRes['Reason'] = "Index is not found: index=" + inIndex
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 時間の取得
		gVal.ARR_SearchData[wIndex]['update_date'] = str( gVal.STR_SystemInfo['TimeDate'] )
		
		#############################
		# カウンタ進行
		gVal.ARR_SearchData[wIndex]['hit_cnt'] += inHitCnt
		gVal.ARR_SearchData[wIndex]['favo_cnt'] += inFavoCnt
		
		#############################
		# データベースを更新する
		wQuery = "update tbl_search_word set " + \
					"hit_cnt = " + str(gVal.ARR_SearchData[wIndex]['hit_cnt']) + ", " + \
					"favo_cnt = " + str(gVal.ARR_SearchData[wIndex]['favo_cnt']) + ", " + \
					"update_date = '" + str(gVal.ARR_SearchData[wIndex]['update_date']) + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"id = '" + wIndex + "' " + \
					";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def ClearSearchWord(self):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "ClearSearchWord"
		
		#############################
		# カウンタを0クリア
		wQuery = "update tbl_search_word set " + \
				"hit_cnt = 0, " + \
				"favo_cnt = 0 " + \
				"where twitterid = '" + inUserData['Account'] + "' ;"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		wRes['Result'] = True
		return wRes

	#####################################################
	def DeleteSearchWord( self, inIndex ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "DeleteSearchWord"
		
		#############################
		# インデックスチェック
		wIndex = str(inIndex)
		if wIndex not in gVal.ARR_SearchData :
			wRes['Reason'] = "Index is not found: index=" + inIndex
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# データベースから削除
		wQuery = "delete from tbl_search_word " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
				"id = '" + wIndex + "' " + \
				";"
		
		#############################
		# クエリの実行
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(2): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			CLS_OSIF.sErr( wRes )
			return wRes
		
		#############################
		# データ削除
		wWord = gVal.ARR_SearchData[wIndex]['word']
		del gVal.ARR_SearchData[inIndex]
		
		#############################
		# ログ記録
		wRes['Reason'] = "Delete SearchWord : index=" + str(wIndex) + " word=" + str( wWord )
		gVal.OBJ_L.Log( "T", wRes )
		
		wRes['Result'] = True
		return wRes



