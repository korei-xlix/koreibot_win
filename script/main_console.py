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
		# 自動監視
		if inCommand=="\\a" :
			cls.OBJ_TwitterMain.AllRun()
		
	#####################################################
###		#############################
###		# いいね解除
###		if inCommand=="\\ic" :
###			cls.OBJ_TwitterMain.RemFavo()
###		
		#############################
		# トレンドツイート
		elif inCommand=="\\tt" :
			cls.OBJ_TwitterMain.TrendTweet()
		
	#####################################################
		#############################
		# Twitter APIの変更
		elif inCommand=="\\ca" :
			wResAPI = gVal.OBJ_Tw_IF.SetTwitter( gVal.STR_UserInfo['Account'] )
			if wResAPI['Result']!=True :
				wRes['Reason'] = "Set Twitter API failed: " + wResAPI['Reason']
				gVal.OBJ_L.Log( "D", wRes )
		
		#############################
		# トレンドタグ設定
		elif inCommand=="\\tc" :
			cls.OBJ_TwitterMain.SetTrendTag()
		
		#############################
		# リスト通知設定
		elif inCommand=="\\lc" :
			cls.OBJ_TwitterMain.SetListInd()
		
	#####################################################
		#############################
		# リスト通知ユーザ表示
		elif inCommand=="\\lv" :
			cls.OBJ_TwitterMain.ViewListIndUser()
		
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
		
		#############################
		# テスト
		elif inCommand=="\\test" :
			
			wSubRes = cls.OBJ_TwitterMain.TestRun()
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




