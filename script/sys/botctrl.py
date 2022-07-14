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

from time import CLS_TIME
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
		
		wRes['Responce'] = {
			"hostname"		: None,
			"database"		: None,
			"username"		: None,
			"password"		: None
		}
		#############################
		# 引数取得
		wArg = CLS_OSIF.sGetArg()
		
		if len(wArg)<7 :	#引数が足りない
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(1)= " + str( wArg )
			CLS_OSIF.sErr( wRes )
###			return False
			return wRes
		
		#############################
		# モード、DB情報の取得
		wRes['Responce']['hostname'] = wArg[2]
		wRes['Responce']['database'] = wArg[3]
		wRes['Responce']['username'] = wArg[4]
		wRes['Responce']['password'] = wArg[5]
		
		#############################
		# add  : データ追加モード
		# word : 文字追加モード
		if wArg[1]=="add" or  \
		   wArg[1]=="word" :
			if len(wArg)!=8 :
###				wRes['Reason'] = "データ追加モード: 引数が足りません"
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(2)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
###				return False
				return wRes
			
			gVal.STR_SystemInfo['RunMode']      = wArg[1]
			gVal.STR_SystemInfo['EXT_FilePath'] = wArg[7]
			gVal.STR_UserInfo['Account']        = wArg[6]
###			return True
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# setup : セットアップモード
###		# init  : 初期化モード
###		# clear : クリアモード
###		elif len(wArg)==2 :	#モード
###			###セットアップモード
###			###全初期化モード
###			###データクリアモード
###			if wArg[1]!="setup" and \
###			   wArg[1]!="init" and \
###			   wArg[1]!="clear" :
###				wRes['Reason'] = "存在しないモードです"
###				CLS_OSIF.sErr( wRes )
###				return False
		elif wArg[1]=="setup" :
###		   wArg[1]=="init" or \
###		   wArg[1]=="clear" :
			if len(wArg)!=6 or len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(3)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			
			if len(wArg)==7 :
				gVal.STR_SystemInfo['EXT_FilePath'] = wArg[6]
			
###			return True
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# init  : 初期化モード
		elif wArg[1]=="init" :
			if len(wArg)!=6 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(4)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.STR_SystemInfo['RunMode'] = wArg[1]
			wRes['Result'] = True	#正常
			return wRes
		
		#############################
		# test : テストモード
###		elif len(wArg)==4 :	#テストモード : bottest か
###			if wArg[3]==gVal.DEF_TEST_MODE :
		elif wArg[1]==gVal.DEF_TEST_MODE :
			if len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(5)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.FLG_Test_Mode = True
		
		#############################
		# run : 通常モード
		elif wArg[1]=="run" :
			if len(wArg)!=7 :
				wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません(6)= " + str( wArg )
				CLS_OSIF.sErr( wRes )
				return wRes
			
			gVal.FLG_Test_Mode = False
		
###		elif len(wArg)!=3 :	#引数が足りない
###			wRes['Reason'] = "CLS_BotCtrl: sBotTest: 引数が足りません= " + str( wArg )
###			CLS_OSIF.sErr( wRes )
###			return False
		
		else:
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: コマンドがありません= " + str( wArg )
			CLS_OSIF.sErr( wRes )
			return wRes
		
###		gVal.STR_UserInfo['Account'] = wArg[1]	#ユーザ名
###		wPassword                    = wArg[2]	#パスワード
		gVal.STR_SystemInfo['RunMode'] = "Normal"
		gVal.STR_UserInfo['Account']   = wArg[6]
		
		#############################
		# DBに接続
		gVal.OBJ_DB_IF = CLS_DB_IF()
###		wSubRes = gVal.OBJ_DB_IF.Connect( inPassWD=wPassword )
		wSubRes = gVal.OBJ_DB_IF.Connect( wRes['Responce'] )
		if wSubRes['Result']!=True :
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: DB接続失敗: reason=" + wResDB['Reason']
			CLS_OSIF.sErr( wRes )
###			return False
			return wRes
		if wSubRes['Responce']!=True :
			##テーブルがない= 初期化してない
			wRes['Reason'] = "CLS_BotCtrl: sBotTest: DB未構築"
			CLS_OSIF.sErr( wRes )
			gVal.OBJ_DB_IF.Close()
###			return False
			return wRes
		
		#############################
		# ログオブジェクトの生成
		gVal.OBJ_L = CLS_Mylog()
		
