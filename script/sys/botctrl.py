#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : bot制御(共通)
#####################################################
from mylog import CLS_Mylog

from db_if import CLS_DB_IF
from twitter_if import CLS_Twitter_IF
from osif import CLS_OSIF
from filectrl import CLS_File
from gval import gVal
#####################################################
class CLS_BotCtrl():
#####################################################

#####################################################
# Botテスト
#####################################################
	@classmethod
	def sBotTest(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sBotTest"
		
		#############################
		# 引数取得
		wArg = CLS_OSIF.sGetArg()
		if len(wArg)==4 :	#テストモード : bottest か
			if wArg[3]==gVal.DEF_TEST_MODE :
				gVal.FLG_Test_Mode = True
		
		elif len(wArg)==2 :	#モード
			###セットアップモード
			###全初期化モード
			###データクリアモード
			if wArg[1]!="setup" and \
			   wArg[1]!="init" and \
			   wArg[1]!="clear" :
				wRes['Reason'] = "存在しないモードです"
				CLS_OSIF.sErr( wRes )
				return False
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			return True
		
		elif len(wArg)!=3 :	#引数が足りない
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません= " + str( wArg )
			CLS_OSIF.sErr( wRes )
			return False
		
		gVal.STR_UserInfo['Account'] = wArg[1]	#ユーザ名
		wPassword                    = wArg[2]	#パスワード
		gVal.STR_SystemInfo['RunMode'] = "Normal"
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
		wSubRes = gVal.OBJ_DB_IF.Connect( inPassWD=wPassword )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "DB接続失敗: reason=" + wResDB['Reason']
			CLS_OSIF.sErr( wRes )
			return False
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			wRes['Reason'] = "DB未構築"
			CLS_OSIF.sErr( wRes )
			gVal.OBJ_DB_IF.Close()
			return False
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
		#############################
		# テーブルがある
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ登録の確認
		if len(wResDB['Responce']['Data'])==0 :
			wRes['Reason'] = "ユーザが登録されていません =" + gVal.STR_UserInfo['Account']
			gVal.OBJ_L.Log( "D", wRes )
			gVal.OBJ_DB_IF.Close()
			return False
		
		#############################
		# 辞書型に整形
		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ユーザ登録の抽出
		wAPIkey    = wChgDict[0]['apikey']
		wAPIsecret = wChgDict[0]['apisecret']
		wACCtoken  = wChgDict[0]['acctoken']
		wACCsecret = wChgDict[0]['accsecret']
		wBearer    = wChgDict[0]['bearer']
		
		#############################
		# 前回ロック時間の取得(=前回bot実行時間)
		gVal.STR_SystemInfo['RateLockTD'] = wChgDict[0]['lupdate']
		
		#############################
		# 排他開始
		wLock = cls.sLock()
		if wLock['Result']!=True :
			wRes['Reason'] = "排他取得失敗: " + wLock['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			gVal.OBJ_DB_IF.Close()
			return
		elif wLock['Responce']!=None :
			wRes['Reason'] = "排他中"
			gVal.OBJ_L.Log( "R", wRes )
			
			CLS_OSIF.sPrn( "処理待機中です。CTRL+Cで中止することもできます。" )
			CLS_OSIF.sPrn( wLock['Reason'] + '\n' )
			
			wResStop = CLS_OSIF.sPrnWAIT( wLock['Responce'] )
			if wResStop==False :
				###ウェイト中止
				CLS_OSIF.sPrn( '\n' + "待機を中止しました。プログラムを停止しました。" )
				gVal.OBJ_DB_IF.Close()
				return
		
		#############################
		# Twitterに接続
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
		wTwitterRes = gVal.OBJ_Tw_IF.Connect( wAPIkey, wAPIsecret, wACCtoken, wACCsecret, wBearer )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wResTwitter['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			cls.sBotEnd()	#bot終了
			return False
		
		#############################
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間取得失敗"
			gVal.OBJ_L.Log( "B", wRes )
			cls.sBotEnd()	#bot終了
			return
		### wTD['TimeDate']
		gVal.STR_SystemInfo['APIrect'] = str(wTD['TimeDate'])
		
		#############################
		# Version情報
		wReadme = []
		if CLS_File.sReadFile( gVal.DEF_STR_FILE['Readme'], outLine=wReadme )!=True :
			wRes['Reason'] = "Readme.mdファイルが見つかりません: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
			return False
		
		if len(wReadme)<=1 :
			wRes['Reason'] = "Readme.mdファイルが空です: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
			return False
		
		for wLine in wReadme :
			#############################
			# 分解+要素数の確認
			wLine = wLine.strip()
			wGetLine = wLine.split("= ")
			if len(wGetLine) != 2 :
				continue
			
			wGetLine[0] = wGetLine[0].replace("::", "")
			#############################
			# キーがあるか確認
			if wGetLine[0] not in gVal.STR_SystemInfo :
				continue
			
			#############################
			# キーを設定
			gVal.STR_SystemInfo[wGetLine[0]] = wGetLine[1]
		
		#############################
		# システム情報の取得
		wCLS_work = CLS_OSIF()
		gVal.STR_SystemInfo['PythonVer'] = wCLS_work.Get_PythonVer()
		gVal.STR_SystemInfo['HostName']  = wCLS_work.Get_HostName()
		
		#############################
		# ログに記録する
		if gVal.FLG_Test_Mode==False :
			wRes['Reason'] = "実行"
		else:
			# テストモード
			wRes['Reason'] = "実行(テストモード)"
		gVal.OBJ_L.Log( "R", wRes )
		
		#############################
		# テスト終了
		return True



#####################################################
# Bot終了
#####################################################
	@classmethod
	def sBotEnd(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sBotEnd"
		
		#############################
		# 排他解除
		wRes = cls.sUnlock()
		if wRes['Result']!=True :
			wRes['Reason'] = "排他取得失敗: " + wRes['Reason']
			gVal.OBJ_L.Log( "C", wRes )
		
		#############################
		# DB終了
		gVal.OBJ_DB_IF.Close()
		return True



#####################################################
# 排他制御
#####################################################
	@classmethod
	def sLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sLock"
		
		#############################
		# テーブルがある
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ登録の確認
		if len(wResDB['Responce']['Data'])==0 :
			wRes['Reason'] = "Not Regist User"
			return wRes
		
		#############################
		# 辞書型に整形
		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ロックの取得
		wLocked  = wChgDict[0]['locked']
		wLUpdate = wChgDict[0]['lupdate']
		if wLocked==True :
			### 排他済み
			
			# ロック保持時間外かを求める (変換＆差)
			wGetLag = CLS_OSIF.sTimeLag( str(wLUpdate), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				return wRes
			if wGetLag['Beyond']==True :
				#反応時間外
				cls.sUnlock()	#一度解除する
				
				#ログに記録する
				wRes['Reason'] = "排他解除"
				gVal.OBJ_L.Log( "R", wRes )
				wRes['Reason'] = None
			
			else :
				wAtSec = gVal.DEF_STR_TLNUM['forLockLimSec'] - wGetLag['RateSec']
				wAtSec = CLS_OSIF.sGetFloor( wAtSec )	#小数点切り捨て
				wRes['Reason'] = "処理終了まであと " + str(wAtSec) + " 秒です"
				wRes['Responce'] = wAtSec
				wRes['Result']   = True
				return wRes
		
		#※排他がかかってない
		#############################
		# 排他する
		
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### wTD['TimeDate']
		
		wQuery = "update tbl_user_data set " + \
				"locked = True, " + \
				"lupdate = '" + str(wTD['TimeDate']) + "'" + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes	#排他あり



#####################################################
# 排他延長
#####################################################
	@classmethod
	def sExtLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sExtLock"
		
		#############################
		# テーブルがある
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ登録の確認
		if len(wResDB['Responce']['Data'])==0 :
			wRes['Reason'] = "Not Regist User"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ロックの取得
		wLocked  = wChgDict[0]['locked']
		wLUpdate = wChgDict[0]['lupdate']
		if wLocked!=True :
			### 排他がかかってない
			wRes['Reason'] = "Do not lock"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# 排他の延長 = 今の操作時間に更新する
		
		# 時間を取得
		wTD = CLS_OSIF.sGetTime()
		if wTD['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "PC時間の取得に失敗しました"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		### wTD['TimeDate']
		
		wQuery = "update tbl_user_data set " + \
				"lupdate = '" + str(wTD['TimeDate']) + "'" + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes



#####################################################
# 排他情報の取得
#####################################################
	@classmethod
	def sGetLock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sGetLock"
		
		wRes['Responce'] = {}
		wRes['Responce'].update({
			"Locked"    : False,
			"Beyond"    : False
		})
		
		#############################
		# テーブルがある
		wQuery = "select * from tbl_user_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# ユーザ登録の確認
		if len(wResDB['Responce']['Data'])==0 :
			wRes['Reason'] = "Not Regist User"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# ロックの取得
		wLocked  = wChgDict[0]['locked']
		wLUpdate = wChgDict[0]['lupdate']
		if wLocked==True :
			### 排他がかかってる
			
			# ロック保持時間外かを求める (変換＆差)
			wGetLag = CLS_OSIF.sTimeLag( str(wLUpdate), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				gVal.OBJ_L.Log( "B", wRes )
				return wRes
			if wGetLag['Beyond']==True :
				###解除可能
				wRes['Reason'] = "解除可能です"
			
			else :
				wAtSec = gVal.DEF_STR_TLNUM['forLockLimSec'] - wGetLag['RateSec']
				wAtSec = CLS_OSIF.sGetFloor( wAtSec )	#小数点切り捨て
				wRes['Reason'] = "処理終了まであと " + str(wAtSec) + " 秒です"
			
			#############################
			# ロック=ON, 排他解除 可or否
			wRes['Responce']['Beyond'] = wGetLag['Beyond']
		
		###else:
			#############################
			# ロック=OFF
		
		#############################
		# ロック状態 ON or OFF, 正常終了
		wRes['Responce']['Locked'] = wLocked
		wRes['Result'] = True
		return wRes



#####################################################
# 排他解除
#####################################################
	@classmethod
	def sUnlock(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_BotCtrl"
		wRes['Func']  = "sUnlock"
		
		#############################
		# 排他解除する
		wQuery = "update tbl_user_data set " + \
				"locked = False " + \
				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		wRes['Result']   = True
		return wRes	#排他なし



