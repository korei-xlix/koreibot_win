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
						"'" + str(wTD['TimeDate']) + "'," + \
						"''," + \
						"'" + str(wTD['TimeDate']) + "'," + \
						"''," + \
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
		
		wRes['Result'] = True
		return wRes



#####################################################
# トレンドタグ設定
#####################################################
	def SetTrendTag( self ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetTrendTag"
		
		wTrendTag = None
		#############################
		# Twitterキーの入力
		CLS_OSIF.sPrn( "トレンドタグの設定をおこないます。" )
		CLS_OSIF.sPrn( "---------------------------------------" )
		while True :
			###初期化
			wTrendTag = None
			
			#############################
			# 実行の確認
			wSelect = CLS_OSIF.sInp( "キャンセルしますか？(y)=> " )
			if wSelect=="y" :
				# 完了
				wRes['Result'] = True
				return wRes
			
			#############################
			# 入力
			wStr = "トレンドツイートに設定するトレンドタグを入力してください。"
			CLS_OSIF.sPrn( wStr )
			wKey = CLS_OSIF.sInp( "Trend Tag？=> " )
			if wKey=="" :
				CLS_OSIF.sPrn( "トレンドタグが未入力です" + '\n' )
				continue
			wTrendTag = wKey
			
			###ここまでで入力は完了した
			break
		
		#############################
		# DBに登録する
		if wTrendTag==None :
			##失敗
			wRes['Reason'] = "Trend unset"
			CLS_OSIF.sErr( wRes )
			return False
		else :
			wQuery = "update tbl_user_data set " + \
					"trendtag = '" + wTrendTag + "' " + \
					"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
			
			wResDB = self.OBJ_DB.RunQuery( wQuery )
			wResDB = self.OBJ_DB.GetQueryStat()
			if wResDB['Result']!=True :
				##失敗
				wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
				CLS_OSIF.sErr( wRes )
				return False
			
			#############################
			# トレンドタグの更新
			gVal.STR_UserInfo['TrendTag'] = wTrendTag
			
			wStr = "トレンドを更新しました。" + '\n'
			CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes



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
# リスト通知設定
#####################################################
	def SetListInd( self, inListName ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_DB_IF"
		wRes['Func']  = "SetListInd"
		
		if gVal.STR_UserInfo['ListName']==inListName :
			##失敗
			wRes['Reason'] = "同じリスト名"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		if inListName=="" or inListName==None :
			##失敗
			wRes['Reason'] = "登録不可の文字列: " + inListName
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		wQuery = "update tbl_user_data set " + \
				"listname = '" + inListName + "' " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = self.OBJ_DB.RunQuery( wQuery )
		wResDB = self.OBJ_DB.GetQueryStat()
		if wResDB['Result']!=True :
			##失敗
			wRes['Reason'] = "Run Query is failed(3): RunFunc=" + wResDB['RunFunc'] + " reason=" + wResDB['Reason'] + " query=" + wResDB['Query']
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		gVal.STR_UserInfo['ListName'] = inListName
		
		wStr = "リスト通知設定を更新しました。" + '\n'
		CLS_OSIF.sPrn( wStr )
		
		wRes['Result'] = True
		return wRes

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
		wDefTimeDate = "1901-01-01 00:00:00"
		
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
			gVal.OBJ_L.Log( "C", wRes )
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
			
			#############################
			# DBのいいね情報取得(IDのみ)
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
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			
			#############################
			# 辞書型に整形
			wARR_RateFavoData = {}
			self.OBJ_DB.ChgDict( wResDB['Responce']['Collum'], wResDB['Responce']['Data'], outDict=wARR_RateFavoData )
			wARR_RateFavoData = wARR_RateFavoData[0]
			
			#############################
			# 削除対象か
			wGetLag = CLS_OSIF.sTimeLag( str( wARR_RateFavoData['favo_date'] ), inThreshold=gVal.DEF_STR_TLNUM['favoDataDelSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==False :
				### 規定以内は除外
				continue
			
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
			
			wRes['Reason'] = "Delete FavoData : " + wResDB['Responce']['Data']['screen_name']
			gVal.OBJ_L.Log( "D", wRes )
		
		#############################
		# 正常
		wRes['Result'] = True
		return wRes