###		#############################
###		# テーブルがある
###		wQuery = "select * from tbl_user_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					";"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ユーザ登録の確認
###		if len(wResDB['Responce']['Data'])==0 :
###			wRes['Reason'] = "ユーザが登録されていません =" + gVal.STR_UserInfo['Account']
###			gVal.OBJ_L.Log( "D", wRes )
###			gVal.OBJ_DB_IF.Close()
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
###		
###		#############################
###		# ユーザ登録の抽出
###		wAPIkey    = wChgDict[0]['apikey']
###		wAPIsecret = wChgDict[0]['apisecret']
###		wACCtoken  = wChgDict[0]['acctoken']
###		wACCsecret = wChgDict[0]['accsecret']
###		wBearer    = wChgDict[0]['bearer']
		#############################
		# Twitterデータ取得
		wTwitterDataRes = gVal.OBJ_DB_IF.GetTwitterData( gVal.STR_UserInfo['Account'] )
		if wTwitterDataRes['Result']!=True :
			wRes['Reason'] = "GetTwitterData is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
###		#############################
###		# 前回ロック時間の取得(=前回bot実行時間)
###		gVal.STR_SystemInfo['RateLockTD'] = wChgDict[0]['lupdate']
###		
		#############################
		# 排他開始
		wLock = cls.sLock()
		if wLock['Result']!=True :
			wRes['Reason'] = "排他取得失敗: " + wLock['Reason']
			gVal.OBJ_L.Log( "A", wRes )
			gVal.OBJ_DB_IF.Close()
###			return
			return wRes
		elif wLock['Responce']!=None :
			gVal.OBJ_L.Log( "S", wRes, "排他中" )
			
			CLS_OSIF.sPrn( "処理待機中です。CTRL+Cで中止することもできます。" )
			CLS_OSIF.sPrn( wLock['Reason'] + '\n' )
			
			wResStop = CLS_OSIF.sPrnWAIT( wLock['Responce'] )
			if wResStop==False :
				###ウェイト中止
				CLS_OSIF.sPrn( '\n' + "待機を中止しました。プログラムを停止しました。" )
				gVal.OBJ_DB_IF.Close()
###				return
				return wRes
		
		#############################
		# Twitterに接続
		gVal.OBJ_Tw_IF = CLS_Twitter_IF()
