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
						"'' " + \
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



