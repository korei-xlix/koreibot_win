#!/usr/bin/python
# coding: UTF-8
#####################################################
# ::Project  : Korei Bot Win
# ::Admin    : Korei (@korei-xlix)
# ::github   : https://github.com/korei-xlix/koreibot_win/
# ::Class    : メイン処理(コンソール)
#####################################################

from osif import CLS_OSIF
from traffic import CLS_Traffic
from filectrl import CLS_File
from setup import CLS_Setup
from botctrl import CLS_BotCtrl
from mydisp import CLS_MyDisp

from twitter_main import CLS_TwitterMain
from gval import gVal
#####################################################
class CLS_Main_Console() :
#####################################################
	#使用クラス実体化
	OBJ_TwitterMain = ""
	
	FLG_MainDispClear = True

#####################################################
# 実行
#####################################################
	@classmethod
	def sRun(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRun"
		
		#############################
		# 実行チェック
		wTestRes = cls.sCheckTest()
		if wTestRes!=True :
			###処理終了
			CLS_OSIF.sInp( '\n' + "リターンキーを押して再度コンソールアプリを起動してください。[RT]" )
			return wRes
		
		### ※通常処理継続
		
		#############################
		# 初期化
		cls.OBJ_TwitterMain  = CLS_TwitterMain()	#メインの実体化
		wResIni = cls.OBJ_TwitterMain.Init()		#初期化
		if wResIni['Result']!=True :
			CLS_BotCtrl.sBotEnd()	#bot停止
			return wRes
		
		#############################
		# コマンド実行前処理
		wSubRes = cls.sFirstProcess()
		if wSubRes['Result']!=True :
			wRes['Reason'] = wSubRes['Reason']
			gVal.OBJ_L.Log( "B", wRes )
			CLS_BotCtrl.sBotEnd()	#bot停止
			return wRes
		
		#############################
		# コンソールを表示
		while True :
			wCommand = cls().sViewMainConsole()
			
			if wCommand=="" :
				###未入力は再度入力
				continue
			
			if wCommand.find("\\q")>=0 or wCommand=="exit" :
				#############################
				# 終了
				wRes['Reason'] = "コンソール停止"
				gVal.OBJ_L.Log( "R", wRes )
				CLS_BotCtrl.sBotEnd()	#bot停止
				break
				#############################
			
			#############################
			# コマンド実行前処理
			wSubRes = cls.sFirstProcess()
			if wSubRes['Result']!=True :
				wRes['Reason'] = wSubRes['Reason']
				gVal.OBJ_L.Log( "B", wRes )
				CLS_BotCtrl.sBotEnd()	#bot停止
				return wRes
			
			#############################
			# コマンド実行
			wResCmd = cls().sRunCommand( wCommand )
			
			#############################
			# 待機(入力待ち)
			CLS_OSIF.sInp( "リターンキーを押すと戻ります。[RT]" )
			
		return




#####################################################
# メインコンソール画面の表示
#####################################################
	@classmethod
	def sViewMainConsole(cls):
		
		#############################
		# メインコンソール画面
		wResDisp = CLS_MyDisp.sViewDisp( "MainConsole", inClear=cls.FLG_MainDispClear )
		if wResDisp['Result']==False :
			gVal.OBJ_L.Log( "D", wResDisp )
			return "\\q"	#失敗=強制終了
		
		wCommand = CLS_OSIF.sInp( "コマンド？=> " )
		return wCommand



#####################################################
# 実行
#####################################################
	@classmethod
	def sRunCommand( cls, inCommand ):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sRunCommand"
		
		#############################
		# Bot実行回数の記録
		gVal.STR_TrafficInfo['runbot'] += 1
		
	#####################################################
		#############################
		# 全自動監視の実行
		if inCommand=="\\g" :
			wSubRes = cls.OBJ_TwitterMain.AllRun()
			if wSubRes['Result']!=True :
				###失敗
				wRes['Reason'] = "OBJ_TwitterMain.AllRun failed: " + CLS_OSIF.sCatErr( wSubRes )
				gVal.OBJ_L.Log( "B", wRes )
				return False
			
			###トラヒック表示
			CLS_Traffic.sNowView()
		
		#############################
		# ユーザのみ更新
		elif inCommand=="\\gu" :
			cls.OBJ_TwitterMain.GetUser()
		
	#####################################################
		#############################
		# トレンドツイート
		elif inCommand=="\\tt" :
			cls.OBJ_TwitterMain.TrendTweet()
		
	#####################################################
		#############################
		# VIPいいね
		elif inCommand=="\\iv" :
			cls.OBJ_TwitterMain.VIPFavo()
		
		#############################
		# ちょっかいいいね
		elif inCommand=="\\ic" :
			cls.OBJ_TwitterMain.ChoFavo()
		
	#####################################################
		#############################
		# フォロワー情報の表示
		elif inCommand=="\\vf" :
			cls.OBJ_TwitterMain.ViewFollower( inFLGall=False )
		
		#############################
		# 全フォロワー情報の表示
		elif inCommand=="\\vfa" :
			cls.OBJ_TwitterMain.ViewFollower( inFLGall=True )
		
	#####################################################
		#############################
		# ユーザ管理
		elif inCommand=="\\u" :
			cls.OBJ_TwitterMain.UserAdmin()
		
	#####################################################
		#############################
		# Twitter APIの変更
		elif inCommand=="\\ca" :
			wResAPI = gVal.OBJ_Tw_IF.SetTwitter( gVal.STR_UserInfo['Account'] )
			if wResAPI['Result']!=True :
				wRes['Reason'] = "Set Twitter API failed: " + wResAPI['Reason']
				gVal.OBJ_L.Log( "D", wRes )
		
	#####################################################
		#############################
		# ログの表示(異常ログ)
		elif inCommand=="\\l" :
			gVal.OBJ_L.View( inViewMode="E" )
		
		#############################
		# ログの表示(運用ログ)
		elif inCommand=="\\lr" :
			gVal.OBJ_L.View( inViewMode="R" )
		
		#############################
		# ログの表示(全ログ)
		elif inCommand=="\\la" :
			gVal.OBJ_L.View()
		
		#############################
		# ログクリア
		elif inCommand=="\\lc" :
			gVal.OBJ_L.Clear()
		
		#############################
		# システム情報の表示
		elif inCommand=="\\v" :
			cls().sView_Sysinfo()
		
		#############################
		# トラヒック情報の表示
		elif inCommand=="\\vt" :
			wResTraffic = CLS_Traffic.sView()
			if wResTraffic['Result']!=True :
				gVal.OBJ_L.Log( "B", wResTraffic )
		
	#####################################################
		#############################
		# 救済処理
		elif inCommand=="\\ks" :
			cls().sKyusai()
			
#		#############################
#		# テスト
#		elif inCommand=="\\test" :
#			
###			wSubRes = cls.OBJ_TwitterMain.TestRun()
###			wTime = CLS_OSIF.sGetTimeformat_Twitter( "2021-10-06T12:23:44.000Z" )
###			print( str(wTime['TimeDate']) )
#
###			wSubRes = cls.OBJ_TwitterMain.CircleWeekend()
#
#			wSubRes = gVal.OBJ_Tw_IF.GetTweetLookup( "1473387112351559680" )
#			print( str(wSubRes) )
#
#			
	#####################################################
		#############################
		# ないコマンド
		else :
			wRes['Reason'] = "存在しないコマンド :" + str(inCommand)
			gVal.OBJ_L.Log( "D", wRes )
			return False
		
		return True



#####################################################
# 救済処理
#####################################################
	@classmethod
	def sKyusai(cls):
		#############################
		# DBのフォロワー一覧取得
		# ・監視対象ユーザ
		# ・自動リムーブ or リムーブ済みではない
		wQuery = "select * from tbl_follower_data where " + \
					"twitterid = '" + gVal.STR_UserInfo['Account'] + "' and " + \
					"adm_agent = True and " + \
					"rc_blockby = False and " + \
					"rc_follower = True " + \
					";"
		
		wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
		if wResDB['Result']!=True :
			wRes['Reason'] = "Run Query is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 辞書型に整形
		wARR_DBData = gVal.OBJ_DB_IF.ChgDict( wResDB['Responce'] )
		
		#############################
		# 添え字をIDに差し替える
		wARR_RateFollowers = gVal.OBJ_DB_IF.ChgDataID( wARR_DBData )
		
		wKeylist = list( wARR_RateFollowers.keys() )
		for wID in wKeylist :
			wID = str(wID)
			
			if wARR_RateFollowers[wID]['un_follower']==False and \
			   wARR_RateFollowers[wID]['limited']==False and \
			   wARR_RateFollowers[wID]['removed']==False :
				continue
			
			### 一定期間内ふぁぼられてない場合は除外
			wGetLag = CLS_OSIF.sTimeLag( str(wARR_RateFollowers[wID]['r_favo_date']), inThreshold=gVal.DEF_STR_TLNUM['forUnfollowSec'] )
			if wGetLag['Result']!=True :
				wRes['Reason'] = "sTimeLag failed(5)" + ": @" + wARR_RateFollowers[wID]['screen_name']
				gVal.OBJ_L.Log( "B", wRes )
				continue
			if wGetLag['Beyond']==True :
				###期間外 =除外
				wQuery = "update tbl_follower_data set " + \
							"limited = False, " + \
							"removed = True " + \
							"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
							" and id = '" + str(wID) + "' ;"
				
				wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
				if wResDB['Result']!=True :
					return wRes
				continue
			
			### フォロー外れてたら再フォロー
			if wARR_RateFollowers[wID]['rc_myfollow']==False :
				wSubRes = cls.OBJ_TwitterMain.SetMyFollow( wARR_RateFollowers[wID] )
				if wResDB['Result']!=True :
					return wRes
			
			wCnt = wARR_RateFollowers[wID]['r_favo_cnt'] + 1
			
			wQuery = "update tbl_follower_data set " + \
						"un_follower = False, " + \
						"r_favo_cnt = " + str(wCnt) + ", " + \
						"limited = False, " + \
						"removed = False " + \
						"where twitterid = '" + gVal.STR_UserInfo['Account'] + "'" + \
						" and id = '" + str(wID) + "' ;"
			
			wResDB = gVal.OBJ_DB_IF.RunQuery( wQuery )
			if wResDB['Result']!=True :
				return wRes

			wStr = "救済ユーザ: @" + wARR_RateFollowers[wID]['screen_name']
			CLS_OSIF.sPrn( wStr )
		
		return



#####################################################
# 実行チェック処理
#####################################################
	@classmethod
	def sCheckTest(cls):
		#############################
		# botテスト、引数ロード
		#   テスト項目
		#     1.引数ロード
		#     2.データベースの取得
		#     3.ログの取得
		#     4.排他
		#     5.Twitterの取得
		#     6.Readme情報の取得
		#     7.Python情報の取得
		#     8.TESTログ記録
		wResTest = CLS_BotCtrl.sBotTest()
		if wResTest!=True :
			return False	###問題あり
		
		wCLS_Setup = CLS_Setup()
		#############################
		# セットアップモードで実行
		if gVal.STR_SystemInfo['RunMode']=="setup" :
			wCLS_Setup.Setup()
			return False	###問題あり
		
		#############################
		# 初期化モードで実行
		elif gVal.STR_SystemInfo['RunMode']=="init" :
			wCLS_Setup.AllInit()
			return False	###問題あり
		
		#############################
		# データ追加モードで実行
		elif gVal.STR_SystemInfo['RunMode']=="add" :
			wCLS_Setup.Add()
			return False	###問題あり
		
		#############################
		# データクリアモードで実行
		elif gVal.STR_SystemInfo['RunMode']=="clear" :
			wCLS_Setup.Clear()
			return False	###問題あり
		
		#############################
		# =正常
		return True



#####################################################
# コマンド実行前処理
#####################################################
	@classmethod
	def sFirstProcess(cls):
		#############################
		# 応答形式の取得
		#   "Result" : False, "Class" : None, "Func" : None, "Reason" : None, "Responce" : None
		wRes = CLS_OSIF.sGet_Resp()
		wRes['Class'] = "CLS_Main_Console"
		wRes['Func']  = "sFirstProcess"
		
		cls.FLG_MainDispClear = True
		#############################
		# 時間を取得
		wSubRes = cls.OBJ_TwitterMain.TimeUpdate()
		if wSubRes['Result']!=True :
			###時間取得失敗  時計壊れた？
			wRes['Reason'] = "TimeUpdate is failed"
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 開始or前回チェックから15分経ったか
		w15Res = cls.OBJ_TwitterMain.Circle15min()
		if w15Res['Result']!=True :
			wRes['Reason'] = "Circle15min is failed"
			gVal.OBJ_L.Log( "C", wRes )
			return wRes
		
		wRateTimeDate = None
		###翌日か
		wTimeDate = gVal.STR_SystemInfo['TimeDate'].split(" ")
		wTimeDate = wTimeDate[0]
		
		wRateTimeDate = str( gVal.STR_SystemInfo['RateTimeDate'] )
		wRateTimeDate_Date = wRateTimeDate.split(" ")
		wRateTimeDate_Date = wRateTimeDate_Date[0]
		if wTimeDate!=wRateTimeDate_Date :
			gVal.STR_SystemInfo['NextDay'] = True
		
		###週末か
		wWeekend = CLS_OSIF.sGetNextWeekday( gVal.STR_SystemInfo['RateTimeDate'], gVal.STR_SystemInfo['TimeDate'], gVal.DEF_STR_TLNUM['weekendHour'], gVal.DEF_STR_TLNUM['weekendWeek'] )
		if wWeekend['Result']!=True :
			wRes['Reason'] = "sGetNextWeekday is faied"
			gVal.OBJ_L.Log( "C", wRes )
		else:
			gVal.STR_SystemInfo['Weekend'] = wWeekend['Weekend']
		
		#############################
		# トラヒック情報の記録
		wResTraffic = CLS_Traffic.sSet()
		if wResTraffic['Result']!=True :
			wRes['Reason'] = "Set Traffic failed: reason" + CLS_OSIF.sCatErr( wResTraffic )
			return wRes
		if wResTraffic['Responce']==True :
			CLS_OSIF.sPrn( "トラヒック情報が切り替わりました。" )
			wRes['Responce'] = False	#画面クリアさせない
			cls.FLG_MainDispClear = False	#画面クリアさせない
		
		wResTraffic = CLS_Traffic.sReport()
		if wResTraffic['Result']!=True :
			wRes['Reason'] = "sReport failed: reason" + CLS_OSIF.sCatErr( wResTraffic )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		
		#############################
		# 毎日処理
		if gVal.STR_SystemInfo['NextDay']==True :
			w1DayRes = cls.OBJ_TwitterMain.Circle1Day()
			if w1DayRes['Result']!=True :
				wRes['Reason'] = "Circle1Day is failed"
				gVal.OBJ_L.Log( "C", wRes )
				return wRes
			CLS_OSIF.sPrn( "毎日処理を実行しました。" )
			cls.FLG_MainDispClear = False	#画面クリアさせない
		
		#############################
		# ユーザ一覧取得
		wTwitterRes = cls.OBJ_TwitterMain.GetUser()
		if wTwitterRes['Result']!=True :
			###失敗
			wRes['Reason'] = "GetUser is failed: " + CLS_OSIF.sCatErr( wTwitterRes )
			gVal.OBJ_L.Log( "B", wRes )
			return wRes
		if wTwitterRes['Responce']==True :
			cls.FLG_MainDispClear = False	#画面クリアさせない
		
		#############################
		# 正常
		wRes['Result']   = True
		return wRes



#####################################################
# システム情報の表示
#####################################################
	@classmethod
	def sView_Sysinfo(cls):
		
		#############################
		# 画面クリア
		CLS_OSIF.sDispClr()
		
		#############################
		# ヘッダ表示
		wStr = "--------------------" + '\n'
		wStr = wStr + " システム情報" + '\n'
		wStr = wStr + "--------------------" + '\n'
		
		#############################
		# 時間の取得
		wRes = CLS_OSIF.sGetTime()
		if wRes['Result']==True :
			wStr = wStr + wRes['TimeDate'] + '\n'
		
		#############################
		# 情報組み立て
		wStr = wStr + "Client Name = " + gVal.STR_SystemInfo['Client_Name'] + '\n'
		wStr = wStr + "Project Name= " + gVal.STR_SystemInfo['ProjectName'] + '\n'
		wStr = wStr + "github      = " + gVal.STR_SystemInfo['github'] + '\n'
		wStr = wStr + "Admin       = " + gVal.STR_SystemInfo['Admin'] + '\n'
		wStr = wStr + "Twitter URL = " + gVal.STR_SystemInfo['TwitterURL'] + '\n'
		wStr = wStr + "Update      = " + gVal.STR_SystemInfo['Update'] + '\n'
		wStr = wStr + "Version     = " + gVal.STR_SystemInfo['Version'] + '\n'
		
		wStr = wStr + "Python      = " + str( gVal.STR_SystemInfo['PythonVer'] )  + '\n'
		wStr = wStr + "HostName    = " + gVal.STR_SystemInfo['HostName'] + '\n'
		
		#############################
		# コンソールに表示
		CLS_OSIF.sPrn( wStr )
		return