###		wTwitterRes = gVal.OBJ_Tw_IF.Connect( wAPIkey, wAPIsecret, wACCtoken, wACCsecret, wBearer )
		wTwitterRes = gVal.OBJ_Tw_IF.Connect( wTwitterDataRes['Responce'] )
		if wTwitterRes['Result']!=True :
			wRes['Reason'] = "Twitterの接続失敗: reason=" + wResTwitter['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			cls.sBotEnd()	#bot終了
###			return False
			return wRes
		
		#############################
		# 時間を取得
###		wTD = CLS_OSIF.sGetTime()
###		if wTD['Result']!=True :
###			###時間取得失敗  時計壊れた？
##			wRes['Reason'] = "PC時間取得失敗"
##			gVal.OBJ_L.Log( "B", wRes )
###			wRes['Reason'] = "PC time get is failer" + '\n'
###			gVal.OBJ_L.Log( "C", wRes )
###			cls.sBotEnd()	#bot終了
###			return
###			return wRes
		wTD = CLS_TIME.sGet( wRes, "(1)" )
		if wTD['Result']!=True :
			cls.sBotEnd()	#bot終了
			return wRes
		### wTD['TimeDate']
###		gVal.STR_SystemInfo['APIrect'] = str(wTD['TimeDate'])
###		
		#############################
		# コマンド実行時間を設定
		wTimeRes = gVal.OBJ_DB_IF.SetTimeInfo( gVal.STR_UserInfo['Account'], "run", wTD['TimeDate'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "SetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# Version情報
		wReadme = []
		if CLS_File.sReadFile( gVal.DEF_STR_FILE['Readme'], outLine=wReadme )!=True :
			wRes['Reason'] = "Readme.mdファイルが見つかりません: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
###			return False
			return wRes
		
		if len(wReadme)<=1 :
			wRes['Reason'] = "Readme.mdファイルが空です: path=" + gVal.DEF_STR_FILE['Readme']
			gVal.OBJ_L.Log( "D", wRes )
			cls.sBotEnd()	#bot終了
###			return False
			return wRes
		
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
		
###		#############################
###		# いいね者送信日時(直近)
###		if wChgDict[0]['favodate']=="" or \
###		   wChgDict[0]['favodate']==None :
###			wChgDict[0]['favodate'] = str(wTD['TimeDate'])
###			wResDB = gVal.OBJ_DB_IF.UpdateFavoDate( str(wTD['TimeDate']) )
###			gVal.OBJ_L.Log( "N", wRes, "いいね日時初期化" )
###		gVal.STR_UserInfo['FavoDate'] = wChgDict[0]['favodate']
###		
###		#############################
###		# トレンドタグの取得
###		if wChgDict[0]['trendtag']==None :
###			wChgDict[0]['trendtag'] = ""
###		gVal.STR_UserInfo['TrendTag'] = wChgDict[0]['trendtag']
###		
###		#############################
###		# リスト通知
###		if wChgDict[0]['listname']==None :
###			wChgDict[0]['listname'] = ""
###		gVal.STR_UserInfo['ListName'] = wChgDict[0]['listname']
###		
###		#############################
###		# 自動リムーブ
###		if wChgDict[0]['arlistname']==None :
###			wChgDict[0]['arlistname'] = ""
###		gVal.STR_UserInfo['ArListName'] = wChgDict[0]['arlistname']
###		
###		if wChgDict[0]['listdate']=="" or \
###		   wChgDict[0]['listdate']==None :
###			### 初期化
###			wChgDict[0]['listdate'] = str(wTD['TimeDate'])
###		gVal.STR_UserInfo['ListDate'] = wChgDict[0]['listdate']
###		
###		#############################
###		# リストいいね日時
###		if wChgDict[0]['lfavdate']=="" or \
###		   wChgDict[0]['lfavdate']==None :
###			### 初期化
###			wChgDict[0]['lfavdate'] = str(wTD['TimeDate'])
###		gVal.STR_UserInfo['LFavoDate'] = wChgDict[0]['lfavdate']
		#############################
		# 時間情報の取得
		wListRes = gVal.OBJ_DB_IF.GetTimeInfo( gVal.STR_UserInfo['Account'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "GetTimeInfo is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# トレンドタグ、リスト通知の取得
		wListRes = gVal.OBJ_DB_IF.GetListName( gVal.STR_UserInfo['Account'] )
		if wListRes['Result']!=True :
			wRes['Reason'] = "GetListName is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# システム情報の取得
		wCLS_work = CLS_OSIF()
		gVal.STR_SystemInfo['PythonVer'] = wCLS_work.Get_PythonVer()
		gVal.STR_SystemInfo['HostName']  = wCLS_work.Get_HostName()
		
		#############################
		# ログに記録する
		if gVal.FLG_Test_Mode==False :
			gVal.OBJ_L.Log( "S", wRes, "bot実行" )
		else:
			# テストモード
			gVal.OBJ_L.Log( "S", wRes, "bot実行(テストモード)" )
		
		#############################
		# テスト終了
###		return True
		wRes['Result'] = True	#正常
		return wRes



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
		
###		#############################
###		# テーブルがある
###		wQuery = "select * from tbl_user_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					";"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ユーザ登録の確認
###		if len(wResDB['Responce']['Data'])==0 :
###			wRes['Reason'] = "Not Regist User"
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
###		
		#############################
		# ロックの取得
###		wLocked  = wChgDict[0]['locked']
###		wLUpdate = wChgDict[0]['lupdate']
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
###		if wLocked==True :
		if wRes['Responce']['locked']==True :
			### 排他済み
			
			# ロック保持時間外かを求める (変換＆差)
###			wGetLag = CLS_OSIF.sTimeLag( str(wLUpdate), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
###			wGetLag = CLS_OSIF.sTimeLag( str(wRes['Responce']['lok_date']), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			wGetLag = CLS_OSIF.sTimeLag( str(wRes['Responce']['get_date']), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed"
				return wRes
			if wGetLag['Beyond']==True :
				#反応時間外
				cls.sUnlock()	#一度解除する
				
				#ログに記録する
				gVal.OBJ_L.Log( "S", wRes, "排他解除" )
				wRes['Reason'] = None
			
			else :
				wAtSec = gVal.DEF_STR_TLNUM['forLockLimSec'] - wGetLag['RateSec']
				wAtSec = CLS_OSIF.sGetFloor( wAtSec )	#小数点切り捨て
				wRes['Reason'] = "処理終了まであと " + str(wAtSec) + " 秒です"
				wRes['Responce'] = wAtSec
				wRes['Result']   = True
				return wRes
		
		#※排他がかかってない
###		#############################
###		# 排他する
###		
		#############################
		# 時間を取得
###		wTD = CLS_OSIF.sGetTime()
###		if wTD['Result']!=True :
###			###時間取得失敗  時計壊れた？
###			wRes['Reason'] = "PC時間の取得に失敗しました"
###			gVal.OBJ_L.Log( "B", wRes )
###			wRes['Reason'] = "PC time get is failer"
###			gVal.OBJ_L.Log( "C", wRes )
###			return wRes
###		### wTD['TimeDate']
		wTD = CLS_TIME.sGet( wRes, "(2)" )
		if wTD['Result']!=True :
			return wRes
		
###		wQuery = "update tbl_user_data set " + \
###				"locked = True, " + \
###				"lupdate = '" + str(wTD['TimeDate']) + "'" + \
###				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
		
###		gVal.STR_SystemInfo['Day']  = False
###		gVal.STR_SystemInfo['Week'] = False
###		#############################
###		# 1日経過か
###		wGetLag = CLS_OSIF.sTimeLag( str(wRes['Responce']['day_date']), inThreshold=gVal.DEF_VAL_DAY )
###		if wGetLag['Result']!=True :
###			wRes['Reason'] = "sTimeLag failed"
###			return wRes
###		if wGetLag['Beyond']==True :
###			#反応時間外 =1日経過
###			gVal.STR_SystemInfo['Day'] = True
###		
###		#############################
###		# 1週間経過か
###		wGetLag = CLS_OSIF.sTimeLag( str(wRes['Responce']['week_date']), inThreshold=gVal.DEF_VAL_WEEK )
###		if wGetLag['Result']!=True :
###			wRes['Reason'] = "sTimeLag failed"
###			return wRes
###		if wGetLag['Beyond']==True :
###			#反応時間外 =1日経過
###			gVal.STR_SystemInfo['Week'] = True
###		
		#############################
		# 排他する
###		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], True, wTD['TimeDate'], gVal.STR_SystemInfo['Day'], gVal.STR_SystemInfo['Week'] )
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], True, wTD['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
###		#ログに記録する
###		gVal.OBJ_L.Log( "S", wRes, "排他開始" )
###		
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
		
###		#############################
###		# テーブルがある
###		wQuery = "select * from tbl_user_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					";"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ユーザ登録の確認
###		if len(wResDB['Responce']['Data'])==0 :
###			wRes['Reason'] = "Not Regist User"
###			gVal.OBJ_L.Log( "D", wRes )
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		#############################
		# ロックの取得
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ロックの取得
###		wLocked  = wChgDict[0]['locked']
###		wLUpdate = wChgDict[0]['lupdate']
###		if wLocked!=True :
		if wRes['Responce']['locked']==True :
			### 排他がかかってない
			wRes['Reason'] = "Do not lock"
			gVal.OBJ_L.Log( "D", wRes )
			return wRes
		
		#############################
		# 排他の延長 = 今の操作時間に更新する
		
		# 時間を取得
###		wTD = CLS_OSIF.sGetTime()
###		if wTD['Result']!=True :
###			###時間取得失敗  時計壊れた？
###			wRes['Reason'] = "PC時間の取得に失敗しました"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		### wTD['TimeDate']
		wTD = CLS_TIME.sGet( wRes, "(3)" )
		if wTD['Result']!=True :
			return wRes
		
###		wQuery = "update tbl_user_data set " + \
###				"lupdate = '" + str(wTD['TimeDate']) + "'" + \
###				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
		#############################
		# 排他する
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], True, wTD['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
###		#ログに記録する
###		gVal.OBJ_L.Log( "S", wRes, "排他延長" )
###		
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
		
###		wRes['Responce'] = {}
###		wRes['Responce'].update({
###			"Locked"    : False,
###			"Beyond"    : False
###		})
		wRes['Responce'] = {
			"Locked"    : False,
			"Beyond"    : False
		}
		
###		#############################
###		# テーブルがある
###		wQuery = "select * from tbl_user_data where " + \
###					"twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
###					";"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# ユーザ登録の確認
###		if len(wResDB['Responce']['Data'])==0 :
###			wRes['Reason'] = "Not Regist User"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
###		
###		#############################
###		# 辞書型に整形
###		wChgDict = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		#############################
		# ロックの取得
		wLockRes = gVal.OBJ_DB_IF.GetLock( gVal.STR_UserInfo['Account'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		#############################
		# ロックの取得
###		wLocked  = wChgDict[0]['locked']
###		wLUpdate = wChgDict[0]['lupdate']
###		if wLocked==True :
		if wRes['Responce']['locked']==True :
			### 排他がかかってる
			
			# ロック保持時間外かを求める (変換＆差)
###			wGetLag = CLS_OSIF.sTimeLag( str(wLUpdate), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
			wGetLag = CLS_OSIF.sTimeLag( str(wLockRes['Responce']['get_date']), inThreshold=gVal.DEF_STR_TLNUM['forLockLimSec'] )
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
###		wQuery = "update tbl_user_data set " + \
###				"locked = False " + \
###				"where twitterid = '" + gVal.STR_UserInfo['Account'] + "' ;"
###		
###		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
###		if wResDB['Result']!=True :
###			wRes['Reason'] = "Run Query is failed"
###			gVal.OBJ_L.Log( "B", wRes )
###			return wRes
		#############################
		# 排他解除
		wLockRes = gVal.OBJ_DB_IF.SetLock( gVal.STR_UserInfo['Account'], False, wTD['TimeDate'] )
		if wLockRes['Result']!=True :
			wRes['Reason'] = "GetLock is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
###		#ログに記録する
###		gVal.OBJ_L.Log( "S", wRes, "排他解除" )
###		
		wRes['Result']   = True
		return wRes	#排他なし



